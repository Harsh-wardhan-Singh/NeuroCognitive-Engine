from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from config.settings import (
    DECAY_RATE,
    GUESS_PROB,
    LEARNING_RATE,
    MAX_QUESTION_HISTORY,
    MAX_RECENT_CONCEPTS,
    SLIP_PROB,
)
from engines.ai_generation.explanation_generator import generate_explanation
from engines.ai_generation.question_generator import generate_question
from engines.cognitive_engine.confidence_model import update_confidence
from engines.cognitive_engine.mastery_update import update_mastery
from engines.cognitive_engine.retention_decay import apply_decay
from engines.quiz_engine.engine import generate_next_question
from engines.risk_engine.predictor import predict_risk
from orchestrator.session_manager import create_session, get_session, update_session
from orchestrator.utils import (
    build_concept_id,
    datetime_to_unix_timestamp,
    get_avg_time_for_concept,
    validate_num_questions,
    validate_submit_input,
)
from services.analytics_service import calculate_streak, generate_session_summary
from services.attempt_service import get_concept_attempt_stats, log_attempt
from services.concept_service import get_concepts
from services.mastery_service import get_mastery_state, upsert_mastery_state
from services.session_service import get_last_questions, get_session_question_record, store_session_question
from services.user_service import get_session_attempts, get_user_record


def _build_concepts_and_risks(db: Session, user_id: UUID, subject: str, topic: str, current_time: float):
    concepts = []
    risks = {}
    for concept in get_concepts(subject, topic):
        concept_id = build_concept_id(subject, topic, concept)
        mastery_state = get_mastery_state(db, user_id, concept_id)
        stats = get_concept_attempt_stats(db, user_id, concept_id)

        mastery = mastery_state["mastery"] if mastery_state else 0.5
        confidence = mastery_state["confidence"] if mastery_state else 0.5
        last_seen = (
            datetime_to_unix_timestamp(mastery_state["last_seen_timestamp"])
            if mastery_state
            else current_time
        )

        concept_data = {
            "concept_id": concept_id,
            "mastery": mastery,
            "confidence": confidence,
            "last_seen_timestamp": last_seen,
            "attempts": stats["attempts"],
            "correct_attempts": stats["correct_attempts"],
        }
        risk = predict_risk(concept_data, current_time)

        concepts.append(
            {
                "concept_id": concept_id,
                "mastery": mastery,
                "confidence": confidence,
                "attempts": stats["attempts"],
                "correct_attempts": stats["correct_attempts"],
            }
        )
        risks[concept_id] = risk

    return concepts, risks


def start_session(db: Session, user_id: UUID, subject: str, topic: str, num_questions: int):
    validate_num_questions(num_questions)

    user = get_user_record(db, user_id)
    if user is None:
        raise ValueError("User does not exist")

    now = datetime.utcnow()
    current_time = datetime_to_unix_timestamp(now)
    concepts, risks = _build_concepts_and_risks(db, user_id, subject, topic, current_time)

    session_state = {
        "current_streak": 0,
        "last_concept": None,
        "recent_concepts": [],
    }
    selection = generate_next_question(concepts, risks, session_state)
    selected_concept_id = selection["concept_id"]
    difficulty = selection["difficulty"]

    session = create_session(
        db,
        {
            "user_id": user_id,
            "subject": subject,
            "topic": topic,
            "total_questions": num_questions,
            "questions_answered": 0,
            "current_concept": selected_concept_id,
            "is_active": True,
        },
    )

    recent_questions = get_last_questions(db, session["session_id"], MAX_QUESTION_HISTORY)

    generated = generate_question(selected_concept_id, difficulty, recent_questions)
    question_id = str(uuid4())

    store_session_question(
        db,
        {
            "session_id": session["session_id"],
            "question_id": question_id,
            "concept_id": selected_concept_id,
            "question_text": generated["question"],
            "options": generated["options"],
            "correct_option": generated["correct_answer"],
            "difficulty_level": difficulty,
        },
    )

    return {
        "session_id": session["session_id"],
        "question": {
            "question_id": question_id,
            "text": generated["question"],
            "options": generated["options"],
        },
    }


def submit_answer(
    db: Session,
    user_id: UUID,
    session_id: UUID,
    question_id: str,
    selected_option: str,
    reported_confidence: float,
    response_time: float,
):
    validate_submit_input(selected_option, reported_confidence, response_time)

    session = get_session(db, session_id)
    if session is None:
        raise ValueError("Session not found")
    if session["user_id"] != user_id:
        raise ValueError("Session does not belong to user")
    if not session["is_active"]:
        raise ValueError("Session is inactive")

    question_row = get_session_question_record(db, session_id, question_id)
    if question_row is None:
        raise ValueError("Question not found in session")

    correct = selected_option == question_row.correct_option

    log_attempt(
        db,
        user_id,
        question_row.concept_id,
        question_id,
        correct,
        response_time,
        reported_confidence,
    )

    now = datetime.utcnow()
    now_unix = datetime_to_unix_timestamp(now)
    mastery_state = get_mastery_state(db, user_id, question_row.concept_id)

    prior_mastery = mastery_state["mastery"] if mastery_state else 0.5
    prior_confidence = mastery_state["confidence"] if mastery_state else 0.5
    last_seen_unix = (
        datetime_to_unix_timestamp(mastery_state["last_seen_timestamp"])
        if mastery_state
        else now_unix
    )

    decayed_mastery = apply_decay(prior_mastery, last_seen_unix, now_unix, DECAY_RATE)
    new_mastery = update_mastery(decayed_mastery, correct, SLIP_PROB, GUESS_PROB, LEARNING_RATE)

    avg_time = get_avg_time_for_concept(question_row.concept_id)
    new_confidence = update_confidence(prior_confidence, reported_confidence, correct, response_time, avg_time)

    upsert_mastery_state(
        db,
        user_id,
        question_row.concept_id,
        new_mastery,
        new_confidence,
        now,
    )

    answered = session["questions_answered"] + 1
    is_complete = answered >= session["total_questions"]

    explanation_payload = generate_explanation(question_row.question_text, question_row.correct_option)
    explanation = explanation_payload.get("explanation", "Explanation unavailable.")

    if is_complete:
        update_session(
            db,
            session_id,
            {
                "questions_answered": answered,
                "current_concept": session["current_concept"],
                "is_active": False,
            },
        )
        return {
            "correct": correct,
            "explanation": explanation,
            "next_question": None,
            "is_session_complete": True,
        }

    concepts, risks = _build_concepts_and_risks(db, user_id, session["subject"], session["topic"], now_unix)
    attempts = get_session_attempts(db, user_id, session["started_at"], now)
    recent_concepts = [row.concept_id for row in attempts[-MAX_RECENT_CONCEPTS:]] if len(attempts) >= MAX_RECENT_CONCEPTS else [row.concept_id for row in attempts]
    session_state = {
        "current_streak": calculate_streak(attempts),
        "last_concept": question_row.concept_id,
        "recent_concepts": recent_concepts,
    }
    selection = generate_next_question(concepts, risks, session_state)
    next_concept_id = selection["concept_id"]
    next_difficulty = selection["difficulty"]

    recent_questions = get_last_questions(db, session_id, MAX_QUESTION_HISTORY)

    generated = generate_question(next_concept_id, next_difficulty, recent_questions)
    next_question_id = str(uuid4())
    store_session_question(
        db,
        {
            "session_id": session_id,
            "question_id": next_question_id,
            "concept_id": next_concept_id,
            "question_text": generated["question"],
            "options": generated["options"],
            "correct_option": generated["correct_answer"],
            "difficulty_level": next_difficulty,
        },
    )

    update_session(
        db,
        session_id,
        {
            "questions_answered": answered,
            "current_concept": next_concept_id,
            "is_active": True,
        },
    )

    return {
        "correct": correct,
        "explanation": explanation,
        "next_question": {
            "question_id": next_question_id,
            "text": generated["question"],
            "options": generated["options"],
        },
        "is_session_complete": False,
    }


def end_session(db: Session, user_id: UUID, session_id: UUID):
    session = get_session(db, session_id)
    if session is None:
        raise ValueError("Session not found")
    if session["user_id"] != user_id:
        raise ValueError("Session does not belong to user")

    summary = generate_session_summary(db, user_id, session_id)

    update_session(
        db,
        session_id,
        {
            "questions_answered": session["questions_answered"],
            "current_concept": session["current_concept"],
            "is_active": False,
        },
    )

    return {
        "summary": {
            "accuracy": summary["accuracy"],
            "avg_confidence": summary["avg_confidence"],
            "weak_concepts": summary["weak_concepts"],
            "strong_concepts": summary["strong_concepts"],
            "risk_insights": summary["risk_insights"],
        }
    }

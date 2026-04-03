from pathlib import Path
from datetime import datetime
import os
import sys
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
from db.crud import (
    create_auth_user,
    create_session,
    create_session_question,
    create_user,
    get_mastery_state,
    get_attempt_stats_for_concept,
    get_recent_session_questions,
    get_session,
    get_session_question,
    get_user_by_email,
    list_attempts_for_session_window,
    list_mastery_states_for_user,
    log_attempt,
    update_session,
    upsert_mastery_state,
)
from db.models import Attempt, MasteryState


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_create_user_returns_uuid() -> None:
    db = _build_test_session()

    output = create_user(db)
    expected = "UUID"
    actual = type(output).__name__

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_log_attempt_inserts_row() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    log_attempt(
        db,
        {
            "user_id": user_id,
            "concept_id": "probability_basics",
            "question_id": "q_100",
            "correct": True,
            "reported_confidence": 0.7,
            "response_time": 9.8,
        },
    )

    row = db.query(Attempt).first()
    expected = {
        "user_id": user_id,
        "concept_id": "probability_basics",
        "question_id": "q_100",
        "correct": True,
        "reported_confidence": 0.7,
        "response_time": 9.8,
    }
    actual = {
        "user_id": row.user_id,
        "concept_id": row.concept_id,
        "question_id": row.question_id,
        "correct": row.correct,
        "reported_confidence": row.reported_confidence,
        "response_time": row.response_time,
    }

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_get_mastery_state_returns_3_field_dict() -> None:
    db = _build_test_session()
    user_id = create_user(db)
    timestamp = datetime(2026, 4, 3, 12, 0, 0)

    upsert_mastery_state(
        db,
        {
            "user_id": user_id,
            "concept_id": "probability_basics",
            "mastery": 0.65,
            "confidence": 0.54,
            "last_seen_timestamp": timestamp,
        },
    )

    output = get_mastery_state(db, user_id, "probability_basics")
    expected = {
        "mastery": 0.65,
        "confidence": 0.54,
        "last_seen_timestamp": timestamp,
    }

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected
    db.close()


def test_upsert_mastery_state_updates_existing_row() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    upsert_mastery_state(
        db,
        {
            "user_id": user_id,
            "concept_id": "probability_basics",
            "mastery": 0.4,
            "confidence": 0.3,
            "last_seen_timestamp": datetime(2026, 4, 3, 10, 0, 0),
        },
    )

    upsert_mastery_state(
        db,
        {
            "user_id": user_id,
            "concept_id": "probability_basics",
            "mastery": 0.8,
            "confidence": 0.7,
            "last_seen_timestamp": datetime(2026, 4, 3, 13, 0, 0),
        },
    )

    rows = db.query(MasteryState).all()
    output = {
        "row_count": len(rows),
        "mastery": rows[0].mastery,
        "confidence": rows[0].confidence,
    }
    expected = {
        "row_count": 1,
        "mastery": 0.8,
        "confidence": 0.7,
    }

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected
    db.close()


def test_create_auth_user_and_lookup_by_email() -> None:
    db = _build_test_session()

    create_auth_user(
        db,
        {
            "email": "learner@example.com",
            "password_hash": "hashed_password",
        },
    )

    row = get_user_by_email(db, "learner@example.com")
    expected = "learner@example.com"
    actual = row.email if row else None

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_session_create_get_update_flow() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    created = create_session(
        db,
        {
            "user_id": user_id,
            "subject": "math",
            "topic": "algebra",
            "total_questions": 10,
            "questions_answered": 0,
            "current_concept": "math.algebra.linear_equations",
            "is_active": True,
        },
    )

    fetched = get_session(db, created["session_id"])
    updated = update_session(
        db,
        created["session_id"],
        {
            "questions_answered": 1,
            "current_concept": "math.algebra.quadratic_equations",
            "is_active": True,
        },
    )

    expected_get = "math.algebra.linear_equations"
    actual_get = fetched["current_concept"] if fetched else None
    print("Expected:", expected_get)
    print("Got:", actual_get)
    assert actual_get == expected_get

    expected_update = {
        "questions_answered": 1,
        "current_concept": "math.algebra.quadratic_equations",
    }
    actual_update = {
        "questions_answered": updated["questions_answered"] if updated else None,
        "current_concept": updated["current_concept"] if updated else None,
    }
    print("Expected:", expected_update)
    print("Got:", actual_update)
    assert actual_update == expected_update
    db.close()


def test_session_question_storage_and_correct_option_fetch() -> None:
    db = _build_test_session()
    user_id = create_user(db)
    session = create_session(
        db,
        {
            "user_id": user_id,
            "subject": "math",
            "topic": "algebra",
            "total_questions": 10,
            "questions_answered": 0,
            "current_concept": "math.algebra.linear_equations",
            "is_active": True,
        },
    )

    create_session_question(
        db,
        {
            "session_id": session["session_id"],
            "question_id": "q_1",
            "concept_id": "math.algebra.linear_equations",
            "question_text": "Solve x + 2 = 5",
            "options": ["1", "2", "3", "4"],
            "correct_option": "3",
            "difficulty_level": "EASY",
        },
    )

    row = get_session_question(db, session["session_id"], "q_1")
    expected_correct = "3"
    actual_correct = row.correct_option if row else None

    print("Expected:", expected_correct)
    print("Got:", actual_correct)
    assert actual_correct == expected_correct

    recent = get_recent_session_questions(db, session["session_id"], limit=15)
    expected_recent = ["Solve x + 2 = 5"]
    print("Expected:", expected_recent)
    print("Got:", recent)
    assert recent == expected_recent
    db.close()


def test_get_attempt_stats_for_concept() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    log_attempt(
        db,
        {
            "user_id": user_id,
            "concept_id": "math.algebra.linear_equations",
            "question_id": "q1",
            "correct": True,
            "reported_confidence": 0.8,
            "response_time": 5.0,
        },
    )
    log_attempt(
        db,
        {
            "user_id": user_id,
            "concept_id": "math.algebra.linear_equations",
            "question_id": "q2",
            "correct": False,
            "reported_confidence": 0.5,
            "response_time": 7.0,
        },
    )

    output = get_attempt_stats_for_concept(db, user_id, "math.algebra.linear_equations")
    expected = {"attempts": 2, "correct_attempts": 1}

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected
    db.close()


def test_session_window_attempts_and_mastery_list() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    log_attempt(
        db,
        {
            "user_id": user_id,
            "concept_id": "math.algebra.linear_equations",
            "question_id": "q1",
            "correct": True,
            "reported_confidence": 0.7,
            "response_time": 6.0,
        },
    )

    now = datetime.utcnow()
    attempts = list_attempts_for_session_window(db, user_id, now.replace(year=2000), now.replace(year=2100))

    upsert_mastery_state(
        db,
        {
            "user_id": user_id,
            "concept_id": "math.algebra.linear_equations",
            "mastery": 0.62,
            "confidence": 0.55,
            "last_seen_timestamp": datetime.utcnow(),
        },
    )
    mastery_rows = list_mastery_states_for_user(db, user_id)

    expected = {"attempt_count": 1, "mastery_count": 1}
    actual = {"attempt_count": len(attempts), "mastery_count": len(mastery_rows)}

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def run_all() -> None:
    test_create_user_returns_uuid()
    test_log_attempt_inserts_row()
    test_get_mastery_state_returns_3_field_dict()
    test_upsert_mastery_state_updates_existing_row()
    test_create_auth_user_and_lookup_by_email()
    test_session_create_get_update_flow()
    test_session_question_storage_and_correct_option_fetch()
    test_get_attempt_stats_for_concept()
    test_session_window_attempts_and_mastery_list()


if __name__ == "__main__":
    run_all()

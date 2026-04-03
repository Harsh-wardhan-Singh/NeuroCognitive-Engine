from uuid import UUID

from sqlalchemy.orm import Session

from db.crud import (
    get_attempt_stats_for_concept,
    log_attempt as crud_log_attempt,
)
from db.models import Attempt, SessionQuestion


def log_attempt(
    db: Session,
    user_id: UUID,
    concept_id: str,
    question_id: str,
    correct: bool,
    response_time: float,
    confidence: float,
):
    payload = {
        "user_id": user_id,
        "concept_id": concept_id,
        "question_id": question_id,
        "correct": correct,
        "reported_confidence": confidence,
        "response_time": response_time,
    }
    return crud_log_attempt(db, payload)


def get_attempts_by_session(db: Session, session_id: UUID):
    return (
        db.query(Attempt)
        .join(
            SessionQuestion,
            Attempt.question_id == SessionQuestion.question_id,
        )
        .filter(SessionQuestion.session_id == session_id)
        .all()
    )


def get_concept_attempt_stats(db: Session, user_id: UUID, concept_id: str):
    return get_attempt_stats_for_concept(db, user_id, concept_id)

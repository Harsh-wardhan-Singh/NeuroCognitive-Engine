from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from config.settings import STRONG_MASTERY_THRESHOLD, WEAK_MASTERY_THRESHOLD
from engines.risk_engine.predictor import predict_risk
from orchestrator.utils import datetime_to_unix_timestamp
from services.attempt_service import get_attempts_by_session
from services.user_service import (
    get_concept_attempt_stats,
    get_user_mastery_states,
)


def calculate_accuracy(attempts) -> float:
    total_attempts = len(attempts)
    if total_attempts == 0:
        return 0.0
    correct_attempts = sum(1 for row in attempts if row.correct)
    return correct_attempts / total_attempts


def calculate_streak(attempts) -> int:
    streak = 0
    sorted_attempts = sorted(attempts, key=lambda row: row.timestamp)
    for row in reversed(sorted_attempts):
        if row.correct:
            streak += 1
        else:
            break
    return streak


def get_weak_concepts(user_id: UUID, mastery_rows) -> list[str]:
    _ = user_id
    return [row.concept_id for row in mastery_rows if row.mastery < WEAK_MASTERY_THRESHOLD]


def confidence_trend(attempts) -> float:
    values = [row.reported_confidence for row in attempts]
    if not values:
        return 0.0
    return sum(values) / len(values)


def generate_session_summary(db: Session, user_id: UUID, session_id: UUID):
    now = datetime.utcnow()
    attempts = get_attempts_by_session(db, session_id)
    mastery_rows = get_user_mastery_states(db, user_id)

    accuracy = calculate_accuracy(attempts)
    avg_confidence = confidence_trend(attempts)
    weak_concepts = get_weak_concepts(user_id, mastery_rows)
    strong_concepts = [row.concept_id for row in mastery_rows if row.mastery >= STRONG_MASTERY_THRESHOLD]

    risk_insights = []
    now_unix = datetime_to_unix_timestamp(now)
    for row in mastery_rows:
        stats = get_concept_attempt_stats(db, user_id, row.concept_id)
        concept_data = {
            "concept_id": row.concept_id,
            "mastery": row.mastery,
            "confidence": row.confidence,
            "last_seen_timestamp": datetime_to_unix_timestamp(row.last_seen_timestamp),
            "attempts": stats["attempts"],
            "correct_attempts": stats["correct_attempts"],
        }
        risk = predict_risk(concept_data, now_unix)
        risk_insights.append(
            {
                "concept_id": risk["concept_id"],
                "risk_level": risk["risk_level"],
                "p_error": risk["p_error"],
            }
        )

    return {
        "accuracy": accuracy,
        "avg_confidence": avg_confidence,
        "weak_concepts": weak_concepts,
        "strong_concepts": strong_concepts,
        "risk_insights": risk_insights,
    }

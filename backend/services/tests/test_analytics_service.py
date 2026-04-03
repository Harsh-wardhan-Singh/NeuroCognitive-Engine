from pathlib import Path
from datetime import datetime
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
from db.crud import create_session, create_user
from services.analytics_service import (
    calculate_accuracy,
    calculate_streak,
    confidence_trend,
    generate_session_summary,
)
from services.attempt_service import log_attempt
from services.mastery_service import upsert_mastery_state


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_accuracy_streak_confidence_helpers() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    log_attempt(db, user_id, "math.algebra.linear_equations", "q1", True, 3.1, 0.8)
    log_attempt(db, user_id, "math.algebra.linear_equations", "q2", True, 3.4, 0.7)

    from services.user_service import get_session_attempts

    attempts = get_session_attempts(db, user_id, datetime(2000, 1, 1), datetime(2100, 1, 1))

    expected = {
        "accuracy": 1.0,
        "streak": 2,
        "avg_confidence": 0.75,
    }
    actual = {
        "accuracy": calculate_accuracy(attempts),
        "streak": calculate_streak(attempts),
        "avg_confidence": confidence_trend(attempts),
    }

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_generate_session_summary() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    session = create_session(
        db,
        {
            "user_id": user_id,
            "subject": "math",
            "topic": "algebra",
            "total_questions": 5,
            "questions_answered": 1,
            "current_concept": "math.algebra.linear_equations",
            "is_active": True,
        },
    )

    log_attempt(db, user_id, "math.algebra.linear_equations", "q1", True, 4.0, 0.8)
    upsert_mastery_state(db, user_id, "math.algebra.linear_equations", 0.4, 0.6, datetime.utcnow())

    output = generate_session_summary(db, user_id, session["session_id"])

    expected_keys = {"accuracy", "avg_confidence", "weak_concepts", "strong_concepts", "risk_insights"}
    actual_keys = set(output.keys())

    print("Expected:", expected_keys)
    print("Got:", actual_keys)
    assert actual_keys == expected_keys
    db.close()


def run_all() -> None:
    test_accuracy_streak_confidence_helpers()
    test_generate_session_summary()


if __name__ == "__main__":
    run_all()

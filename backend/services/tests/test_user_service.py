from pathlib import Path
from datetime import datetime
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
from db.crud import create_user, log_attempt, upsert_mastery_state
from services.user_service import (
    get_concept_attempt_stats,
    get_session_attempts,
    get_user_mastery_states,
    get_user_record,
)


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_get_user_record() -> None:
    db = _build_test_session()
    user_id = create_user(db)
    user = get_user_record(db, user_id)

    expected = str(user_id)
    actual = str(user.user_id) if user else None

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_attempt_stats_and_session_attempts() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    log_attempt(
        db,
        {
            "user_id": user_id,
            "concept_id": "math.algebra.linear_equations",
            "question_id": "q_1",
            "correct": True,
            "reported_confidence": 0.9,
            "response_time": 4.5,
        },
    )

    stats = get_concept_attempt_stats(db, user_id, "math.algebra.linear_equations")
    attempts = get_session_attempts(db, user_id, datetime(2000, 1, 1), datetime(2100, 1, 1))

    expected_stats = {"attempts": 1, "correct_attempts": 1}
    actual_stats = stats
    print("Expected:", expected_stats)
    print("Got:", actual_stats)
    assert actual_stats == expected_stats

    expected_attempts = 1
    actual_attempts = len(attempts)
    print("Expected:", expected_attempts)
    print("Got:", actual_attempts)
    assert actual_attempts == expected_attempts
    db.close()


def test_get_user_mastery_states() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    upsert_mastery_state(
        db,
        {
            "user_id": user_id,
            "concept_id": "math.algebra.linear_equations",
            "mastery": 0.62,
            "confidence": 0.57,
            "last_seen_timestamp": datetime.utcnow(),
        },
    )

    rows = get_user_mastery_states(db, user_id)
    expected = 1
    actual = len(rows)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def run_all() -> None:
    test_get_user_record()
    test_attempt_stats_and_session_attempts()
    test_get_user_mastery_states()


if __name__ == "__main__":
    run_all()

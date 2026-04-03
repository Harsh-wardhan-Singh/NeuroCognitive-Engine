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
from db.crud import create_user, get_mastery_state, log_attempt, upsert_mastery_state
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


def run_all() -> None:
    test_create_user_returns_uuid()
    test_log_attempt_inserts_row()
    test_get_mastery_state_returns_3_field_dict()
    test_upsert_mastery_state_updates_existing_row()


if __name__ == "__main__":
    run_all()

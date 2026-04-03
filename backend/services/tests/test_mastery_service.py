from pathlib import Path
from datetime import datetime
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
from db.crud import create_user
from services.mastery_service import get_mastery_state, upsert_mastery_state


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_get_and_upsert_mastery_state() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    upsert_mastery_state(
        db,
        user_id,
        "math.algebra.linear_equations",
        0.65,
        0.55,
        datetime(2026, 4, 4, 10, 0, 0),
    )

    output = get_mastery_state(db, user_id, "math.algebra.linear_equations")
    expected = {
        "mastery": 0.65,
        "confidence": 0.55,
    }
    actual = {
        "mastery": output["mastery"] if output else None,
        "confidence": output["confidence"] if output else None,
    }

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def run_all() -> None:
    test_get_and_upsert_mastery_state()


if __name__ == "__main__":
    run_all()

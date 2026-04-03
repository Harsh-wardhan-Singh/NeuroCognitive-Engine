from pathlib import Path
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
from db.crud import create_user
from orchestrator.session_manager import create_session, get_session, update_session


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_create_get_update_session_manager_flow() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    created = create_session(
        db,
        {
            "user_id": user_id,
            "subject": "math",
            "topic": "algebra",
            "total_questions": 5,
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

    expected_fetched = "math.algebra.linear_equations"
    actual_fetched = fetched["current_concept"] if fetched else None
    print("Expected:", expected_fetched)
    print("Got:", actual_fetched)
    assert actual_fetched == expected_fetched

    expected_updated = {
        "questions_answered": 1,
        "current_concept": "math.algebra.quadratic_equations",
    }
    actual_updated = {
        "questions_answered": updated["questions_answered"] if updated else None,
        "current_concept": updated["current_concept"] if updated else None,
    }
    print("Expected:", expected_updated)
    print("Got:", actual_updated)
    assert actual_updated == expected_updated
    db.close()


def run_all() -> None:
    test_create_get_update_session_manager_flow()


if __name__ == "__main__":
    run_all()

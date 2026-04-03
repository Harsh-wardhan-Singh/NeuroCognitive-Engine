from pathlib import Path
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
from db.crud import create_user
from services.session_service import (
    create_session_record,
    get_last_questions,
    get_session_question_record,
    get_session_record,
    store_session_question,
    update_session_record,
)


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_create_and_get_session_record() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    created = create_session_record(
        db,
        {
            "user_id": user_id,
            "subject": "math",
            "topic": "algebra",
            "total_questions": 6,
            "questions_answered": 0,
            "current_concept": "math.algebra.linear_equations",
            "is_active": True,
        },
    )

    fetched = get_session_record(db, created["session_id"])
    expected = "math.algebra.linear_equations"
    actual = fetched["current_concept"] if fetched else None

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_update_session_record() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    created = create_session_record(
        db,
        {
            "user_id": user_id,
            "subject": "math",
            "topic": "algebra",
            "total_questions": 6,
            "questions_answered": 0,
            "current_concept": "math.algebra.linear_equations",
            "is_active": True,
        },
    )

    updated = update_session_record(
        db,
        created["session_id"],
        {
            "questions_answered": 2,
            "current_concept": "math.algebra.quadratic_equations",
            "is_active": True,
        },
    )

    expected = {
        "questions_answered": 2,
        "current_concept": "math.algebra.quadratic_equations",
    }
    actual = {
        "questions_answered": updated["questions_answered"] if updated else None,
        "current_concept": updated["current_concept"] if updated else None,
    }

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_question_store_and_fetch_and_recent() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    created = create_session_record(
        db,
        {
            "user_id": user_id,
            "subject": "math",
            "topic": "algebra",
            "total_questions": 6,
            "questions_answered": 0,
            "current_concept": "math.algebra.linear_equations",
            "is_active": True,
        },
    )

    store_session_question(
        db,
        {
            "session_id": created["session_id"],
            "question_id": "q_1",
            "concept_id": "math.algebra.linear_equations",
            "question_text": "Solve x + 2 = 5",
            "options": ["1", "2", "3", "4"],
            "correct_option": "3",
            "difficulty_level": "EASY",
        },
    )

    row = get_session_question_record(db, created["session_id"], "q_1")
    expected_correct = "3"
    actual_correct = row.correct_option if row else None

    print("Expected:", expected_correct)
    print("Got:", actual_correct)
    assert actual_correct == expected_correct

    recent = get_last_questions(db, created["session_id"], limit=15)
    expected_recent = ["Solve x + 2 = 5"]

    print("Expected:", expected_recent)
    print("Got:", recent)
    assert recent == expected_recent
    db.close()


def run_all() -> None:
    test_create_and_get_session_record()
    test_update_session_record()
    test_question_store_and_fetch_and_recent()


if __name__ == "__main__":
    run_all()

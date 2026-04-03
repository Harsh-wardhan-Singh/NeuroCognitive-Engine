from pathlib import Path
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
from db.crud import create_session, create_session_question, create_user
from services.attempt_service import get_attempts_by_session, get_concept_attempt_stats, log_attempt


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_log_attempt_and_stats() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    log_attempt(
        db,
        user_id,
        "math.algebra.linear_equations",
        "q-1",
        True,
        4.0,
        0.8,
    )

    output = get_concept_attempt_stats(db, user_id, "math.algebra.linear_equations")
    expected = {"attempts": 1, "correct_attempts": 1}

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected
    db.close()


def test_get_attempts_by_session_join() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    session = create_session(
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

    create_session_question(
        db,
        {
            "session_id": session["session_id"],
            "question_id": "q-join-1",
            "concept_id": "math.algebra.linear_equations",
            "question_text": "Solve x + 2 = 5",
            "options": ["1", "2", "3", "4"],
            "correct_option": "3",
            "difficulty_level": "EASY",
        },
    )

    log_attempt(
        db,
        user_id,
        "math.algebra.linear_equations",
        "q-join-1",
        True,
        3.5,
        0.7,
    )

    rows = get_attempts_by_session(db, session["session_id"])
    expected = 1
    actual = len(rows)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def run_all() -> None:
    test_log_attempt_and_stats()
    test_get_attempts_by_session_join()


if __name__ == "__main__":
    run_all()

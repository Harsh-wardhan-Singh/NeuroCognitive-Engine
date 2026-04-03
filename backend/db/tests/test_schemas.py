from pathlib import Path
from datetime import datetime
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from db.schemas import (
    AttemptCreate,
    AuthUserCreate,
    MasteryStateRead,
    MasteryUpdate,
    SessionCreate,
    SessionQuestionCreate,
    SessionUpdate,
    UserCreate,
)


def test_user_create_is_empty_schema() -> None:
    output = UserCreate().model_dump()
    expected = {}

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_attempt_create_schema_fields() -> None:
    user_id = uuid.uuid4()
    schema = AttemptCreate(
        user_id=user_id,
        concept_id="probability_basics",
        question_id="q1",
        correct=True,
        reported_confidence=0.75,
        response_time=12.4,
    )

    expected = {
        "user_id": user_id,
        "concept_id": "probability_basics",
        "question_id": "q1",
        "correct": True,
        "reported_confidence": 0.75,
        "response_time": 12.4,
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_mastery_update_schema_fields() -> None:
    user_id = uuid.uuid4()
    ts = datetime(2026, 4, 3, 10, 0, 0)
    schema = MasteryUpdate(
        user_id=user_id,
        concept_id="probability_basics",
        mastery=0.62,
        confidence=0.58,
        last_seen_timestamp=ts,
    )

    expected = {
        "user_id": user_id,
        "concept_id": "probability_basics",
        "mastery": 0.62,
        "confidence": 0.58,
        "last_seen_timestamp": ts,
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_mastery_state_read_schema_fields() -> None:
    ts = datetime(2026, 4, 3, 11, 0, 0)
    schema = MasteryStateRead(
        mastery=0.81,
        confidence=0.67,
        last_seen_timestamp=ts,
    )

    expected = {
        "mastery": 0.81,
        "confidence": 0.67,
        "last_seen_timestamp": ts,
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_auth_user_create_schema_fields() -> None:
    schema = AuthUserCreate(email="test@example.com", password_hash="hashed")
    expected = {"email": "test@example.com", "password_hash": "hashed"}
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_session_create_schema_fields() -> None:
    user_id = uuid.uuid4()
    schema = SessionCreate(
        user_id=user_id,
        subject="math",
        topic="algebra",
        total_questions=10,
        questions_answered=0,
        current_concept="math.algebra.linear_equations",
        is_active=True,
    )
    expected = {
        "user_id": user_id,
        "subject": "math",
        "topic": "algebra",
        "total_questions": 10,
        "questions_answered": 0,
        "current_concept": "math.algebra.linear_equations",
        "is_active": True,
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_session_update_schema_fields() -> None:
    schema = SessionUpdate(
        questions_answered=5,
        current_concept="math.algebra.quadratic_equations",
        is_active=False,
    )
    expected = {
        "questions_answered": 5,
        "current_concept": "math.algebra.quadratic_equations",
        "is_active": False,
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_session_question_create_schema_fields() -> None:
    session_id = uuid.uuid4()
    schema = SessionQuestionCreate(
        session_id=session_id,
        question_id="q_1",
        concept_id="math.algebra.linear_equations",
        question_text="Solve x + 2 = 5",
        options=["1", "2", "3", "4"],
        correct_option="3",
        difficulty_level="EASY",
    )
    expected = {
        "session_id": session_id,
        "question_id": "q_1",
        "concept_id": "math.algebra.linear_equations",
        "question_text": "Solve x + 2 = 5",
        "options": ["1", "2", "3", "4"],
        "correct_option": "3",
        "difficulty_level": "EASY",
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def run_all() -> None:
    test_user_create_is_empty_schema()
    test_attempt_create_schema_fields()
    test_mastery_update_schema_fields()
    test_mastery_state_read_schema_fields()
    test_auth_user_create_schema_fields()
    test_session_create_schema_fields()
    test_session_update_schema_fields()
    test_session_question_create_schema_fields()


if __name__ == "__main__":
    run_all()

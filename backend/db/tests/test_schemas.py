from pathlib import Path
from datetime import datetime
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from db.schemas import AttemptCreate, MasteryStateRead, MasteryUpdate, UserCreate


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


def run_all() -> None:
    test_user_create_is_empty_schema()
    test_attempt_create_schema_fields()
    test_mastery_update_schema_fields()
    test_mastery_state_read_schema_fields()


if __name__ == "__main__":
    run_all()

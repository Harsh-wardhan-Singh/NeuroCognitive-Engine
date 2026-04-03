from pathlib import Path
from datetime import datetime
import os
import sys

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from db.database import Base
from db.models import User


def test_table_names_exist() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    expected = {"users", "attempts", "mastery_state"}
    actual = set(inspect(engine).get_table_names())

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def test_attempt_has_correct_column_name() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    columns = {column["name"] for column in inspect(engine).get_columns("attempts")}
    expected = True
    actual = "correct" in columns and "correctness" not in columns

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def test_mastery_state_has_composite_key() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    pk = inspect(engine).get_pk_constraint("mastery_state")
    expected = {"user_id", "concept_id"}
    actual = set(pk.get("constrained_columns", []))

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def test_user_id_is_uuid_instance() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    user = User(created_at=datetime.utcnow())
    db.add(user)
    db.commit()
    db.refresh(user)

    expected = "UUID"
    actual = type(user.user_id).__name__

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def run_all() -> None:
    test_table_names_exist()
    test_attempt_has_correct_column_name()
    test_mastery_state_has_composite_key()
    test_user_id_is_uuid_instance()


if __name__ == "__main__":
    run_all()

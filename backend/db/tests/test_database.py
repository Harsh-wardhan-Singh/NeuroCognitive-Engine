from pathlib import Path
import importlib
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def _reload_database_module_with_env(database_url):
    if database_url is None:
        os.environ["DATABASE_URL"] = ""
    else:
        os.environ["DATABASE_URL"] = database_url

    if "db.database" in sys.modules:
        del sys.modules["db.database"]

    return importlib.import_module("db.database")


def test_database_url_is_required():
    expected_error = "DATABASE_URL environment variable is required"
    actual_error = None

    try:
        _reload_database_module_with_env(None)
    except ValueError as exc:
        actual_error = str(exc)

    print("Expected:", expected_error)
    print("Got:", actual_error)
    assert actual_error == expected_error


def test_engine_and_session_creation():
    module = _reload_database_module_with_env("sqlite:///:memory:")

    expected_engine_exists = True
    actual_engine_exists = module.engine is not None

    expected_session_type = "Session"
    session = module.SessionLocal()
    actual_session_type = type(session).__name__
    session.close()

    print("Expected:", expected_engine_exists)
    print("Got:", actual_engine_exists)
    print("Expected:", expected_session_type)
    print("Got:", actual_session_type)

    assert actual_engine_exists == expected_engine_exists
    assert actual_session_type == expected_session_type


def test_get_db_yields_session_object():
    module = _reload_database_module_with_env("sqlite:///:memory:")

    expected_session_type = "Session"
    db_generator = module.get_db()
    session = next(db_generator)
    actual_session_type = type(session).__name__

    print("Expected:", expected_session_type)
    print("Got:", actual_session_type)

    assert actual_session_type == expected_session_type
    db_generator.close()


def run_all() -> None:
    test_database_url_is_required()
    test_engine_and_session_creation()
    test_get_db_yields_session_object()


if __name__ == "__main__":
    run_all()

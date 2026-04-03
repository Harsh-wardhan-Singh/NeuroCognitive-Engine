from pathlib import Path
import importlib
import os
import sys

from sqlalchemy import inspect

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def test_init_db_creates_all_tables() -> None:
    db_file = Path(__file__).resolve().parent / "init_db_test.sqlite"
    if db_file.exists():
        db_file.unlink()

    os.environ["DATABASE_URL"] = f"sqlite:///{db_file.as_posix()}"

    for module_name in ["db.database", "db.models", "db.init_db"]:
        if module_name in sys.modules:
            del sys.modules[module_name]

    database_module = importlib.import_module("db.database")
    importlib.import_module("db.models")
    init_db_module = importlib.import_module("db.init_db")

    init_db_module.init_db()

    expected = {"users", "attempts", "mastery_state"}
    actual = set(inspect(database_module.engine).get_table_names())

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected

    database_module.engine.dispose()
    if db_file.exists():
        db_file.unlink()


def run_all() -> None:
    test_init_db_creates_all_tables()


if __name__ == "__main__":
    run_all()

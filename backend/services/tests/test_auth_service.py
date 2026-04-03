from pathlib import Path
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret"

import db.database as database_module
from services.auth_service import (
    get_user_id_from_token,
    login,
    require_authenticated_user,
    revoke_token,
    signup,
)


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_signup_creates_user() -> None:
    db = _build_test_session()
    output = signup(db, "auth_user@example.com", "pass1234")

    expected = "auth_user@example.com"
    actual = output["email"]

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_login_returns_jwt_token() -> None:
    db = _build_test_session()
    created = signup(db, "login_user@example.com", "pass1234")
    output = login(db, "login_user@example.com", "pass1234")

    token = output["token"]
    decoded_user_id = get_user_id_from_token(token)

    expected = str(created["user_id"])
    actual = str(decoded_user_id)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_require_authenticated_user_returns_db_user() -> None:
    db = _build_test_session()
    created = signup(db, "jwt_user@example.com", "pass1234")
    token = login(db, "jwt_user@example.com", "pass1234")["token"]

    user = require_authenticated_user(db, token)

    expected = str(created["user_id"])
    actual = str(user.user_id)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_signup_rejects_weak_password() -> None:
    db = _build_test_session()
    expected = "Password must include at least one number"
    actual = None

    try:
        signup(db, "weak@example.com", "password")
    except ValueError as error:
        actual = str(error)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def test_revoked_token_is_rejected() -> None:
    db = _build_test_session()
    signup(db, "revoke@example.com", "pass1234")
    token = login(db, "revoke@example.com", "pass1234")["token"]
    revoke_token(token)

    expected = "Token revoked"
    actual = None
    try:
        get_user_id_from_token(token)
    except ValueError as error:
        actual = str(error)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    db.close()


def run_all() -> None:
    test_signup_creates_user()
    test_login_returns_jwt_token()
    test_require_authenticated_user_returns_db_user()
    test_signup_rejects_weak_password()
    test_revoked_token_is_rejected()


if __name__ == "__main__":
    run_all()

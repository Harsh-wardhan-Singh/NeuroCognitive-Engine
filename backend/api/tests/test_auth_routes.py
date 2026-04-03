from pathlib import Path
import os
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "this-is-a-secure-test-secret-with-length-32"

import db.database as database_module
from api.deps import get_db_session
from api.routes.auth import router as auth_router


def _build_test_app_and_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    app = FastAPI()
    app.include_router(auth_router)

    def _override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db_session] = _override_get_db
    return app


def test_signup_and_login_routes() -> None:
    app = _build_test_app_and_db()
    client = TestClient(app)

    signup_response = client.post(
        "/auth/signup",
        json={"email": "route_user@example.com", "password": "pass1234"},
    )
    login_response = client.post(
        "/auth/login",
        json={"email": "route_user@example.com", "password": "pass1234"},
    )

    expected_signup = 200
    actual_signup = signup_response.status_code

    print("Expected:", expected_signup)
    print("Got:", actual_signup)
    assert actual_signup == expected_signup

    expected_login = 200
    actual_login = login_response.status_code

    print("Expected:", expected_login)
    print("Got:", actual_login)
    assert actual_login == expected_login

    expected_token_present = True
    actual_token_present = "token" in login_response.json()

    print("Expected:", expected_token_present)
    print("Got:", actual_token_present)
    assert actual_token_present == expected_token_present


def run_all() -> None:
    test_signup_and_login_routes()


if __name__ == "__main__":
    run_all()

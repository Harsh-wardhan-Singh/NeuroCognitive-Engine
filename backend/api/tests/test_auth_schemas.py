from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from schemas.auth_schemas import LoginRequest, LoginResponse, SignupRequest, SignupResponse


def test_signup_request_schema() -> None:
    schema = SignupRequest(email="a@example.com", password="pass123")
    expected = {"email": "a@example.com", "password": "pass123"}
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_login_response_schema() -> None:
    schema = LoginResponse(token="jwt-token")
    expected = {"token": "jwt-token"}
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_signup_response_schema() -> None:
    user_id = uuid.uuid4()
    schema = SignupResponse(user_id=user_id, email="a@example.com")
    expected = {"user_id": user_id, "email": "a@example.com"}
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def run_all() -> None:
    test_signup_request_schema()
    test_login_response_schema()
    test_signup_response_schema()


if __name__ == "__main__":
    run_all()

from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["JWT_SECRET_KEY"] = "this-is-a-secure-test-secret-with-length-32"

from services.auth_service import create_access_token
from api.deps import get_current_user_id
from fastapi.security import HTTPAuthorizationCredentials
from uuid import uuid4


def test_get_current_user_id_from_bearer_token() -> None:
    user_id = uuid4()
    token = create_access_token(user_id)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    output = get_current_user_id(credentials)

    expected = str(user_id)
    actual = str(output)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def run_all() -> None:
    test_get_current_user_id_from_bearer_token()


if __name__ == "__main__":
    run_all()

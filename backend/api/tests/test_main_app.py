from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from api.main import app


def test_app_includes_auth_and_quiz_routes() -> None:
    paths = {route.path for route in app.routes}
    expected = {"/auth/signup", "/auth/login", "/start-session", "/submit-answer", "/end-session/{session_id}"}
    actual = expected & paths

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def run_all() -> None:
    test_app_includes_auth_and_quiz_routes()


if __name__ == "__main__":
    run_all()

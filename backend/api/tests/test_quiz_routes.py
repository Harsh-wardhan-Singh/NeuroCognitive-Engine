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
import orchestrator.quiz_orchestrator as quiz_orchestrator
from api.deps import get_db_session
from api.routes.auth import router as auth_router
from api.routes.quiz import router as quiz_router


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
    app.include_router(quiz_router)

    def _override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db_session] = _override_get_db
    return app


def test_protected_quiz_flow_routes() -> None:
    app = _build_test_app_and_db()
    client = TestClient(app)

    original_generate_question = quiz_orchestrator.generate_question
    original_generate_explanation = quiz_orchestrator.generate_explanation

    state = {"calls": 0}

    def _mock_generate_question(concept, difficulty, previous_questions):
        _ = previous_questions
        state["calls"] += 1
        if state["calls"] == 1:
            return {
                "question": "Solve x + 2 = 5",
                "options": ["1", "2", "3", "4"],
                "correct_answer": "3",
            }
        return {
            "question": "Solve x + 1 = 2",
            "options": ["0", "1", "2", "3"],
            "correct_answer": "1",
        }

    def _mock_generate_explanation(question, correct_answer):
        return {"explanation": "mock explanation"}

    quiz_orchestrator.generate_question = _mock_generate_question
    quiz_orchestrator.generate_explanation = _mock_generate_explanation

    signup_res = client.post("/auth/signup", json={"email": "quiz@example.com", "password": "pass1234"})
    login_res = client.post("/auth/login", json={"email": "quiz@example.com", "password": "pass1234"})

    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post(
        "/start-session",
        json={"subject": "math", "topic": "algebra", "num_questions": 5},
        headers=headers,
    )
    start_data = start_res.json()

    submit_res = client.post(
        "/submit-answer",
        json={
            "session_id": start_data["session_id"],
            "question_id": start_data["question"]["question_id"],
            "selected_option": "3",
            "reported_confidence": 0.8,
            "response_time": 4.1,
        },
        headers=headers,
    )

    end_res = client.get(f"/end-session/{start_data['session_id']}", headers=headers)

    expected = {"signup": 200, "login": 200, "start": 200, "submit": 200, "end": 200}
    actual = {
        "signup": signup_res.status_code,
        "login": login_res.status_code,
        "start": start_res.status_code,
        "submit": submit_res.status_code,
        "end": end_res.status_code,
    }

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected

    expected_correct = True
    actual_correct = submit_res.json()["correct"]

    print("Expected:", expected_correct)
    print("Got:", actual_correct)
    assert actual_correct == expected_correct

    quiz_orchestrator.generate_question = original_generate_question
    quiz_orchestrator.generate_explanation = original_generate_explanation


def run_all() -> None:
    test_protected_quiz_flow_routes()


if __name__ == "__main__":
    run_all()

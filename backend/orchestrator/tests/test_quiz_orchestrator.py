from pathlib import Path
from uuid import UUID
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import db.database as database_module
import orchestrator.quiz_orchestrator as quiz_orchestrator
from db.crud import create_user


def _build_test_session():
    engine = create_engine("sqlite:///:memory:")
    database_module.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_start_session_returns_first_question() -> None:
    db = _build_test_session()
    user_id = create_user(db)

    original_generate_question = quiz_orchestrator.generate_question

    def _mock_generate_question(concept, difficulty, previous_questions):
        _ = previous_questions
        return {
            "question": "Solve x + 2 = 5",
            "options": ["1", "2", "3", "4"],
            "correct_answer": "3",
        }

    quiz_orchestrator.generate_question = _mock_generate_question

    output = quiz_orchestrator.start_session(db, user_id, "math", "algebra", 5)
    expected_question_text = "Solve x + 2 = 5"
    actual_question_text = output["question"]["text"]

    print("Expected:", expected_question_text)
    print("Got:", actual_question_text)
    assert actual_question_text == expected_question_text
    assert isinstance(output["session_id"], UUID)

    quiz_orchestrator.generate_question = original_generate_question
    db.close()


def test_submit_answer_computes_correctness_from_db_question() -> None:
    db = _build_test_session()
    user_id = create_user(db)

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
        return {"explanation": f"Correct answer is {correct_answer}"}

    quiz_orchestrator.generate_question = _mock_generate_question
    quiz_orchestrator.generate_explanation = _mock_generate_explanation

    started = quiz_orchestrator.start_session(db, user_id, "math", "algebra", 5)
    output = quiz_orchestrator.submit_answer(
        db,
        user_id,
        started["session_id"],
        started["question"]["question_id"],
        "3",
        0.8,
        4.0,
    )

    expected = {"correct": True, "is_session_complete": False}
    actual = {"correct": output["correct"], "is_session_complete": output["is_session_complete"]}

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected
    assert output["next_question"] is not None

    quiz_orchestrator.generate_question = original_generate_question
    quiz_orchestrator.generate_explanation = original_generate_explanation
    db.close()


def test_end_session_returns_summary() -> None:
    db = _build_test_session()
    user_id = create_user(db)

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
            "question": "Solve x + 3 = 6",
            "options": ["1", "2", "3", "4"],
            "correct_answer": "3",
        }

    def _mock_generate_explanation(question, correct_answer):
        return {"explanation": "explanation"}

    quiz_orchestrator.generate_question = _mock_generate_question
    quiz_orchestrator.generate_explanation = _mock_generate_explanation

    started = quiz_orchestrator.start_session(db, user_id, "math", "algebra", 5)
    quiz_orchestrator.submit_answer(
        db,
        user_id,
        started["session_id"],
        started["question"]["question_id"],
        "3",
        0.8,
        4.0,
    )

    summary_output = quiz_orchestrator.end_session(db, user_id, started["session_id"])
    expected_keys = {"accuracy", "avg_confidence", "weak_concepts", "strong_concepts", "risk_insights"}
    actual_keys = set(summary_output["summary"].keys())

    print("Expected:", expected_keys)
    print("Got:", actual_keys)
    assert actual_keys == expected_keys

    quiz_orchestrator.generate_question = original_generate_question
    quiz_orchestrator.generate_explanation = original_generate_explanation
    db.close()


def run_all() -> None:
    test_start_session_returns_first_question()
    test_submit_answer_computes_correctness_from_db_question()
    test_end_session_returns_summary()


if __name__ == "__main__":
    run_all()

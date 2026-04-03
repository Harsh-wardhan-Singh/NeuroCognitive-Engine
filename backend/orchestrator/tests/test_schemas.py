from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from orchestrator.schemas import QuestionResponse, SessionSummary, StartSessionRequest, SubmitAnswerRequest


def test_start_session_request_schema() -> None:
    schema = StartSessionRequest(subject="math", topic="algebra", num_questions=10)
    expected = {"subject": "math", "topic": "algebra", "num_questions": 10}
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_submit_answer_request_schema() -> None:
    session_id = uuid.uuid4()
    schema = SubmitAnswerRequest(
        session_id=session_id,
        question_id="q_1",
        selected_option="B",
        reported_confidence=0.75,
        response_time=4.2,
    )
    expected = {
        "session_id": session_id,
        "question_id": "q_1",
        "selected_option": "B",
        "reported_confidence": 0.75,
        "response_time": 4.2,
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_question_response_schema() -> None:
    schema = QuestionResponse(
        question_id="q_1",
        text="Solve x + 2 = 5",
        options=["1", "2", "3", "4"],
    )
    expected = {
        "question_id": "q_1",
        "text": "Solve x + 2 = 5",
        "options": ["1", "2", "3", "4"],
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_session_summary_schema() -> None:
    schema = SessionSummary(
        accuracy=0.7,
        avg_confidence=0.65,
        weak_concepts=["math.algebra.linear_equations"],
        strong_concepts=["math.algebra.quadratic_equations"],
        risk_insights=[{"concept_id": "math.algebra.linear_equations", "risk_level": "HIGH"}],
    )
    expected = {
        "accuracy": 0.7,
        "avg_confidence": 0.65,
        "weak_concepts": ["math.algebra.linear_equations"],
        "strong_concepts": ["math.algebra.quadratic_equations"],
        "risk_insights": [{"concept_id": "math.algebra.linear_equations", "risk_level": "HIGH"}],
    }
    output = schema.model_dump()

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def run_all() -> None:
    test_start_session_request_schema()
    test_submit_answer_request_schema()
    test_question_response_schema()
    test_session_summary_schema()


if __name__ == "__main__":
    run_all()

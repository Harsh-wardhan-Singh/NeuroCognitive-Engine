from uuid import UUID

from pydantic import BaseModel


class StartSessionRequest(BaseModel):
    subject: str
    topic: str
    num_questions: int


class SubmitAnswerRequest(BaseModel):
    session_id: UUID
    question_id: str
    selected_option: str
    reported_confidence: float
    response_time: float


class QuestionResponse(BaseModel):
    question_id: str
    text: str
    options: list[str]


class SessionSummary(BaseModel):
    accuracy: float
    avg_confidence: float
    weak_concepts: list[str]
    strong_concepts: list[str]
    risk_insights: list[dict]

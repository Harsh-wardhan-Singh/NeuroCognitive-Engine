from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
	pass


class AuthUserCreate(BaseModel):
	email: str
	password_hash: str


class AuthUserRead(BaseModel):
	user_id: UUID
	email: str
	created_at: datetime


class AttemptCreate(BaseModel):
	user_id: UUID
	concept_id: str
	question_id: str
	correct: bool
	reported_confidence: float
	response_time: float


class MasteryUpdate(BaseModel):
	user_id: UUID
	concept_id: str
	mastery: float
	confidence: float
	last_seen_timestamp: datetime


class MasteryStateRead(BaseModel):
	mastery: float
	confidence: float
	last_seen_timestamp: datetime


class SessionCreate(BaseModel):
	user_id: UUID
	subject: str
	topic: str
	total_questions: int
	questions_answered: int
	current_concept: str
	is_active: bool


class SessionUpdate(BaseModel):
	questions_answered: int
	current_concept: str
	is_active: bool


class SessionRead(BaseModel):
	session_id: UUID
	user_id: UUID
	subject: str
	topic: str
	total_questions: int
	questions_answered: int
	current_concept: str
	started_at: datetime
	updated_at: datetime
	is_active: bool


class SessionQuestionCreate(BaseModel):
	session_id: UUID
	question_id: str
	concept_id: str
	question_text: str
	options: list[str]
	correct_option: str
	difficulty_level: str | None = None


class SessionQuestionRead(BaseModel):
	id: int
	session_id: UUID
	question_id: str
	concept_id: str
	question_text: str
	options: list[str]
	correct_option: str
	difficulty_level: str | None = None
	created_at: datetime

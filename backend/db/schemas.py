from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
	pass


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

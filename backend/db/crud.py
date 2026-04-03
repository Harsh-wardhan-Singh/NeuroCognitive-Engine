from uuid import UUID

from sqlalchemy.orm import Session

from db.models import Attempt, MasteryState, User
from db.schemas import AttemptCreate, MasteryStateRead, MasteryUpdate


def create_user(db: Session):
	user = User()
	db.add(user)
	db.commit()
	db.refresh(user)
	return user.user_id


def log_attempt(db: Session, attempt_data):
	if isinstance(attempt_data, AttemptCreate):
		data = attempt_data.model_dump()
	elif isinstance(attempt_data, dict):
		data = AttemptCreate(**attempt_data).model_dump()
	else:
		raise TypeError("attempt_data must be AttemptCreate or dict")

	attempt = Attempt(
		user_id=data["user_id"],
		concept_id=data["concept_id"],
		question_id=data["question_id"],
		correct=data["correct"],
		reported_confidence=data["reported_confidence"],
		response_time=data["response_time"],
	)

	db.add(attempt)
	db.commit()
	db.refresh(attempt)


def get_mastery_state(db: Session, user_id: UUID, concept_id: str):
	state = (
		db.query(MasteryState)
		.filter(MasteryState.user_id == user_id, MasteryState.concept_id == concept_id)
		.first()
	)
	if state is None:
		return None

	return MasteryStateRead(
		mastery=state.mastery,
		confidence=state.confidence,
		last_seen_timestamp=state.last_seen_timestamp,
	).model_dump()


def upsert_mastery_state(db: Session, data):
	if isinstance(data, MasteryUpdate):
		payload = data.model_dump()
	elif isinstance(data, dict):
		payload = MasteryUpdate(**data).model_dump()
	else:
		raise TypeError("data must be MasteryUpdate or dict")

	existing = (
		db.query(MasteryState)
		.filter(
			MasteryState.user_id == payload["user_id"],
			MasteryState.concept_id == payload["concept_id"],
		)
		.first()
	)

	if existing:
		existing.mastery = payload["mastery"]
		existing.confidence = payload["confidence"]
		existing.last_seen_timestamp = payload["last_seen_timestamp"]
	else:
		db.add(
			MasteryState(
				user_id=payload["user_id"],
				concept_id=payload["concept_id"],
				mastery=payload["mastery"],
				confidence=payload["confidence"],
				last_seen_timestamp=payload["last_seen_timestamp"],
			)
		)

	db.commit()

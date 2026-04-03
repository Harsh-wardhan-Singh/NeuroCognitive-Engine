from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from db.models import Attempt, MasteryState, Session as SessionModel, SessionQuestion, User
from db.schemas import (
	AttemptCreate,
	AuthUserCreate,
	MasteryStateRead,
	MasteryUpdate,
	SessionCreate,
	SessionQuestionCreate,
	SessionRead,
	SessionUpdate,
)


def create_user(db: Session):
	user = User()
	db.add(user)
	db.commit()
	db.refresh(user)
	return user.user_id


def create_auth_user(db: Session, data):
	if isinstance(data, AuthUserCreate):
		payload = data.model_dump()
	elif isinstance(data, dict):
		payload = AuthUserCreate(**data).model_dump()
	else:
		raise TypeError("data must be AuthUserCreate or dict")

	user = User(
		email=payload["email"],
		password_hash=payload["password_hash"],
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


def get_user_by_email(db: Session, email: str):
	return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID):
	return db.query(User).filter(User.user_id == user_id).first()


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


def create_session(db: Session, data):
	if isinstance(data, SessionCreate):
		payload = data.model_dump()
	elif isinstance(data, dict):
		payload = SessionCreate(**data).model_dump()
	else:
		raise TypeError("data must be SessionCreate or dict")

	session = SessionModel(
		user_id=payload["user_id"],
		subject=payload["subject"],
		topic=payload["topic"],
		total_questions=payload["total_questions"],
		questions_answered=payload["questions_answered"],
		current_concept=payload["current_concept"],
		is_active=payload["is_active"],
	)
	db.add(session)
	db.commit()
	db.refresh(session)
	return SessionRead(
		session_id=session.session_id,
		user_id=session.user_id,
		subject=session.subject,
		topic=session.topic,
		total_questions=session.total_questions,
		questions_answered=session.questions_answered,
		current_concept=session.current_concept,
		started_at=session.started_at,
		updated_at=session.updated_at,
		is_active=session.is_active,
	).model_dump()


def get_session(db: Session, session_id: UUID):
	session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
	if session is None:
		return None
	return SessionRead(
		session_id=session.session_id,
		user_id=session.user_id,
		subject=session.subject,
		topic=session.topic,
		total_questions=session.total_questions,
		questions_answered=session.questions_answered,
		current_concept=session.current_concept,
		started_at=session.started_at,
		updated_at=session.updated_at,
		is_active=session.is_active,
	).model_dump()


def update_session(db: Session, session_id: UUID, data):
	if isinstance(data, SessionUpdate):
		payload = data.model_dump()
	elif isinstance(data, dict):
		payload = SessionUpdate(**data).model_dump()
	else:
		raise TypeError("data must be SessionUpdate or dict")

	session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
	if session is None:
		return None

	session.questions_answered = payload["questions_answered"]
	session.current_concept = payload["current_concept"]
	session.is_active = payload["is_active"]
	session.updated_at = datetime.utcnow()
	db.commit()
	db.refresh(session)

	return SessionRead(
		session_id=session.session_id,
		user_id=session.user_id,
		subject=session.subject,
		topic=session.topic,
		total_questions=session.total_questions,
		questions_answered=session.questions_answered,
		current_concept=session.current_concept,
		started_at=session.started_at,
		updated_at=session.updated_at,
		is_active=session.is_active,
	).model_dump()


def create_session_question(db: Session, data):
	if isinstance(data, SessionQuestionCreate):
		payload = data.model_dump()
	elif isinstance(data, dict):
		payload = SessionQuestionCreate(**data).model_dump()
	else:
		raise TypeError("data must be SessionQuestionCreate or dict")

	row = SessionQuestion(
		session_id=payload["session_id"],
		question_id=payload["question_id"],
		concept_id=payload["concept_id"],
		question_text=payload["question_text"],
		options=payload["options"],
		correct_option=payload["correct_option"],
		difficulty_level=payload["difficulty_level"],
	)
	db.add(row)
	db.commit()
	db.refresh(row)
	return row


def get_session_question(db: Session, session_id: UUID, question_id: str):
	return (
		db.query(SessionQuestion)
		.filter(SessionQuestion.session_id == session_id, SessionQuestion.question_id == question_id)
		.first()
	)


def get_recent_session_questions(db: Session, session_id: UUID, limit: int = 15):
	rows = (
		db.query(SessionQuestion)
		.filter(SessionQuestion.session_id == session_id)
		.order_by(SessionQuestion.created_at.desc())
		.limit(limit)
		.all()
	)
	return [row.question_text for row in rows]


def get_attempt_stats_for_concept(db: Session, user_id: UUID, concept_id: str):
	attempt_rows = db.query(Attempt).filter(Attempt.user_id == user_id, Attempt.concept_id == concept_id).all()
	attempts = len(attempt_rows)
	correct_attempts = sum(1 for row in attempt_rows if row.correct)
	return {
		"attempts": attempts,
		"correct_attempts": correct_attempts,
	}


def list_attempts_for_session_window(db: Session, user_id: UUID, started_at: datetime, ended_at: datetime):
	return (
		db.query(Attempt)
		.filter(Attempt.user_id == user_id, Attempt.timestamp >= started_at, Attempt.timestamp <= ended_at)
		.all()
	)


def list_mastery_states_for_user(db: Session, user_id: UUID):
	return db.query(MasteryState).filter(MasteryState.user_id == user_id).all()

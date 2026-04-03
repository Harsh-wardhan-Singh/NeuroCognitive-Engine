from uuid import UUID

from sqlalchemy.orm import Session

from db.crud import (
	create_session,
	create_session_question,
	get_recent_session_questions,
	get_session,
	get_session_question,
	update_session,
)


def create_session_record(db: Session, data: dict):
	return create_session(db, data)


def update_session_record(db: Session, session_id: UUID, data: dict):
	return update_session(db, session_id, data)


def get_session_record(db: Session, session_id: UUID):
	return get_session(db, session_id)


def store_session_question(db: Session, data: dict):
	return create_session_question(db, data)


def get_session_question_record(db: Session, session_id: UUID, question_id: str):
	return get_session_question(db, session_id, question_id)


def get_last_questions(db: Session, session_id: UUID, limit: int = 15):
	return get_recent_session_questions(db, session_id, limit)

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from db.crud import (
	get_attempt_stats_for_concept,
	get_user_by_id,
	list_attempts_for_session_window,
	list_mastery_states_for_user,
)


def get_user_record(db: Session, user_id: UUID):
	return get_user_by_id(db, user_id)


def get_concept_attempt_stats(db: Session, user_id: UUID, concept_id: str):
	return get_attempt_stats_for_concept(db, user_id, concept_id)


def get_session_attempts(db: Session, user_id: UUID, started_at: datetime, ended_at: datetime):
	return list_attempts_for_session_window(db, user_id, started_at, ended_at)


def get_user_mastery_states(db: Session, user_id: UUID):
	return list_mastery_states_for_user(db, user_id)

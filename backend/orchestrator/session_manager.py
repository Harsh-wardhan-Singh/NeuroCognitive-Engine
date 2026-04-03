from uuid import UUID

from sqlalchemy.orm import Session

from services.session_service import create_session_record, get_session_record, update_session_record


def create_session(db: Session, data: dict):
    return create_session_record(db, data)


def update_session(db: Session, session_id: UUID, data: dict):
    return update_session_record(db, session_id, data)


def get_session(db: Session, session_id: UUID):
    return get_session_record(db, session_id)

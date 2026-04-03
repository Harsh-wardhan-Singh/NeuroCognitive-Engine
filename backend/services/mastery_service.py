from uuid import UUID

from sqlalchemy.orm import Session

from db.crud import get_mastery_state as crud_get_mastery_state
from db.crud import upsert_mastery_state as crud_upsert_mastery_state


def get_mastery_state(db: Session, user_id: UUID, concept_id: str):
    return crud_get_mastery_state(db, user_id, concept_id)


def upsert_mastery_state(
    db: Session,
    user_id: UUID,
    concept_id: str,
    mastery: float,
    confidence: float,
    last_seen_timestamp,
):
    payload = {
        "user_id": user_id,
        "concept_id": concept_id,
        "mastery": mastery,
        "confidence": confidence,
        "last_seen_timestamp": last_seen_timestamp,
    }
    return crud_upsert_mastery_state(db, payload)

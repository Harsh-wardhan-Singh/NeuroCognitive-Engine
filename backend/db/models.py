from datetime import datetime
import uuid
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, PrimaryKeyConstraint, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
class User(Base):
	__tablename__ = "users"

	user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
class Attempt(Base):
	__tablename__ = "attempts"

	attempt_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.user_id"), nullable=False)
	concept_id: Mapped[str] = mapped_column(String, nullable=False)
	question_id: Mapped[str] = mapped_column(String, nullable=False)
	correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
	reported_confidence: Mapped[float] = mapped_column(Float, nullable=False)
	response_time: Mapped[float] = mapped_column(Float, nullable=False)
	timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
class MasteryState(Base):
	__tablename__ = "mastery_state"
	__table_args__ = (
		PrimaryKeyConstraint("user_id", "concept_id", name="pk_mastery_state_user_concept"),
	)
	user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.user_id"), nullable=False)
	concept_id: Mapped[str] = mapped_column(String, nullable=False)
	mastery: Mapped[float] = mapped_column(Float, nullable=False)
	confidence: Mapped[float] = mapped_column(Float, nullable=False)
	last_seen_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

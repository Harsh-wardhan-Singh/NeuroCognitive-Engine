from datetime import datetime
import uuid
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, PrimaryKeyConstraint, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class User(Base):
	__tablename__ = "users"

	user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, nullable=False)
	email: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
	password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
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


class Session(Base):
	__tablename__ = "sessions"

	session_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, nullable=False)
	user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.user_id"), nullable=False)
	subject: Mapped[str] = mapped_column(String, nullable=False)
	topic: Mapped[str] = mapped_column(String, nullable=False)
	total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
	questions_answered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
	current_concept: Mapped[str] = mapped_column(String, nullable=False)
	started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class SessionQuestion(Base):
	__tablename__ = "session_questions"
	__table_args__ = (
		UniqueConstraint("session_id", "question_id", name="uq_session_question_id"),
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	session_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("sessions.session_id"), nullable=False)
	question_id: Mapped[str] = mapped_column(String, nullable=False)
	concept_id: Mapped[str] = mapped_column(String, nullable=False)
	question_text: Mapped[str] = mapped_column(String, nullable=False)
	options: Mapped[list] = mapped_column(JSON, nullable=False)
	correct_option: Mapped[str] = mapped_column(String, nullable=False)
	difficulty_level: Mapped[str | None] = mapped_column(String, nullable=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

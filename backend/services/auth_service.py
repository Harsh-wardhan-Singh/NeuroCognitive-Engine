import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config.settings import PASSWORD_MIN_LENGTH
from db.crud import create_auth_user, get_user_by_email, get_user_by_id


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
	raise ValueError("JWT_SECRET_KEY environment variable is required")

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
TOKEN_DENYLIST: set[str] = set()


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
	return pwd_context.verify(password, password_hash)


def validate_password(password: str) -> None:
	if len(password) < PASSWORD_MIN_LENGTH:
		raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters")
	if not any(char.isdigit() for char in password):
		raise ValueError("Password must include at least one number")


def create_access_token(user_id: UUID) -> str:
	expires_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES)
	payload = {
		"user_id": str(user_id),
		"exp": expires_at,
	}
	return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def signup(db: Session, email: str, password: str):
	existing = get_user_by_email(db, email)
	if existing is not None:
		raise ValueError("Email already exists")

	validate_password(password)

	password_hash = hash_password(password)
	user = create_auth_user(db, {"email": email, "password_hash": password_hash})
	return {
		"user_id": user.user_id,
		"email": user.email,
	}


def login(db: Session, email: str, password: str):
	user = get_user_by_email(db, email)
	if user is None or user.password_hash is None:
		raise ValueError("Invalid credentials")

	if not verify_password(password, user.password_hash):
		raise ValueError("Invalid credentials")

	token = create_access_token(user.user_id)
	return {"token": token}


def get_user_id_from_token(token: str) -> UUID:
	if token in TOKEN_DENYLIST:
		raise ValueError("Token revoked")

	try:
		payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
	except jwt.PyJWTError as error:
		raise ValueError("Invalid token") from error

	user_id_raw = payload.get("user_id")
	if user_id_raw is None:
		raise ValueError("Invalid token payload")

	try:
		return UUID(user_id_raw)
	except ValueError as error:
		raise ValueError("Invalid token payload") from error


def require_authenticated_user(db: Session, token: str):
	user_id = get_user_id_from_token(token)
	user = get_user_by_id(db, user_id)
	if user is None:
		raise ValueError("User not found")
	return user


def revoke_token(token: str):
	TOKEN_DENYLIST.add(token)

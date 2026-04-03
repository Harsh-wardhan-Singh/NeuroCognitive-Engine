from uuid import UUID

from pydantic import BaseModel


class SignupRequest(BaseModel):
	email: str
	password: str


class LoginRequest(BaseModel):
	email: str
	password: str


class SignupResponse(BaseModel):
	user_id: UUID
	email: str


class LoginResponse(BaseModel):
	token: str

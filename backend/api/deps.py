from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from db.database import get_db
from services.auth_service import get_user_id_from_token


bearer_scheme = HTTPBearer()


def get_db_session(db: Session = Depends(get_db)):
	return db


def get_current_user_id(
	credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UUID:
	if credentials.scheme.lower() != "bearer":
		raise HTTPException(status_code=401, detail="Invalid authentication scheme")

	try:
		return get_user_id_from_token(credentials.credentials)
	except ValueError as error:
		raise HTTPException(status_code=401, detail=str(error)) from error

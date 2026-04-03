from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db_session
from schemas.auth_schemas import LoginRequest, LoginResponse, SignupRequest, SignupResponse
from services.auth_service import login, signup


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=SignupResponse)
def signup_route(payload: SignupRequest, db: Session = Depends(get_db_session)):
    try:
        output = signup(db, payload.email, payload.password)
        return SignupResponse(**output)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/login", response_model=LoginResponse)
def login_route(payload: LoginRequest, db: Session = Depends(get_db_session)):
    try:
        output = login(db, payload.email, payload.password)
        return LoginResponse(**output)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error

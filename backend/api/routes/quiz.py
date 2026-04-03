from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_current_user_id, get_db_session
from orchestrator.quiz_orchestrator import end_session, start_session, submit_answer
from orchestrator.schemas import StartSessionRequest, SubmitAnswerRequest


router = APIRouter(tags=["quiz"])


@router.post("/start-session")
def start_session_route(
    payload: StartSessionRequest,
    db: Session = Depends(get_db_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        return start_session(db, user_id, payload.subject, payload.topic, payload.num_questions)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/submit-answer")
def submit_answer_route(
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        return submit_answer(
            db,
            user_id,
            payload.session_id,
            payload.question_id,
            payload.selected_option,
            payload.reported_confidence,
            payload.response_time,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/end-session/{session_id}")
def end_session_route(
    session_id: UUID,
    db: Session = Depends(get_db_session),
    user_id: UUID = Depends(get_current_user_id),
):
    try:
        return end_session(db, user_id, session_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

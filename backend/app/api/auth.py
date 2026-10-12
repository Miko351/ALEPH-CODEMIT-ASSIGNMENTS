from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.member import RegisterRequest, RegisterResponse
from app.services.registration import DuplicateEmailError, register_member

router = APIRouter(prefix="/api/auth", tags=["회원가입"])


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> RegisterResponse:
    try:
        return register_member(payload, session, request.app.state.security)
    except DuplicateEmailError:
        raise HTTPException(
            status_code=409, detail="이미 가입된 이메일입니다. 다른 이메일을 사용해 주세요."
        ) from None

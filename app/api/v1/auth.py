from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import (
    PasswordReset,
    PasswordResetRequest,
    Token,
    UserLogin,
    UserOut,
    UserRegister,
)
from app.services import auth as auth_service

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(
            db,
            name=payload.name,
            email=payload.email,
            password=payload.password,
            location=payload.location,
            role=payload.role,
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        return auth_service.login(db, email=payload.email, password=payload.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/password-reset-request")
def request_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    token = auth_service.request_password_reset(db, email=payload.email)
    if not token:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"message": "Password reset token generated", "token": token}


@router.post("/password-reset")
def reset_password(payload: PasswordReset, db: Session = Depends(get_db)):
    try:
        auth_service.reset_password(db, token=payload.token, new_password=payload.new_password)
        return {"message": "Password reset successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

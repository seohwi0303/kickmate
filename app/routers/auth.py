from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import RegisterRequest, TokenResponse
from app.core.security import create_access_token
from app.services.auth_service import register_user, authenticate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(
            db, email=payload.email, password=payload.password, handle=payload.handle
        )
    except ValueError as e:
        code = str(e)
        if code in ("EMAIL_ALREADY_EXISTS", "HANDLE_ALREADY_EXISTS"):
            raise HTTPException(status_code=409, detail=code)
        raise

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate(db, email=form.username, password=form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_CREDENTIALS",
        )
    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)
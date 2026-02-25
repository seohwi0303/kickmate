from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models.user import User


# auth.py의 login endpoint가 /auth/login 이므로 tokenUrl도 동일하게
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="INVALID_TOKEN")
    except JWTError:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="USER_NOT_FOUND")
    return user
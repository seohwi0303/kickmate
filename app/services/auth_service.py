from sqlalchemy.orm import Session
from app.core.security import password_hash, verify_password
from app.models.user import User


def register_user(db: Session, *, email: str, password: str, handle: str) -> User:
    # 중복 체크
    if db.query(User).filter(User.email == email).first():
        raise ValueError("EMAIL_ALREADY_EXISTS")

    if db.query(User).filter(User.handle == handle).first():
        raise ValueError("HANDLE_ALREADY_EXISTS")

    user = User(
        email=email,
        encrypted_password=password_hash(password),
        handle=handle,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, *, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    # 🔥 여기 반드시 encrypted_password로 맞춰야 함
    if not verify_password(password, user.encrypted_password):
        return None

    return user
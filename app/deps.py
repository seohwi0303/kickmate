# app/deps.py
from __future__ import annotations

from uuid import UUID

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User


def get_current_user(
    db: Session = Depends(get_db),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """
    임시 인증(로그인 전 단계)
    - X-User-Id 헤더가 UUID면: 그 UUID로 유저 조회
    - X-User-Id 헤더가 UUID가 아니면: handle로 간주하고 유저 조회
    """
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing X-User-Id header")

    # 1) UUID로 파싱 시도
    user: User | None = None
    try:
        user_uuid = UUID(x_user_id)
        user = db.query(User).filter(User.id == user_uuid).first()
    except ValueError:
        # 2) UUID가 아니면 handle로 간주
        user = db.query(User).filter(User.handle == x_user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found for X-User-Id")

    return user
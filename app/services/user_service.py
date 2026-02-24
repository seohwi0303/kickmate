from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User  # 네 모델 경로에 맞게

def list_users_paginated(db: Session, limit: int = 20, offset: int = 0):
    # total count
    total = db.query(func.count(User.id)).scalar() or 0

    # items
    items = (
        db.query(User)
        .order_by(User.created_at.desc())  # created_at 없으면 id desc로
        .offset(offset)
        .limit(limit)
        .all()
    )

    has_more = (offset + limit) < total
    next_offset = (offset + limit) if has_more else None

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "next_offset": next_offset,
        "has_more": has_more,
    }
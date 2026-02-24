from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import PaginatedUsersOut
from app.services.user_service import list_users_paginated

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=PaginatedUsersOut)
def list_users(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    data = list_users_paginated(db=db, limit=limit, offset=offset)
    return data
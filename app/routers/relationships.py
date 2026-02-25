from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.schemas.relationship import RelationshipRequestCreate, RelationshipOut
from app.services.relationship_service import (
    send_friend_request,
    accept_friend_request,
    list_my_friends,
)

router = APIRouter(prefix="/relationships", tags=["relationships"])


@router.post("/friend-requests", response_model=RelationshipOut)
def create_friend_request(
    payload: RelationshipRequestCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return send_friend_request(
            db=db,
            requester_id=current_user.id,
            addressee_handle=payload.addressee_handle,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/friend-requests/{request_id}/accept", response_model=RelationshipOut)
def accept_request(
    request_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return accept_friend_request(
            db=db,
            me_id=current_user.id,
            request_id=request_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/friends", response_model=list[RelationshipOut])
def get_my_friends(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_my_friends(db=db, me_id=current_user.id)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.relationship import RelationshipRequestCreate, RelationshipOut
from app.services.relationship_service import send_friend_request, accept_friend_request, list_my_friends

router = APIRouter(prefix="/relationships", tags=["relationships"])

# 임시: 로그인 없으니 me_id를 query로 받는 버전
@router.post("/friend-requests", response_model=RelationshipOut)
def create_friend_request(payload: RelationshipRequestCreate, me_id: str, db: Session = Depends(get_db)):
    try:
        return send_friend_request(db=db, requester_id=me_id, addressee_handle=payload.addressee_handle)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


from uuid import UUID

@router.post("/friend-requests/{request_id}/accept", response_model=RelationshipOut)
def accept_request(request_id: UUID, me_id: UUID, db: Session = Depends(get_db)):
    try:
        return accept_friend_request(db=db, me_id=me_id, request_id=request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/friends", response_model=list[RelationshipOut])
def get_my_friends(me_id: str, db: Session = Depends(get_db)):
    return list_my_friends(db=db, me_id=me_id)
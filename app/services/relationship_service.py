from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.user import User
from app.models.relationship import UserRelationship, RelationshipStatus


def send_friend_request(db: Session, requester_id, addressee_handle: str) -> UserRelationship:
    addressee = db.query(User).filter(User.handle == addressee_handle).first()
    if not addressee:
        raise ValueError("addressee not found")

    if str(addressee.id) == str(requester_id):
        raise ValueError("cannot friend yourself")

    # 이미 관계가 있는지(양방향) 확인
    existing = db.query(UserRelationship).filter(
        or_(
            and_(UserRelationship.requester_id == requester_id, UserRelationship.addressee_id == addressee.id),
            and_(UserRelationship.requester_id == addressee.id, UserRelationship.addressee_id == requester_id),
        )
    ).first()

    if existing:
        # 이미 친구거나 대기중이면 그대로 막기
        if existing.status in (RelationshipStatus.PENDING, RelationshipStatus.ACCEPTED):
            raise ValueError(f"relationship already exists: {existing.status}")
        # 거절/차단이면 정책에 따라 재요청 허용할지 결정 가능(지금은 막기)
        raise ValueError(f"cannot request due to status: {existing.status}")

    rel = UserRelationship(
        requester_id=requester_id,
        addressee_id=addressee.id,
        status=RelationshipStatus.PENDING,
    )
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel


def accept_friend_request(db: Session, me_id, request_id) -> UserRelationship:
    rel = db.query(UserRelationship).filter(UserRelationship.id == request_id).first()
    if not rel:
        raise ValueError("request not found")

    # 수락은 addressee(받는 사람)만 가능
    if str(rel.addressee_id) != str(me_id):
        raise ValueError("not allowed")

    if rel.status != RelationshipStatus.PENDING:
        raise ValueError("not pending")

    rel.status = RelationshipStatus.ACCEPTED
    db.commit()
    db.refresh(rel)
    return rel


def list_my_friends(db: Session, me_id):
    rels = db.query(UserRelationship).filter(
        UserRelationship.status == RelationshipStatus.ACCEPTED,
        or_(
            UserRelationship.requester_id == me_id,
            UserRelationship.addressee_id == me_id,
        ),
    ).all()

    return rels
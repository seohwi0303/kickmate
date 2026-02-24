from app.db.base import Base
from app.db.session import engine

# 모델 import를 해줘야 Base.metadata가 테이블을 알게 됨
from app.models.user import User  # noqa: F401

# 모델들이 create_all 전에 import 되어야 테이블이 생성됨

from app.models.relationship import UserRelationship

def init_db():
    Base.metadata.create_all(bind=engine)
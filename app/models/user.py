# app/models/user.py
import uuid
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class User(Base):
    __tablename__ = "app_users"  # ✅ auth.users 말고 우리 테이블

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    handle = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=True)

    email = Column(String, unique=True, index=True, nullable=True)
    encrypted_password = Column(String, nullable=False)

    elo = Column(Integer, default=1200, nullable=False)
    level = Column(String, default="Bronze", nullable=False)
    trust_tier = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
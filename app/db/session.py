# app/config.py (또는 app/db/session.py)
from dotenv import load_dotenv
load_dotenv()  # <= 최상단에서 1번

import os
DATABASE_URL = os.getenv("DATABASE_URL")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is empty. Check your .env file.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
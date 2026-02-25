from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.db.init_db import init_db
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    now = db.execute(text("SELECT now()")).scalar()
    return {"db": "connected", "now": str(now)}


app.include_router(users_router)

from app.routers.relationships import router as relationships_router
...
app.include_router(users_router)
app.include_router(relationships_router)



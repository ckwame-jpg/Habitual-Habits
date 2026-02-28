import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app import models
from app.routes.users import router as users_router
from app.routes.habits import router as habits_router
from app.auth import router as auth_router, hash_password

load_dotenv()

DEMO_EMAIL = "demo@habitual.dev"
DEMO_PASSWORD = "demo1234"


def seed_demo_account():
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email == DEMO_EMAIL).first()
        if not existing:
            user = models.User(email=DEMO_EMAIL, hashed_password=hash_password(DEMO_PASSWORD))
            db.add(user)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_demo_account()
    yield


app = FastAPI(title="Habitual Habits", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(habits_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running"}

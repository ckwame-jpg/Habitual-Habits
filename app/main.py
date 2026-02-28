import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models
from app.routes.users import router as users_router
from app.routes.habits import router as habits_router
from app.auth import router as auth_router

load_dotenv()

app = FastAPI(title="Habitual Habits")

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

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running"}

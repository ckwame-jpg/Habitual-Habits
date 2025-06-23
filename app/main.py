from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes.users import router as users_router
from app.routes.habits import router as habits_router
from app.auth import router as auth_router

app = FastAPI()
app.include_router(users_router)
app.include_router(habits_router)
app.include_router(auth_router)

# Create the database tables
# This will create the tables defined in the models if they do not exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is working LETS GOOOOOOOO!"}

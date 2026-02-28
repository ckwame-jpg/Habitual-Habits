from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    frequency: str

class Habit(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    frequency: str
    user_id: int


class HabitCompletionCreate(BaseModel):
    date_completed: date

class HabitCompletion(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    habit_id: int
    date_completed: date


class Token(BaseModel):
    access_token: str
    token_type: str

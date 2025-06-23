from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Habit(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class HabitCreate(BaseModel):
    name: str
    description: str

class HabitCompletion(BaseModel):
    completed: bool

    class Config:
        orm_mode = True

class HabitCompletionCreate(BaseModel):
    completed: bool

class Token(BaseModel):
    access_token: str
    token_type: str
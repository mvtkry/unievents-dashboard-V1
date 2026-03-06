from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class EventCreate(BaseModel):
    name: str
    description: str
    status: str = "Active"

class ParticipantCreate(BaseModel):
    name: str
    email: EmailStr
    department: str

class ScoreCreate(BaseModel):
    event_id: int
    participant_id: int
    points: float

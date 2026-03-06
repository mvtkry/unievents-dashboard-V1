from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String)
    status = Column(String, default="Active") # Active, Completed, Planned
    
    scores = relationship("Score", back_populates="event")

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    department = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    scores = relationship("Score", back_populates="participant")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    participant_id = Column(Integer, ForeignKey("participants.id"))
    points = Column(Float)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    event = relationship("Event", back_populates="scores")
    participant = relationship("Participant", back_populates="scores")

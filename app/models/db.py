from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    email=Column(String(255),unique=True,index=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc))
    recommendations=relationship("RecommendationHistory",back_populates="user",cascade="all, delete-orphan")
class RecommendationHistory(Base):
    __tablename__="recommendation_history"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    planner=Column(String(30),nullable=False)
    budget=Column(Float,nullable=False)
    input_json=Column(Text,nullable=False)
    result_json=Column(Text,nullable=False)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc))
    user=relationship("User",back_populates="recommendations")

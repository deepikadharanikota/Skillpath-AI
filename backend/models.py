from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)

class UserState(Base):
    __tablename__ = "user_states"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    target_role = Column(String)
    extracted_skills = Column(JSON) # list of skills
    current_topic = Column(String)
    current_difficulty = Column(String)
    current_module = Column(String)
    module_progress = Column(JSON) # dict
    fatigue = Column(Float, default=0.0)
    
    user = relationship("User")

class QuizHistory(Base):
    __tablename__ = "quiz_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)
    module_key = Column(String)
    difficulty = Column(String)
    quiz_score = Column(Float)
    code_score = Column(Float)
    reward = Column(Float)

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# User table definition
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # One-to-many relationship: a user can have many tasks
    tasks = relationship("Task", back_populates="owner")


# Task table definition
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Each task belongs to a user
    owner = relationship("User", back_populates="tasks")

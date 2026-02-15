from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

user_tasks = Table(
    "user_tasks",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    owned_tasks = relationship("Task", back_populates="owner")
    shared_tasks = relationship(
        "Task",
        secondary=user_tasks,
        back_populates="shared_with_users",
    )

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="owned_tasks")

    shared_with_users = relationship(
        "User",
        secondary=user_tasks,
        back_populates="shared_tasks",
    )

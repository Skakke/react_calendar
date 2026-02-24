from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from app.database import Base


# ---------------------------------------------------------
# Association table for event sharing (many-to-many)
# ---------------------------------------------------------
user_events = Table(
    "user_events",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
)


# ---------------------------------------------------------
# Group Model (Optional - for teams / departments)
# ---------------------------------------------------------
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    users = relationship("User", back_populates="group")


# ---------------------------------------------------------
# User Model
# ---------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Optional: group membership
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship("Group", back_populates="users")

    # Events created/owned by this user
    owned_events = relationship("Event", back_populates="owner")

    # Events shared with this user
    shared_events = relationship(
        "Event",
        secondary=user_events,
        back_populates="shared_with_users",
    )


# ---------------------------------------------------------
# Event Model (FullCalendar aligned)
# ---------------------------------------------------------
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    # Core calendar fields
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)

    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    all_day = Column(Boolean, default=False)

    # Status / tagging
    completed = Column(Boolean, default=False)
    status = Column(String(50), default="scheduled")  
    # e.g. scheduled / confirmed / cancelled

    # Owner
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="owned_events")

    # Shared users (many-to-many)
    shared_with_users = relationship(
        "User",
        secondary=user_events,
        back_populates="shared_events",
    )

    # Optional: audit timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
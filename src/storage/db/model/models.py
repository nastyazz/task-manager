from src.storage.db.model.meta import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey, JSON
import enum
import uuid

class TaskStatus(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class User(Base):
    __tablename__ = "users"


    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

class Intergration(Base):
    __tablename__ = "integrations"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    external_id : Mapped[str] = mapped_column(String(100), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    enabled: Mapped[bool] = mapped_column(nullable=False, default=True)    
    created_at: Mapped[DateTime] = mapped_column(String(50), nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(nullable=False, default=TaskStatus.TODO)
    source: Mapped[String] = mapped_column(String(100), nullable=True)
    external_id: Mapped[String] = mapped_column(String(100), nullable=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(String(50), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(String(50), nullable=False)


class Event(Base):
    __tablename__ = "events"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    task_id: Mapped[UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(String(50), nullable=False)
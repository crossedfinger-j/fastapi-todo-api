# app/models/todos.py
import uuid
from typing import TYPE_CHECKING, Optional
from datetime import date, datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .priority import Priority

class TodoBase(SQLModel):
    content: str
    date: date
    is_completed: bool = Field(default=False)
    category_id: Optional[uuid.UUID] = Field(default=None, foreign_key="category.id")
    priority_id: Optional[int] = Field(default=None, foreign_key="priority.id")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    content: Optional[str] = None
    date: Optional[date] = None
    is_completed: Optional[bool] = None
    category_id: Optional[uuid.UUID] = None
    priority_id: Optional[int] = None


class TodoPublic(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class Todo(TodoBase, table=True):
    __tablename__ = "todos"
    id: uuid.UUID = Field(primary_key=True, default=uuid.uuid4)
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")

    created_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    owner: "User" = Relationship(back_populates="todos")
    category: Optional["Category"] = Relationship(back_populates="todos")
    priority: Optional["Priority"] = Relationship(back_populates="todos")

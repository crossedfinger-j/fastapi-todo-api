# app/models/priority.py
from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .todos import Todo

class Priority(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=255)
    todos: List["Todo"] = Relationship(back_populates="priority")

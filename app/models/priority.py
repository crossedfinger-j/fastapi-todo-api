# app/models/priority.py
import uuid
from sqlmodel import SQLModel, Field, Relationship

class Priority(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=255)

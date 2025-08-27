# app/models/user.py
# model + schema
import uuid
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from typing import List


class UserBase(SQLModel):
    """ common field for API, DB """
    username: EmailStr = Field(unique=True, index=True, max_length=255)

class UserCreate(UserBase):
    """ Data format that the API will receive during user registration """
    password: str = Field(min_length=8, max_length=40)

class UserPublic(UserBase):
    """ API response body for user information (password excluded) """
    id: uuid.UUID

class User(UserBase, table=True):
    """ User Entity (Database Table model) """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str
    created_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    categories: List["Category"] = Relationship(back_populates="owner")

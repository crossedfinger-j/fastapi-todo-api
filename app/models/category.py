# app/models/category.py
import uuid
from sqlmodel import SQLModel, Field, Relationship

class CategoryBase(SQLModel):
    name: str = Field(index=True, max_length=255)

class CategoryCreate(CategoryBase):
    pass

class CategoryPublic(CategoryBase):
    id: uuid.UUID
    user_id: uuid.UUID

class Category(CategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")

    owner: "User" = Relationship(back_populates="categories")

# app/crud/category.py
import uuid

from sqlmodel import Session, select
from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.models.user import User


def get_category_by_user(db: Session, user: User) -> list[Category]:
    statement = select(Category).where(Category.user_id == user.id)
    return db.exec(statement).all()

def create_category(db: Session, category_id: CategoryCreate, user: User) -> Category:
    db_category = Category.model_validate(
        category_id, update={"user_id": user.id}
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category_by_id(db: Session, category_id: uuid.UUID) -> Category | None:
    return db.get(Category, category_id)

def update_category(
        *,
        session: Session,
        db_category: Category,
        category_in: CategoryUpdate
) -> Category:
    update_data = category_in.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(update_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

def delete_category(db: Session, db_category: Category) -> None:
    db.delete(db_category)
    db.commit()
    return

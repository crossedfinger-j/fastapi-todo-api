# app/crud/category.py
from sqlmodel import Session, select
from app.models.category import Category, CategoryCreate
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


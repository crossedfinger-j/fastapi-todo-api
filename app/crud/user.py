from sqlmodel import Session, select
from app.core.security import get_password_hash
from pydantic import EmailStr
from app.models.user import User, UserCreate


def get_user_by_username(db: Session, username: str | EmailStr) -> User | None:
    statement = select(User).where(User.username == str(username))
    user = db.exec(statement).first()
    return user

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    user_data = user_in.model_dump()
    db_user = User(**user_data, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

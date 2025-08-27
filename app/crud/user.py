from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from pydantic import EmailStr
from app.models.user import User, UserCreate


def get_user_by_username(db: Session, username: str | EmailStr) -> User | None:
    statement = select(User).where(User.username == str(username))
    user = db.exec(statement).first()
    return user

def create_user(db: Session, user_in: UserCreate) -> User:
    db_obj = User.model_validate(
        user_in,
        update={
            "password": get_password_hash(user_in.password),
        }
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def authenticate(*, db: Session, username: str, password: str) -> User | None:
    db_user = get_user_by_username(db, username=username)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return db_user

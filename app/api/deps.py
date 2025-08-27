from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session
from app.core import security
from app.db.session import engine
from app.models.user import User
from app.core.config import settings
from app.crud.user import get_user_by_username
from pydantic import ValidationError

from app.models.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_db():
    with Session(engine) as session:
        yield session

def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = get_user_by_username(db, username=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
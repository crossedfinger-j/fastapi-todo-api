from typing import Any
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.api import deps
from app.models.priority import Priority

router = APIRouter()

@router.get('/priorities', response_model=list[Priority])
def get_all_priorities(
    db: Session = Depends(deps.get_db)
) -> Any:
    statement = select(Priority).order_by(Priority.id)
    return db.exec(statement).all()
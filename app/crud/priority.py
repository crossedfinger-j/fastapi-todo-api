from sqlmodel import Session

from app.models import Priority


def get_priority_by_id(db: Session, priority_id: int) -> Priority | None:
    return db.get(Priority, priority_id)
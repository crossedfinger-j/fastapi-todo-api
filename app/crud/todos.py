# app/crud/todos.py
from sqlmodel import Session, select
from app.models import Todo, User
from app.models.todos import TodoCreate, TodoUpdate
import uuid
from datetime import date
from typing import List


def get_todos_by_user(
        *,
        session: Session,
        owner: User,
        start_date: date | None = None,
        end_date: date | None = None,
        completed: bool | None = None,
        priority_id: int | None = None,
        category_id: uuid.UUID | None = None,
) -> List[Todo]:
    statement = select(Todo).where(Todo.user_id == owner.id)

    # filtering
    if start_date:
        statement = statement.where(Todo.date >= start_date)
    if end_date:
        statement = statement.where(Todo.date <= end_date)
    if completed is not None:
        statement = statement.where(Todo.is_completed == completed)
    if priority_id is not None:
        statement = statement.where(Todo.priority_id == priority_id)
    if category_id is not None:
        statement = statement.where(Todo.category_id == category_id)

    todos = session.exec(statement).all()
    return todos


def create_todo(
        *,
        session: Session,
        todo_in: TodoCreate,
        owner: User
) -> Todo:
    db_obj = Todo.model_validate(todo_in, update={"user_id": owner.id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_todo(
        *,
        session: Session,
        db_todo: Todo,
        todo_in: TodoUpdate
) -> Todo:
    update_todo = todo_in.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(update_todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def get_todo_by_id(
        *,
        session: Session,
        todo_id: uuid.UUID
) -> Todo | None:
    return session.get(Todo, todo_id)

def remove_todo(*, session: Session, db_todo: Todo) -> None:
    session.delete(db_todo)
    session.commit()
    return

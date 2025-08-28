import uuid
from datetime import date
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.api import deps
from app.crud import todos as crud_todo
from app.crud import category as crud_category
from app.crud import priority as crud_priority
from app.models.message import Message
from app.models.todos import Todo, TodoCreate, TodoPublic, TodoUpdate
from app.models.user import User

router = APIRouter()

@router.get("/todos", response_model=List[TodoPublic])
def get_my_todos(
        *,
        session: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        start_date: date | None = Query(None, description="Start date of YYYY-MM-DD"),
        end_date: date | None = Query(None, description="End date of YYYY-MM-DD"),
        completed: bool | None = Query(None, description="filter of completion"),
        priority_id: int | None = Query(None, description="filter of priority"),
        category_id: uuid.UUID | None = Query(None, description="filter of category"),
) -> Any:
    todos = crud_todo.get_todos_by_user(
        session=session,
        owner=current_user,
        start_date=start_date,
        end_date=end_date,
        completed=completed,
        priority_id=priority_id,
        category_id=category_id,
    )
    return todos

@router.post("/todos", response_model=TodoPublic, status_code=201)
def create_todo(
        *,
        session: Session = Depends(deps.get_db),
        todo_in: TodoCreate,
        current_user: User = Depends(deps.get_current_user),
) -> Any:
    category = crud_category.get_category_by_id(db=session, category_id=todo_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions for this category")

    priority = crud_priority.get_priority_by_id(db=session, priority_id=todo_in.priority_id)
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")

    return crud_todo.create_todo(session=session, todo_in=todo_in, owner=current_user)

@router.get("/todos/{todo_id}", response_model=TodoPublic)
def get_todo_details(
        *,
        session: Session = Depends(deps.get_db),
        todo_id: uuid.UUID,
        current_user: User = Depends(deps.get_current_user),
) -> Any:
    todo = crud_todo.get_todo_by_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return todo

@router.put("/todos/{todo_id}", response_model=TodoPublic)
def update_todo_item(
        *,
        session: Session = Depends(deps.get_db),
        todo_id: uuid.UUID,
        todo_in: TodoUpdate,
        current_user: User = Depends(deps.get_current_user),
) -> Any:
    db_todo = crud_todo.get_todo_by_id(session=session, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    update_data = todo_in.model_dump(exclude_unset=True)
    if "category_id" in update_data:
        category = crud_category.get_category_by_id(db=session, category_id=update_data["category_id"])
        if not category:
            raise HTTPException(status_code=404, detail="Category not found to update")
        if category.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions for this category")

    if "priority_id" in update_data:
        priority = crud_priority.get_priority_by_id(db=session, priority_id=update_data["priority_id"])
        if not priority:
            raise HTTPException(status_code=404, detail="Priority not found")

    updated_todo = crud_todo.update_todo(session=session, db_todo=db_todo, todo_in=todo_in)
    return updated_todo

@router.delete("/todos/{todo_id}", response_model=Message)
def delete_todo(
        *,
        session: Session = Depends(deps.get_db),
        todo_id: uuid.UUID,
        current_user: User = Depends(deps.get_current_user),
) -> Any:
    db_todo = crud_todo.get_todo_by_id(session=session, todo_id=todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    crud_todo.remove_todo(session=session, db_todo=db_todo)
    return Message(
        message="success",
    )


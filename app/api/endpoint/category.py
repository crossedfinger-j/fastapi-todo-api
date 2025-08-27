# app/api/endpoint/category.py
# app/api/endpoint/category.py
import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api import deps
from app.crud import category as crud_category
from app.models.category import Category, CategoryCreate, CategoryPublic, CategoryUpdate
from app.models.message import Message
from app.models.user import User

router = APIRouter()

@router.get('/categories', response_model=list[CategoryPublic])
def get_my_categories(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)
) -> Any:
    return crud_category.get_category_by_user(db=db, user=current_user)

@router.post("/categories", response_model=CategoryPublic)
def create_category(
        *,
        db: Session = Depends(deps.get_db),
        category_in: CategoryCreate,
        current_user: User = Depends(deps.get_current_user)
) -> Any:
    return crud_category.create_category(db, category_id=category_in, user=current_user)

@router.put('/categories/{category_id}', response_model=CategoryPublic)
def update_category(
        *,
        db: Session = Depends(deps.get_db),
        category_id: uuid.UUID,
        category_in: CategoryUpdate,
        current_user: User = Depends(deps.get_current_user)
) -> Any:
    db_category = crud_category.get_category_by_id(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if db_category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    update_data = category_in.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(update_data)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete('/categories/{category_id}', response_model=Message)
def delete_category(
        *,
        db: Session = Depends(deps.get_db),
        category_id: uuid.UUID,
        current_user: User = Depends(deps.get_current_user)
) -> Any:
    db_category = crud_category.get_category_by_id(db=db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if db_category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(db_category)
    db.commit()
    return Message(
        message="success",
    )

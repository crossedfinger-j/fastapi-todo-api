# app/api/endpoint/category.py
# app/api/endpoint/category.py
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api import deps
from app.crud import category as crud_category
from app.models.category import Category, CategoryCreate, CategoryPublic
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


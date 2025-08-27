# app/api/routers.py
from fastapi import APIRouter

from app.api.endpoint import user, category

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
api_router.include_router(category.router, tags=["category"])
# app/api/routers.py
from fastapi import APIRouter

from app.api.endpoint import user, category, priority

api_router = APIRouter()
api_router.include_router(user.router, tags=["user"])
api_router.include_router(category.router, tags=["category"])
api_router.include_router(priority.router, tags=["priority"])
# app/api/routers.py
from fastapi import APIRouter

from app.api.endpoint import login

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
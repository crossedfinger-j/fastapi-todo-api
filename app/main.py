from fastapi import FastAPI
from contextlib import asynccontextmanager # 추가
from app.initial_data import create_initial_priorities # 추가
from app.api.routers import api_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_initial_priorities() # 앱 시작 시 초기 데이터 생성
    yield
    print("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)

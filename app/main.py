import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager # 추가

# --- DB 설정 (이 부분은 그대로 둡니다) ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy 모델 정의 (이 부분도 그대로 둡니다) ---
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# --- FastAPI 앱 수명 주기(Lifespan) 관리 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱이 시작될 때 실행됩니다.
    print("애플리케이션 시작...")
    # 이 시점에서 테이블을 생성합니다.
    Base.metadata.create_all(bind=engine)
    yield
    # 앱이 종료될 때 실행됩니다 (여기서는 특별한 작업 없음).
    print("애플리케이션 종료...")

# FastAPI 앱 인스턴스에 lifespan을 연결합니다.
app = FastAPI(lifespan=lifespan)

# --- Pydantic 모델 및 API 코드는 이전과 동일합니다 ---
class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemSchema(ItemBase):
    id: int
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=ItemSchema)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[ItemSchema])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items
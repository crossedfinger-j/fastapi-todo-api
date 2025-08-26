# app/models/user.py
# model + schema
import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


# --- 1. 공통 속성을 가진 기본 모델 ---

# API와 DB 모델이 공통으로 사용할 필드를 정의합니다.
class UserBase(SQLModel):
    username: EmailStr = Field(unique=True, index=True, max_length=255)

# --- 2. API 전용 모델 (스키마) ---

# 회원가입 시 API가 받을 데이터 형태
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

# API가 사용자 정보를 응답으로 보낼 때의 형태 (비밀번호 제외)
class UserPublic(UserBase):
    id: uuid.UUID


# --- 3. DB 테이블 전용 모델 ---

# 'table=True'를 통해 실제 DB 테이블과 연결되는 모델임을 선언
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str


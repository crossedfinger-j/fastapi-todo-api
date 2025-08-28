# FastAPI To-do List API 📝
FastAPI, SQLModel, PostgreSQL을 사용하여 구축한 To-do List 백엔드 API 프로젝트입니다.

Docker를 활용하여 개발 환경을 손쉽게 구성할 수 있으며, JWT 토큰 기반의 사용자 인증을 포함한 전체 CRUD 기능을 제공합니다. 이 프로젝트는 FastAPI의 현대적인 기능과 ORM의 효율성을 학습하는 과정을 기록합니다.

### ✨ 주요 기능 
* 사용자 인증: JWT 토큰 기반의 회원가입 및 로그인

* 카테고리 관리: 사용자별 고유 카테고리 생성, 조회, 수정, 삭제 (CRUD)

* 중요도 관리: 모든 사용자가 공유하는 사전 정의된 중요도 목록 조회

* 할 일(To-do) 관리:

  * 사용자별 To-do 생성, 조회, 수정, 삭제 (CRUD)

  * 기간, 완료 여부, 카테고리, 중요도 등 다양한 조건으로 필터링 가능한 목록 조회

### 🛠️ 기술 스택
* Backend: FastAPI, SQLModel (Pydantic + SQLAlchemy), Uvicorn
* Database: PostgreSQL (Docker를 통해 실행)
* Authentication: JWT (JSON Web Tokens), passlib[bcrypt]
* Migrations: Alembic
* Environment: Docker, Docker Compose, Python 3.10+

### 🚀 프로젝트 시작하기 
1. 프로젝트 복제
<pre>
<code>
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
</code>
</pre>

2. .env 파일 생성
프로젝트 루트 디렉토리에 .env 파일을 만들고 아래 내용을 복사하여 붙여넣으세요. SECRET_KEY는 반드시 새로운 값으로 교체해야 합니다.
<pre>
<code>
# .env

# POSTGRES (로컬 개발 시 Docker DB 접속용)
POSTGRES_SERVER=localhost
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb
</code>
</pre>

3. 데이터베이스 실행
Docker를 사용하여 PostgreSQL 데이터베이스 컨테이너를 실행합니다. 
<pre>
<code>
docker-compose up -d db
</code>
</pre>

4. 가상환경 설정 및 라이브러리 설치
<pre>
<code>
# 1. 가상환경 생성
python -m venv .venv

# 2. 가상환경 활성화 (Windows)
.\.venv\Scripts\activate
# (macOS/Linux: source .venv/bin/activate)

# 3. 필요 라이브러리 설치
pip install -r requirements.txt
</code>
</pre>

5. 데이터베이스 마이그레이션
Alembic을 사용하여 데이터베이스에 모든 테이블을 생성합니다.
<pre>
<code>
alembic upgrade head
</code></pre>

6. FastAPI 서버 실행
<pre>
<code>
# --port 8001 또는 원하는 포트로 실행
uvicorn app.main:app --reload --port 8000
</code></pre>

### 📚 API 문서 
이 API는 FastAPI의 자동 문서화 기능을 통해 완벽한 API 문서를 제공합니다. 서버를 실행한 후 아래 주소로 접속하세요. 
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

### 🗄️ 데이터베이스 마이그레이션 (Alembic)
app/models 폴더의 모델 파일을 수정한 후에는 반드시 아래 명령어를 통해 데이터베이스 스키마를 업데이트해야 합니다.

1. 마이그레이션 파일 자동 생성:
<pre>
<code>
alembic revision --autogenerate -m "변경 사항에 대한 설명"
</code>
</pre>
2. 데이터베이스에 마이그레이션 적용:
<pre>
<code>
alembic upgrade head
</code>
</pre>

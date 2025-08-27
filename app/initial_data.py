from sqlmodel import Session, select
from app.db.session import engine
from app.models.priority import Priority

PRIORITIES = [
    {"id": 1, "name": "낮음"},
    {"id": 2, "name": "보통"},
    {"id": 3, "name": "높음"},
    {"id": 4, "name": "매우 높음"},
]

def create_initial_priorities():
    with Session(engine) as session:
        statement = select(Priority)
        results = session.exec(statement).all()
        if not results:
            print("Creating initial priorities...")
            for priority_data in PRIORITIES:
                db_priority = Priority.model_validate(priority_data)
                session.add(db_priority)
            session.commit()
            print("Initial priorities created.")
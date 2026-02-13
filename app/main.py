from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db import Base, engine, SessionLocal
from app.models import Task as TaskModel

app = FastAPI(title="FastAPI Starter", version="0.2.0")

# crea tablas al arrancar (simple para comenzar)
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TaskIn(BaseModel):
    title: str
    done: bool = False


class TaskOut(TaskIn):
    id: str


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskIn, db: Session = Depends(get_db)):
    task = TaskModel(id=str(uuid4()), title=payload.title, done=payload.done)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

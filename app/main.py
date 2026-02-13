from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: str, payload: TaskIn, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = payload.title
    task.done = payload.done

    db.commit()
    db.refresh(task)
    return task

@app.delete("/task/{task_id}", status_code=204)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail = "Task not found")

    db.delete(task)
    db.commit()
    return    
    
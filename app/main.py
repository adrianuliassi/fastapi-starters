from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uuid import uuid4


app = FastAPI(title="FastAPI Starter", version="0.1.0")

@app.get("/health")
def health():
     return{"status" : "ok"}

class TaskIn(BaseModel):
     title : str
     done: bool = False

class Task(TaskIn):
     id: str

tasks : List[Task] = []

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskIn):
     task = Task(id=str(uuid4()), **payload.model_dump())
     tasks.append(task)
     return task

@app.get("/tasks", response_model = List[Task])
def lis_tasks():
     return tasks
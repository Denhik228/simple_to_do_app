from fastapi import FastAPI, status
from uuid import uuid4
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreatedSchema(BaseModel):
    title: str

tasks: list[TaskSchema] = []

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

@app.get('/tasks')
def get_tasks() -> list[TaskSchema]:
    return tasks

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreatedSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task

def find_task_from_id(id: str):
    for task in tasks:
        if task.id == id:
            return tasks.index(task)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id):
      for task in tasks:
          if task.id == task_id:
              tasks.remove(task)

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema) -> TaskSchema:
    if payload.title:
        tasks[find_task_from_id(task_id)].title = payload.title
    if payload.completed is not None:
        tasks[find_task_from_id(task_id)].completed = payload.completed

    return tasks[find_task_from_id(task_id)]


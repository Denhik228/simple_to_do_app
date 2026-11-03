from fastapi import FastAPI, status, HTTPException
from uuid import uuid4
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

DATABASE_URL = "postgresql+psycopg://postgres:MDMS2010[2010]@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bin=engine)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreatedSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class CategorySchema(BaseModel):
    id: str
    name: str

class CategoryCreateSchema(BaseModel):
    name: str

tasks: list[TaskSchema] = []
categories: list[CategorySchema] = []

def find_item_from_id(id: str, var):
    for item in var:
        if item.id == id:
            return var.index(item)
    return False

@app.get('/tasks')
def get_tasks() -> list[TaskSchema]:
    return tasks

@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreatedSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
      for task in tasks:
          if task.id == task_id:
              tasks.remove(task)

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema) -> TaskSchema:
    if payload.title:
        tasks[find_item_from_id(task_id, tasks)].title = payload.title
    if payload.completed is not None:
        tasks[find_item_from_id(task_id, tasks)].completed = payload.completed

    return tasks[find_item_from_id(task_id, tasks)]

@app.get('/categories')
def get_categories() -> list[CategorySchema]:
    return categories

@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema):
    new_category = CategorySchema(id=str(uuid4()),name=payload.name)
    categories.append(new_category)

    return new_category

@app.patch('/categories/{category_id}')
def update_category(category_id, payload: CategoryCreateSchema):
    if find_item_from_id(str(category_id), categories) is not None:
        categories[find_item_from_id(category_id, categories)].name = payload.name

        return categories[find_item_from_id(category_id, categories)]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    if find_item_from_id(category_id, categories) is not None:
        for category in categories:
            if category.id == category_id:
                categories.remove(category)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

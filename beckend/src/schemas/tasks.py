from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreatedSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
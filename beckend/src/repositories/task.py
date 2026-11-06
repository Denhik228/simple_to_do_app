from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.task import TaskORM
from src.schemas.tasks import TaskCreatedSchema

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[TaskORM]:
        return list(self.db.scalars(select(TaskORM)).all())

    def get_by_id(self, task_id: str) -> TaskORM | None:
        return self.db.get(TaskORM, task_id)

    def create(self, payload: TaskCreatedSchema) -> TaskORM:
        new_task = TaskORM(title=payload.title)
        self.db.add(new_task)
        return new_task

    def delete(self, task_orm: TaskORM) -> None:
        self.db.delete(task_orm)
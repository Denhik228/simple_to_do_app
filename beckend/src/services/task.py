import json

from sqlalchemy.orm import Session

from src.cache.redi_s import RedisCache
from src.repositories.task import TaskRepository
from src.schemas.tasks import TaskSchema, TaskCreatedSchema, TaskUpdateSchema
from src.models.task import TaskORM
from src.core.config import get_settings

settings = get_settings()

class TaskNotFound(Exception):
    """"Task with id not found in DataBase"""

def convert_task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)
        self.cache = RedisCache(redis_url=settings.redis_url, redis_time_to_live_seconds=settings.cache_time_to_live_seconds)

    def get_all(self) -> list[TaskSchema]:
        task_cache = self.cache.get(settings.redis_task_key)
        if task_cache is not None:
            return [TaskSchema(id=task["id"], title=task["title"], completed=task["completed"]) for task in task_cache]

        task_orm = self.task_repository.get_all()
        tasks = [TaskSchema(id=task.id, title=task.title, completed=task.completed) for task in task_orm]
        tasks_for_cache = [task.model_dump() for task in tasks]
        self.cache.set(settings.redis_task_key, tasks_for_cache)

        return [TaskSchema(id=task.id, title=task.title, completed=task.completed) for task in task_orm]

    def create(self, payload: TaskCreatedSchema) -> TaskSchema:
        self.cache.delete(settings.redis_task_key)

        new_task = self.task_repository.create(payload)
        self.db.commit()
        return convert_task_orm_to_model(new_task)

    def update(self, task_id: str, payload: TaskUpdateSchema) -> TaskSchema:
        self.cache.delete(settings.redis_task_key)

        task_to_update = self.task_repository.get_by_id(task_id)
        if task_to_update is None:
            raise TaskNotFound(f"Task with {task_id} id not found")
        if payload.title:
            task_to_update.title = payload.title
        if payload.completed is not None:
            task_to_update.completed = payload.completed
        self.db.commit()

        return convert_task_orm_to_model(task_to_update)

    def delete(self, task_id: str) -> None:
        self.cache.delete(settings.redis_task_key)

        task_to_delete = self.task_repository.get_by_id(task_id)
        if task_to_delete is None:
            raise TaskNotFound(f"Task with id {task_id} not found")
        self.task_repository.delete(task_to_delete)
        self.db.commit()
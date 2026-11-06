from sqlalchemy.orm import Session
from fastapi import Depends

from src.services.category import CategoryService
from src.services.task import TaskService
from src.database.session import get_dataBase


def get_task_service(db: Session = Depends(get_dataBase)) -> TaskService:
    return TaskService(db=db)

def get_category_service(db: Session = Depends(get_dataBase)) -> CategoryService:
    return CategoryService(db=db)
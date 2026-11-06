from fastapi import status, APIRouter, Depends, HTTPException

from src.schemas.tasks import TaskSchema, TaskCreatedSchema, TaskUpdateSchema
from src.services.task import TaskService, TaskNotFound
from src.api.dependencies import get_task_service

router = APIRouter(prefix='/tasks')

@router.get('')
def get_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.get_all()

@router.post('', status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreatedSchema, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    return task_service.create(payload)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    try:
        task_service.delete(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.patch("/{task_id}")
def update_task(
        task_id: str,
        payload: TaskUpdateSchema,
        task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    try:
        return task_service.update(task_id, payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
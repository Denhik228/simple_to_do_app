from fastapi import status, APIRouter, Depends, HTTPException

from src.schemas.categories import CategorySchema, CategoryCreateSchema
from src.services.category import CategoryService, CategoryNotFound
from src.services.task import TaskService
from src.api.dependencies import get_category_service

router = APIRouter(prefix='/categories')

@router.get('')
def get_categories(category_service: CategoryService = Depends(get_category_service)) -> list[CategorySchema]:
    return category_service.get_all()

@router.post('', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema,
                    category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    return category_service.create(payload)

@router.patch('/{category_id}')
def update_category(category_id,
                    payload: CategoryCreateSchema,
                    category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    try:
        return category_service.update(category_id, payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_service: CategoryService = Depends(get_category_service)) -> None:
    try:
        return category_service.delete(category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
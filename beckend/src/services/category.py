from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.repositories.categories import CategoryRepository
from src.schemas.categories import CategorySchema, CategoryCreateSchema
from src.models.category import CategoryORM

class CategoryNotFound(Exception):
    """"Category with id not found in DataBase"""

def convert_category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
    return CategorySchema(id=category_orm.id, name=category_orm.title)

class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db=db)

    def get_all(self) -> list[CategorySchema]:
        categories_orm = self.category_repository.get_all()
        return [CategorySchema(id=category.id, name=category.title) for category in categories_orm]

    def create(self, payload: CategoryCreateSchema) -> CategorySchema:
        new_category = self.category_repository.create(payload=payload)
        self.db.commit()
        return convert_category_orm_to_model(new_category)

    def update(self, category_id: str, payload: CategoryCreateSchema) -> CategorySchema:
        category_to_update = self.category_repository.get_by_id(category_id=category_id)
        if category_to_update is not None:
            category_to_update.title = payload.name
            self.db.commit()

            return convert_category_orm_to_model(category_to_update)
        else:
            raise CategoryNotFound(f"Categori with id {category_id} not found")

    def delete(self, category_id: str) -> None:
        category_to_delete = self.category_repository.get_by_id(category_id=category_id)
        if category_to_delete is None:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        self.db.delete(category_to_delete)
        self.db.commit()
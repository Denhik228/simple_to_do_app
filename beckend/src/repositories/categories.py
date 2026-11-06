from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.category import CategoryORM
from src.schemas.categories import CategorySchema, CategoryCreateSchema

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())

    def get_by_id(self, category_id) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)

    def create(self, payload: CategoryCreateSchema) -> CategoryORM:
        new_category = CategoryORM(title=payload.name)
        self.db.add(new_category)
        return new_category

    def delete(self, category_orm: CategoryORM):
        self.db.delete(category_orm)


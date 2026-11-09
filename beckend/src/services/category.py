from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.cache.redi_s import RedisCache
from src.repositories.categories import CategoryRepository
from src.schemas.categories import CategorySchema, CategoryCreateSchema
from src.models.category import CategoryORM
from src.core.config import get_settings

settings = get_settings()

class CategoryNotFound(Exception):
    """"Category with id not found in DataBase"""

def convert_category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
    return CategorySchema(id=category_orm.id, name=category_orm.title)

class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db=db)
        self.cache = RedisCache(redis_url=settings.redis_url, redis_time_to_live_seconds=settings.cache_time_to_live_seconds)

    def get_all(self) -> list[CategorySchema]:
        category_cache = self.cache.get(settings.redis_category_key)
        if category_cache is not None:
            return [CategorySchema(id=category["id"], name=category["name"]) for category in category_cache]

        categories_orm = self.category_repository.get_all()
        categories = [CategorySchema(id=category.id, name=category.title) for category in categories_orm]
        category_for_cache = [category.model_dump() for category in categories]
        self.cache.set(settings.redis_category_key, category_for_cache)

        return  categories

    def create(self, payload: CategoryCreateSchema) -> CategorySchema:
        self.cache.delete(settings.redis_category_key)

        new_category = self.category_repository.create(payload=payload)
        self.db.commit()
        return convert_category_orm_to_model(new_category)

    def update(self, category_id: str, payload: CategoryCreateSchema) -> CategorySchema:
        self.cache.delete(settings.redis_category_key)

        category_to_update = self.category_repository.get_by_id(category_id=category_id)
        if category_to_update is not None:
            category_to_update.title = payload.name
            self.db.commit()

            return convert_category_orm_to_model(category_to_update)
        else:
            raise CategoryNotFound(f"Categori with id {category_id} not found")

    def delete(self, category_id: str) -> None:
        self.cache.delete(settings.redis_category_key)

        category_to_delete = self.category_repository.get_by_id(category_id=category_id)
        if category_to_delete is None:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        self.db.delete(category_to_delete)
        self.db.commit()
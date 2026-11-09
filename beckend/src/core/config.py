from dataclasses import dataclass

@dataclass()
class Settings():
    DATABASE_URL: str
    redis_url: str
    cache_time_to_live_seconds: int
    redis_task_key: str
    redis_category_key: str
    cors_allow_origins: list[str]
    cors_allow_methods: list[str]

def get_settings():
    return Settings(
        DATABASE_URL="postgresql+psycopg://postgres:MDMS2010[2010]@localhost:5432/postgres",
        redis_url="redis://localhost:6379/0",
        cache_time_to_live_seconds=3600,
        redis_task_key="cache:task_list",
        redis_category_key="cache:category_list",
        cors_allow_origins=["http://localhost:3000"],
        cors_allow_methods=["*"]
    )
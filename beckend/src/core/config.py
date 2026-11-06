from dataclasses import dataclass

@dataclass()
class Settings():
    DATABASE_URL: str
    cors_allow_origins: list[str]
    cors_allow_methods: list[str]

def get_settings():
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:MDMS2010[2010]@localhost:5432/postgres",
        cors_allow_origins = ["http://localhost:3000"],
        cors_allow_methods =["*"]
    )
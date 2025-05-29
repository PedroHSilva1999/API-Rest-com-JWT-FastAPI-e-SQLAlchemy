import os 
from sqlalchemy.ext.declarative import declarative_base
import dotenv 
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import ClassVar

DB_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/users_products"
dotenv.load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = DB_URL
    DBBaseModel: ClassVar[DeclarativeMeta] = declarative_base()

    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 dias

    class Config:
        case_sensitive = True


settings = Settings()

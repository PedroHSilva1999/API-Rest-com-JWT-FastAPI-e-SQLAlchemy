from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.configs import settings
from typing import List

class User(settings.DBBaseModel):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(256), nullable=False)
    email: str = Column(String(256), nullable=False, unique=True)
    password: str = Column(String(256), nullable=False)
    is_admin: bool = Column(Boolean, default=False)
    is_active: bool = Column(Boolean, default=True)

  
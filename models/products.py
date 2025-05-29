import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from core.configs import settings

class Product(settings.DBBaseModel):
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(256), nullable=False)
    description: str = Column(String(256), nullable=False)
    price: float = Column(Float, nullable=False)
    stock: int = Column(Integer, nullable=False)
    is_active: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.datetime.now)
    updated_at: datetime = Column(DateTime, default=datetime.datetime.now)
    created_by: int = Column(Integer, ForeignKey("users.id"))
    updated_by: int = Column(Integer, ForeignKey("users.id"))


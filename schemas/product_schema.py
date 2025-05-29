from pydantic import BaseModel
from typing import Optional
import datetime
class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    stock: int
    is_active: Optional[bool] = True
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True


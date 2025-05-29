import datetime
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    password: str
    is_admin: bool = False
    is_active: bool = True

    class Config:
        from_attributes = True

class UserSchemaCreate(UserSchema):
    password: str

    class Config:
        extra = "ignore"
        
class UserSchemaUpdate(UserSchema):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    updated_at: Optional[datetime.datetime.now] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "extra": "ignore"
    }


class UserSchemaOut(UserSchema):
    id: int
    name: str
    email: str
    is_admin: bool
    is_active: bool
    class Config:
        from_attributes = True

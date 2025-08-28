from pydantic import EmailStr
from app.schemas.base import BaseSchema

class UserCreate(BaseSchema):
    email: EmailStr
    password: str

class UserOut(BaseSchema):
    id: int
    email: EmailStr
    is_active: bool
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True 
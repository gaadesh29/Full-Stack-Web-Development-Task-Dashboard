from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PortfolioBase(BaseModel):
    name: str

class PortfolioCreate(PortfolioBase):
    user_id: UUID

class PortfolioOut(PortfolioBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True 
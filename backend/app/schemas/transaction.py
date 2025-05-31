from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    investment_id: UUID
    type: str
    amount: float
    nav: Optional[float] = None
    units: Optional[float] = None
    date: date

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: UUID

    class Config:
        orm_mode = True 
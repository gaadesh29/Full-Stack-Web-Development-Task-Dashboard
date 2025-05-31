from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class FundHoldingBase(BaseModel):
    mutual_fund_id: UUID
    stock_id: UUID
    weight_percent: Optional[float] = None
    as_of_date: Optional[date] = None

class FundHoldingCreate(FundHoldingBase):
    pass

class FundHoldingOut(FundHoldingBase):
    id: UUID

    class Config:
        orm_mode = True 
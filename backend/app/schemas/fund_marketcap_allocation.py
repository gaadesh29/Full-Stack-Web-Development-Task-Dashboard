from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class FundMarketCapAllocationBase(BaseModel):
    mutual_fund_id: UUID
    large_cap_percent: Optional[float] = None
    mid_cap_percent: Optional[float] = None
    small_cap_percent: Optional[float] = None
    as_of_date: Optional[date] = None

class FundMarketCapAllocationCreate(FundMarketCapAllocationBase):
    pass

class FundMarketCapAllocationOut(FundMarketCapAllocationBase):
    id: UUID

    class Config:
        orm_mode = True 
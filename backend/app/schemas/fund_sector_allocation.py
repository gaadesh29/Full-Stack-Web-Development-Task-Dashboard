from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class FundSectorAllocationBase(BaseModel):
    mutual_fund_id: UUID
    sector_id: UUID
    weight_percent: Optional[float] = None
    as_of_date: Optional[date] = None

class FundSectorAllocationCreate(FundSectorAllocationBase):
    pass

class FundSectorAllocationOut(FundSectorAllocationBase):
    id: UUID

    class Config:
        orm_mode = True 
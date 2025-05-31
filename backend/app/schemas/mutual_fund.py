from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class MutualFundBase(BaseModel):
    name: str
    isin: str
    amc: Optional[str] = None
    fund_type: Optional[str] = None
    category: Optional[str] = None
    benchmark: Optional[str] = None
    risk_level: Optional[str] = None
    inception_date: Optional[date] = None
    expense_ratio: Optional[float] = None
    aum: Optional[float] = None
    nav: Optional[float] = None
    nav_date: Optional[date] = None
    exit_load: Optional[float] = None
    fund_manager: Optional[str] = None
    rating: Optional[str] = None

class MutualFundCreate(MutualFundBase):
    pass

class MutualFundOut(MutualFundBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True 
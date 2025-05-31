from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class InvestmentBase(BaseModel):
    portfolio_id: UUID
    mutual_fund_id: UUID
    investment_date: date
    amount_invested: float
    nav_at_investment: float
    units_allotted: float
    current_value: Optional[float] = None
    returns_since_investment: Optional[float] = None

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentOut(InvestmentBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True 
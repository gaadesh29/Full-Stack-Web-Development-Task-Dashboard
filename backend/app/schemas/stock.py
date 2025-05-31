from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class StockBase(BaseModel):
    symbol: str
    name: str
    sector_id: UUID
    market_cap_category: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockOut(StockBase):
    id: UUID

    class Config:
        orm_mode = True 
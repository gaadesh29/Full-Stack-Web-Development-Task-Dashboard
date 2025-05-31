from pydantic import BaseModel
from uuid import UUID

class SectorBase(BaseModel):
    name: str

class SectorCreate(SectorBase):
    pass

class SectorOut(SectorBase):
    id: UUID

    class Config:
        orm_mode = True 
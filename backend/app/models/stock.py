from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    sector_id = Column(UUID(as_uuid=True), ForeignKey('sectors.id'))
    market_cap_category = Column(String(20)) 
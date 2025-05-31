from sqlalchemy import Column, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base

class FundMarketCapAllocation(Base):
    __tablename__ = 'fund_marketcap_allocations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mutual_fund_id = Column(UUID(as_uuid=True), ForeignKey('mutual_funds.id', ondelete='CASCADE'))
    large_cap_percent = Column(Numeric(5,2))
    mid_cap_percent = Column(Numeric(5,2))
    small_cap_percent = Column(Numeric(5,2))
    as_of_date = Column(Date) 
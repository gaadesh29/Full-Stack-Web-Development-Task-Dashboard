from sqlalchemy import Column, Date, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.models.base import Base

class Investment(Base):
    __tablename__ = 'investments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id', ondelete='CASCADE'))
    mutual_fund_id = Column(UUID(as_uuid=True), ForeignKey('mutual_funds.id', ondelete='CASCADE'))
    investment_date = Column(Date, nullable=False)
    amount_invested = Column(Numeric, nullable=False)
    nav_at_investment = Column(Numeric, nullable=False)
    units_allotted = Column(Numeric, nullable=False)
    current_value = Column(Numeric)
    returns_since_investment = Column(Numeric)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
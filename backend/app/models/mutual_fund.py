from sqlalchemy import Column, String, Date, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.models.base import Base

class MutualFund(Base):
    __tablename__ = 'mutual_funds'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    isin = Column(String(20), unique=True, nullable=False)
    amc = Column(String(100))
    fund_type = Column(String(50))
    category = Column(String(50))
    benchmark = Column(String(100))
    risk_level = Column(String(20))
    inception_date = Column(Date)
    expense_ratio = Column(Numeric(5,2))
    aum = Column(Numeric)
    nav = Column(Numeric)
    nav_date = Column(Date)
    exit_load = Column(Numeric(5,2))
    fund_manager = Column(String(100))
    rating = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
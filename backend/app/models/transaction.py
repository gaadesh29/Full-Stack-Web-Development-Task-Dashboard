from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    investment_id = Column(UUID(as_uuid=True), ForeignKey('investments.id', ondelete='CASCADE'))
    type = Column(String(20), nullable=False)
    amount = Column(Numeric, nullable=False)
    nav = Column(Numeric)
    units = Column(Numeric)
    date = Column(Date, nullable=False) 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func, Index
from datetime import datetime

Base = declarative_base() 

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# Common indexes
def create_common_indexes(table_name: str, columns: list):
    """Create common indexes for a table."""
    indexes = []
    for column in columns:
        indexes.append(Index(f'idx_{table_name}_{column}', column))
    return indexes

# Example usage in models:
"""
class User(Base, TimestampMixin):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    
    # Create indexes
    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_created_at', 'created_at'),
    )
""" 
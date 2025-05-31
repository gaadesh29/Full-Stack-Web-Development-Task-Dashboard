import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Index, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Database URL for Supabase
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/yourdb")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    portfolios = relationship("Portfolio", back_populates="user")

# Portfolio model
class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio")

# Transaction model
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    amount = Column(Float)
    price = Column(Float)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    portfolio = relationship("Portfolio", back_populates="transactions")

# Indexes for performance
Index("idx_user_username", User.username)
Index("idx_user_email", User.email)
Index("idx_portfolio_user_id", Portfolio.user_id)
Index("idx_transaction_portfolio_id", Transaction.portfolio_id)

# Function to create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
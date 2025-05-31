from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db, User, Portfolio, Transaction, create_tables
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Secret key for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User model
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Portfolio model
class PortfolioBase(BaseModel):
    name: str

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Transaction model
class TransactionBase(BaseModel):
    type: str
    amount: float
    price: float

class TransactionCreate(TransactionBase):
    portfolio_id: int

class Transaction(TransactionBase):
    id: int
    portfolio_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
@limiter.limit("10/minute")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/users/", response_model=User)
@limiter.limit("3/minute")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/portfolios/", response_model=List[Portfolio])
@limiter.limit("10/minute")
def read_portfolios(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
        logger.info(f"Retrieved {len(portfolios)} portfolios for user {current_user.username}")
        return portfolios
    except Exception as e:
        logger.error(f"Error retrieving portfolios: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/portfolios/", response_model=Portfolio)
@limiter.limit("5/minute")
def create_portfolio(portfolio: PortfolioCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        db_portfolio = Portfolio(name=portfolio.name, user_id=current_user.id)
        db.add(db_portfolio)
        db.commit()
        db.refresh(db_portfolio)
        logger.info(f"Created portfolio {db_portfolio.name} for user {current_user.username}")
        return db_portfolio
    except Exception as e:
        logger.error(f"Error creating portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/transactions/", response_model=List[Transaction])
@limiter.limit("10/minute")
def read_transactions(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        transactions = db.query(Transaction).join(Portfolio).filter(Portfolio.user_id == current_user.id).all()
        logger.info(f"Retrieved {len(transactions)} transactions for user {current_user.username}")
        return transactions
    except Exception as e:
        logger.error(f"Error retrieving transactions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/transactions/", response_model=Transaction)
@limiter.limit("5/minute")
def create_transaction(transaction: TransactionCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        portfolio = db.query(Portfolio).filter(Portfolio.id == transaction.portfolio_id, Portfolio.user_id == current_user.id).first()
        if not portfolio:
            logger.warning(f"Portfolio {transaction.portfolio_id} not found for user {current_user.username}")
            raise HTTPException(status_code=404, detail="Portfolio not found")
        db_transaction = Transaction(**transaction.dict())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        logger.info(f"Created transaction for portfolio {portfolio.name} for user {current_user.username}")
        return db_transaction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/readme")
async def readme():
    return {
        "title": "FastAPI Backend API",
        "description": "This API provides endpoints for user management, portfolio management, and transaction management.",
        "endpoints": {
            "/token": "Login to get access token",
            "/users/me": "Get current user information",
            "/users/": "Create a new user",
            "/portfolios/": "Get all portfolios for the current user",
            "/portfolios/": "Create a new portfolio",
            "/transactions/": "Get all transactions for the current user",
            "/transactions/": "Create a new transaction",
            "/health": "Check the health of the API",
            "/readme": "Get information about the API"
        }
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend!"} 
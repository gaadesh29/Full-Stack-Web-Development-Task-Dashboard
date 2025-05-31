from fastapi import FastAPI
from app.api import portfolio
from app.api import auth

app = FastAPI()

app.include_router(portfolio.router, prefix="/api/portfolio")
app.include_router(auth.router, prefix="/api/auth")
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .core.error_handlers import error_handler, AppError
from .api import auth, portfolio, investments
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Investment Portfolio API",
    description="""
    A comprehensive API for managing investment portfolios, mutual funds, and transactions.
    
    ## Features
    * User authentication and authorization
    * Portfolio management
    * Investment tracking
    * Transaction history
    * Performance analytics
    
    ## Authentication
    All endpoints require JWT authentication. Include the token in the Authorization header:
    ```
    Authorization: Bearer <your_token>
    ```
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Authentication operations",
        },
        {
            "name": "portfolio",
            "description": "Portfolio management operations",
        },
        {
            "name": "investments",
            "description": "Investment tracking operations",
        },
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handler
app.add_exception_handler(AppError, error_handler)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(investments.router, prefix="/api/investments", tags=["investments"])

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API status.
    
    Returns:
        dict: API status information
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "development"
    }

# Log startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Investment Portfolio API")

# Log shutdown
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Investment Portfolio API")
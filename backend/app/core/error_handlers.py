from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from typing import Union
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

async def error_handler(request: Request, exc: Union[AppError, Exception]) -> JSONResponse:
    """Global error handler for the application."""
    if isinstance(exc, AppError):
        logger.error(f"Application error: {exc.code} - {exc.message}", extra={
            'code': exc.code,
            'details': exc.details,
            'path': request.url.path,
            'method': request.method
        })
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'error': {
                    'code': exc.code,
                    'message': exc.message,
                    'details': exc.details
                }
            }
        )
    
    if isinstance(exc, SQLAlchemyError):
        logger.error(f"Database error: {str(exc)}", extra={
            'path': request.url.path,
            'method': request.method,
            'traceback': traceback.format_exc()
        })
        return JSONResponse(
            status_code=500,
            content={
                'error': {
                    'code': 'DATABASE_ERROR',
                    'message': 'An error occurred while accessing the database'
                }
            }
        )
    
    # Handle unexpected errors
    logger.error(f"Unexpected error: {str(exc)}", extra={
        'path': request.url.path,
        'method': request.method,
        'traceback': traceback.format_exc()
    })
    return JSONResponse(
        status_code=500,
        content={
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'An unexpected error occurred'
            }
        }
    )

# Custom error classes
class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication failed", details: dict = None):
        super().__init__("AUTH_ERROR", message, 401, details)

class AuthorizationError(AppError):
    def __init__(self, message: str = "Not authorized", details: dict = None):
        super().__init__("FORBIDDEN", message, 403, details)

class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed", details: dict = None):
        super().__init__("VALIDATION_ERROR", message, 400, details)

class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__("NOT_FOUND", message, 404, details)

class ConflictError(AppError):
    def __init__(self, message: str = "Resource conflict", details: dict = None):
        super().__init__("CONFLICT", message, 409, details) 
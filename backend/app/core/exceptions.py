from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union, Dict, Any
from loguru import logger

# Custom exception classes
class DatabaseError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class AIServiceError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class AuthenticationError(Exception):
    def __init__(self, detail: str = "Authentication failed"):
        self.detail = detail

# Exception handlers
async def database_exception_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "database_error",
            "detail": exc.detail,
        },
    )

async def ai_service_exception_handler(request: Request, exc: AIServiceError):
    logger.error(f"AI Service error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "ai_service_error",
            "detail": exc.detail,
        },
    )

async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "authentication_error",
            "detail": exc.detail,
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        error_detail = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        errors.append(error_detail)
    
    logger.warning(f"Validation error: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "detail": "Invalid request parameters",
            "errors": errors,
        },
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "detail": exc.detail,
        },
        headers=exc.headers,
    )

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "detail": "An unexpected error occurred",
        },
    )

def setup_exception_handlers(app):
    """Register all exception handlers with the FastAPI app"""
    app.add_exception_handler(DatabaseError, database_exception_handler)
    app.add_exception_handler(AIServiceError, ai_service_exception_handler)
    app.add_exception_handler(AuthenticationError, authentication_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
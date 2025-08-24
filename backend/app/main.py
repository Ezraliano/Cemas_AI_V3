from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import user, auth, chat
from app.core.database import Base, engine
from app.core.config import settings
from app.core.docs import setup_docs
from app.core.exceptions import setup_exception_handlers
from loguru import logger
import os

# Create tables in DB
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)

# Setup API documentation
setup_docs(app)

# Setup exception handlers
setup_exception_handlers(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_path, exist_ok=True)
logger.add(
    os.path.join(log_path, "app.log"),
    rotation="10 MB",
    retention="1 week",
    level="INFO"
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api", tags=["Users"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "status": "online",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

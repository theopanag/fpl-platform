"""
FPL Analytics Platform Backend

FastAPI application providing REST API for Fantasy Premier League analytics.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    logger.info("Starting FPL Analytics Backend...")

    # Create database tables
    await create_tables()
    logger.info("Database tables created/verified")

    yield

    logger.info("Shutting down FPL Analytics Backend...")


app = FastAPI(
    title="FPL Analytics API",
    description="REST API for Fantasy Premier League analytics and insights",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "fpl-backend"}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "FPL Analytics Backend API",
        "docs": "/docs",
        "version": "0.1.0"
    }
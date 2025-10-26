"""
AUREX.AI - FastAPI Backend Main Application.

This module initializes the FastAPI application and configures
all routes, middleware, and dependencies.
"""

import sys
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

try:
    # Try Docker/production import
    from backend.app.api.v1 import api_router
except ModuleNotFoundError:
    # Fall back to local development import
    from app.api.v1 import api_router
from packages.shared.config import config
from packages.shared.logging_config import setup_logging


# Configure logging
setup_logging("aurex-backend", log_level=config.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("=" * 80)
    logger.info("AUREX.AI Backend Starting...")
    logger.info("=" * 80)
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Debug Mode: {config.DEBUG}")
    logger.info(f"API Host: {config.API_HOST}:{config.API_PORT}")
    logger.info(f"Database: {config.DATABASE_URL.split('@')[1]}")
    logger.info("=" * 80)

    yield

    logger.info("AUREX.AI Backend Shutting Down...")


# Create FastAPI application
app = FastAPI(
    title="AUREX.AI API",
    description="AI-Driven Financial Sentiment Analysis & XAUUSD Price Prediction",
    version=config.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GZip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code}")
    return response


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": request.url.path,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Internal server error",
            "path": request.url.path,
        },
    )


# Include API router
app.include_router(api_router)


# Root endpoint
@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint returning API information."""
    return {
        "name": "AUREX.AI API",
        "version": config.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower(),
    )

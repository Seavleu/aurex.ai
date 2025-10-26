"""
AUREX.AI - FastAPI Backend Main Application.

This module initializes the FastAPI application and configures
all routes, middleware, and dependencies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Application metadata
app = FastAPI(
    title="AUREX.AI API",
    description="AI-Driven Financial Sentiment Analysis & XAUUSD Price Prediction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://aurex-ai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint returning API information."""
    return {
        "name": "AUREX.AI API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "aurex-backend",
            "version": "1.0.0",
        },
        status_code=200,
    )


@app.get("/sentiment/latest")
async def get_latest_sentiment() -> dict[str, str | float]:
    """Get latest sentiment analysis summary."""
    # TODO: Implement in Sprint 2
    return {
        "message": "Sentiment endpoint - Coming in Sprint 2",
        "avg_sentiment": 0.0,
        "status": "not_implemented",
    }


@app.get("/price/current")
async def get_current_price() -> dict[str, str | float]:
    """Get current XAUUSD price."""
    # TODO: Implement in Sprint 2
    return {
        "message": "Price endpoint - Coming in Sprint 2",
        "symbol": "XAUUSD",
        "price": 0.0,
        "status": "not_implemented",
    }


@app.get("/news/recent")
async def get_recent_news() -> dict[str, str | list]:
    """Get recent news headlines with sentiment."""
    # TODO: Implement in Sprint 2
    return {
        "message": "News endpoint - Coming in Sprint 2",
        "news": [],
        "status": "not_implemented",
    }


@app.get("/correlation")
async def get_correlation() -> dict[str, str | float]:
    """Get sentiment-price correlation analysis."""
    # TODO: Implement in Sprint 4
    return {
        "message": "Correlation endpoint - Coming in Sprint 4",
        "correlation": 0.0,
        "status": "not_implemented",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


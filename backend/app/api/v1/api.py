"""
API v1 router configuration.

Main router for API version 1 endpoints.
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.api.v1.endpoints import analytics, leagues, managers
from app.services.fpl_api import FPLAPIService

api_router = APIRouter()

# Bootstrap endpoint
@api_router.get("/bootstrap")
async def get_bootstrap() -> Any:
    """Get general FPL game information including current gameweek."""
    try:
        fpl_service = FPLAPIService()
        bootstrap_data = await fpl_service.get_bootstrap_static()

        if not bootstrap_data:
            raise HTTPException(status_code=500, detail="Failed to fetch bootstrap data")

        return bootstrap_data

    except Exception as e:
        logger.error(f"Error fetching bootstrap data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Include endpoint routers
api_router.include_router(leagues.router, prefix="/leagues", tags=["leagues"])
api_router.include_router(managers.router, prefix="/managers", tags=["managers"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
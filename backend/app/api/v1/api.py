"""
API v1 router configuration.

Main router for API version 1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import analytics, leagues, managers

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(leagues.router, prefix="/leagues", tags=["leagues"])
api_router.include_router(managers.router, prefix="/managers", tags=["managers"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
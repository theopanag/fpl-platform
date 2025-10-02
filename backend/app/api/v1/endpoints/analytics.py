"""
Analytics endpoints for FPL API.

Handles analytics operations including performance comparisons,
head-to-head analysis, and league-wide statistics.
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.api.deps import SessionDep
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/compare")
async def compare_managers(
    manager1_id: int,
    manager2_id: int,
    gameweek_start: int | None = None,
    gameweek_end: int | None = None,
    db: SessionDep = None,
) -> Any:
    """Compare two managers' performance."""
    try:
        analytics_service = AnalyticsService()
        comparison = await analytics_service.compare_managers(
            manager1_id, manager2_id, gameweek_start, gameweek_end
        )

        return comparison

    except Exception as e:
        logger.error(f"Error comparing managers {manager1_id} vs {manager2_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/league/{league_id}/summary")
async def get_league_analytics(
    league_id: int,
    gameweek: int | None = None,
    db: SessionDep = None,
) -> Any:
    """Get comprehensive analytics for a league."""
    try:
        analytics_service = AnalyticsService()
        summary = await analytics_service.get_league_summary(league_id, gameweek)

        return summary

    except Exception as e:
        logger.error(f"Error getting analytics for league {league_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/league/{league_id}/transfers")
async def get_league_transfer_trends(
    league_id: int,
    gameweek: int | None = None,
    db: SessionDep = None,
) -> Any:
    """Get transfer trends within a league."""
    try:
        analytics_service = AnalyticsService()
        trends = await analytics_service.get_league_transfer_trends(league_id, gameweek)

        return trends

    except Exception as e:
        logger.error(f"Error getting transfer trends for league {league_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/league/{league_id}/captaincy")
async def get_league_captaincy_analysis(
    league_id: int,
    gameweek: int | None = None,
    db: SessionDep = None,
) -> Any:
    """Get captaincy analysis for a league."""
    try:
        analytics_service = AnalyticsService()
        analysis = await analytics_service.get_captaincy_analysis(league_id, gameweek)

        return analysis

    except Exception as e:
        logger.error(f"Error getting captaincy analysis for league {league_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
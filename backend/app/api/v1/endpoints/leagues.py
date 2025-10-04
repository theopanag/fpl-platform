"""
League endpoints for FPL API.

Handles league-related operations including fetching league data,
standings, and league-wide analytics.
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.api.deps import SessionDep
from app.schemas.league import League, LeagueStandings
from app.services.fpl_api import FPLAPIService

router = APIRouter()


@router.get("/{league_id}", response_model=League)
async def get_league(
    league_id: int,
    db: SessionDep,
) -> Any:
    """Get league information by ID."""
    try:
        fpl_service = FPLAPIService()
        league_data = await fpl_service.get_league(league_id)

        if not league_data:
            raise HTTPException(status_code=404, detail="League not found")

        return league_data

    except Exception as e:
        logger.error(f"Error fetching league {league_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{league_id}/standings", response_model=LeagueStandings)
async def get_league_standings(
    league_id: int,
    gameweek: int | None = None,
    db: SessionDep = None,
) -> Any:
    """Get league standings for a specific gameweek."""
    try:
        fpl_service = FPLAPIService()
        
        # If gameweek is specified, fetch historical data
        if gameweek:
            logger.info(f"Fetching historical standings for league {league_id}, GW {gameweek}")
            standings = await fpl_service.get_historical_league_standings(league_id, gameweek)
        else:
            # Otherwise get current standings
            standings = await fpl_service.get_league_standings(league_id, gameweek)

        if not standings:
            raise HTTPException(status_code=404, detail="Standings not found")

        return standings

    except Exception as e:
        logger.error(f"Error fetching standings for league {league_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{league_id}/history")
async def get_league_history(
    league_id: int,
    db: SessionDep,
) -> Any:
    """Get historical performance data for the league."""
    try:
        fpl_service = FPLAPIService()
        history = await fpl_service.get_league_history(league_id)

        return {"league_id": league_id, "history": history}

    except Exception as e:
        logger.error(f"Error fetching history for league {league_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
"""
Manager endpoints for FPL API.

Handles manager-related operations including fetching manager data,
team information, and individual performance analytics.
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.api.deps import SessionDep
from app.schemas.manager import Manager, ManagerTeam, ManagerHistory
from app.services.fpl_api import FPLAPIService

router = APIRouter()


@router.get("/{manager_id}", response_model=Manager)
async def get_manager(
    manager_id: int,
    db: SessionDep,
) -> Any:
    """Get manager information by ID."""
    try:
        fpl_service = FPLAPIService()
        manager_data = await fpl_service.get_manager(manager_id)

        if not manager_data:
            raise HTTPException(status_code=404, detail="Manager not found")

        return manager_data

    except Exception as e:
        logger.error(f"Error fetching manager {manager_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{manager_id}/team", response_model=ManagerTeam)
async def get_manager_team(
    manager_id: int,
    gameweek: int | None = None,
    db: SessionDep = None,
) -> Any:
    """Get manager's team for a specific gameweek."""
    try:
        fpl_service = FPLAPIService()
        team_data = await fpl_service.get_manager_team(manager_id, gameweek)

        if not team_data:
            raise HTTPException(status_code=404, detail="Team data not found")

        return team_data

    except Exception as e:
        logger.error(f"Error fetching team for manager {manager_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{manager_id}/history", response_model=ManagerHistory)
async def get_manager_history(
    manager_id: int,
    db: SessionDep,
) -> Any:
    """Get manager's historical performance data."""
    try:
        fpl_service = FPLAPIService()
        history = await fpl_service.get_manager_history(manager_id)

        if not history:
            raise HTTPException(status_code=404, detail="Manager history not found")

        return history

    except Exception as e:
        logger.error(f"Error fetching history for manager {manager_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{manager_id}/transfers")
async def get_manager_transfers(
    manager_id: int,
    gameweek: int | None = None,
    db: SessionDep = None,
) -> Any:
    """Get manager's transfer history."""
    try:
        fpl_service = FPLAPIService()
        transfers = await fpl_service.get_manager_transfers(manager_id, gameweek)

        return {"manager_id": manager_id, "transfers": transfers}

    except Exception as e:
        logger.error(f"Error fetching transfers for manager {manager_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
"""
Manager Pydantic schemas for API serialization.

Request and response models for manager-related endpoints.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ManagerBase(BaseModel):
    """Base manager schema."""

    first_name: str
    last_name: str
    player_first_name: str
    player_last_name: str
    player_region_name: str
    player_region_id: int
    player_region_short_iso: str
    summary_overall_points: int = 0
    summary_overall_rank: int | None = None
    summary_event_points: int = 0
    summary_event_rank: int | None = None
    current_event: int = 1
    total_transfers: int = 0


class Manager(ManagerBase):
    """Manager response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    fpl_id: int
    league_id: int | None = None
    created_at: datetime
    updated_at: datetime


class ManagerCreate(ManagerBase):
    """Manager creation schema."""

    fpl_id: int
    league_id: int | None = None


class ManagerTeamPick(BaseModel):
    """Individual player pick in manager's team."""

    element: int
    position: int
    multiplier: int
    is_captain: bool
    is_vice_captain: bool


class ManagerTeam(BaseModel):
    """Manager's team for a specific gameweek."""

    picks: list[ManagerTeamPick]
    chips: list[str]
    transfers: dict[str, Any]


class ManagerGameweekHistory(BaseModel):
    """Manager's performance for a single gameweek."""

    event: int
    points: int
    total_points: int
    rank: int | None
    rank_sort: int | None
    overall_rank: int | None
    bank: int
    value: int
    event_transfers: int
    event_transfers_cost: int
    points_on_bench: int


class ManagerHistory(BaseModel):
    """Manager's complete historical performance."""

    manager_id: int
    current_season: list[ManagerGameweekHistory]
    past_seasons: list[dict[str, Any]]
    chips: list[dict[str, Any]]
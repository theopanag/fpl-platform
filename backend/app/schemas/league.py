"""
League Pydantic schemas for API serialization.

Request and response models for league-related endpoints.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class LeagueBase(BaseModel):
    """Base league schema."""

    name: str
    league_type: str
    scoring: str
    start_event: int
    code_privacy: str
    admin_entry: int | None = None
    rank: int | None = None


class League(LeagueBase):
    """League response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    fpl_id: int
    created_at: datetime
    updated_at: datetime


class LeagueCreate(LeagueBase):
    """League creation schema."""

    fpl_id: int


class LeagueStandingEntry(BaseModel):
    """Individual entry in league standings."""

    id: int
    entry_name: str
    player_first_name: str
    player_last_name: str
    rank: int
    last_rank: int
    rank_sort: int
    total: int
    entry: int
    event_total: int


class LeagueStandings(BaseModel):
    """League standings response schema."""

    league: League
    standings: dict[str, Any]
    new_entries: list[LeagueStandingEntry]
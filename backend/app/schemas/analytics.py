"""
Analytics Pydantic schemas for API serialization.

Request and response models for analytics-related endpoints.
"""

from typing import Any

from pydantic import BaseModel


class ManagerComparison(BaseModel):
    """Manager comparison analytics schema."""

    manager1_id: int
    manager2_id: int
    gameweek_start: int | None = None
    gameweek_end: int | None = None
    total_points_comparison: dict[str, int]
    average_points_comparison: dict[str, float]
    captain_success_rate: dict[str, float]
    transfer_efficiency: dict[str, float]
    bench_points: dict[str, int]
    head_to_head_record: dict[str, int]


class LeagueSummary(BaseModel):
    """League-wide analytics summary."""

    league_id: int
    gameweek: int | None = None
    total_managers: int
    average_points: float
    highest_points: int
    lowest_points: int
    most_captained_player: dict[str, Any]
    most_transferred_in: list[dict[str, Any]]
    most_transferred_out: list[dict[str, Any]]
    chip_usage: dict[str, int]


class TransferTrend(BaseModel):
    """Transfer trend data for a player."""

    player_id: int
    player_name: str
    transfers_in: int
    transfers_out: int
    net_transfers: int
    ownership_percentage: float


class LeagueTransferTrends(BaseModel):
    """League transfer trends summary."""

    league_id: int
    gameweek: int | None = None
    most_transferred_in: list[TransferTrend]
    most_transferred_out: list[TransferTrend]
    total_transfers: int
    average_transfers_per_manager: float


class CaptainChoice(BaseModel):
    """Captain choice data."""

    player_id: int
    player_name: str
    times_captained: int
    total_points: int
    average_points: float
    success_rate: float


class CaptaincyAnalysis(BaseModel):
    """Captaincy analysis for a league."""

    league_id: int
    gameweek: int | None = None
    most_popular_captain: CaptainChoice
    most_effective_captain: CaptainChoice
    captain_choices: list[CaptainChoice]
    differential_captains: list[CaptainChoice]
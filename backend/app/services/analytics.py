"""
Analytics service for computing FPL insights and comparisons.

Handles complex analytics calculations and aggregations.
"""

from typing import Any

from loguru import logger

from app.services.fpl_api import FPLAPIService


class AnalyticsService:
    """Service for computing FPL analytics and insights."""

    def __init__(self):
        self.fpl_service = FPLAPIService()

    async def compare_managers(
        self,
        manager1_id: int,
        manager2_id: int,
        gameweek_start: int | None = None,
        gameweek_end: int | None = None,
    ) -> dict[str, Any]:
        """Compare performance between two managers."""
        try:
            # Get manager data
            manager1_data = await self.fpl_service.get_manager(manager1_id)
            manager2_data = await self.fpl_service.get_manager(manager2_id)

            if not manager1_data or not manager2_data:
                return {"error": "One or more managers not found"}

            # Get historical data
            manager1_history = await self.fpl_service.get_manager_history(manager1_id)
            manager2_history = await self.fpl_service.get_manager_history(manager2_id)

            # Filter by gameweek range if provided
            m1_current = manager1_history.get("current", []) if manager1_history else []
            m2_current = manager2_history.get("current", []) if manager2_history else []

            if gameweek_start or gameweek_end:
                m1_current = [
                    gw for gw in m1_current
                    if (not gameweek_start or gw["event"] >= gameweek_start) and
                       (not gameweek_end or gw["event"] <= gameweek_end)
                ]
                m2_current = [
                    gw for gw in m2_current
                    if (not gameweek_start or gw["event"] >= gameweek_start) and
                       (not gameweek_end or gw["event"] <= gameweek_end)
                ]

            # Calculate comparison metrics
            m1_total_points = sum(gw["points"] for gw in m1_current)
            m2_total_points = sum(gw["points"] for gw in m2_current)

            m1_avg_points = m1_total_points / len(m1_current) if m1_current else 0
            m2_avg_points = m2_total_points / len(m2_current) if m2_current else 0

            return {
                "manager1_id": manager1_id,
                "manager2_id": manager2_id,
                "gameweek_start": gameweek_start,
                "gameweek_end": gameweek_end,
                "total_points_comparison": {
                    "manager1": m1_total_points,
                    "manager2": m2_total_points,
                },
                "average_points_comparison": {
                    "manager1": round(m1_avg_points, 2),
                    "manager2": round(m2_avg_points, 2),
                },
                "head_to_head_record": {
                    "manager1_wins": 0,  # TODO: Calculate from gameweek data
                    "manager2_wins": 0,
                    "draws": 0,
                },
            }

        except Exception as e:
            logger.error(f"Error comparing managers {manager1_id} vs {manager2_id}: {e}")
            return {"error": "Failed to compare managers"}

    async def get_league_summary(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any]:
        """Get comprehensive analytics summary for a league."""
        try:
            # Get league data
            league_data = await self.fpl_service.get_league_standings(league_id, gameweek)
            if not league_data:
                return {"error": "League not found"}

            standings = league_data.get("standings", {}).get("results", [])
            if not standings:
                return {"error": "No standings data found"}

            # Calculate summary statistics
            points_list = [entry.get("event_total", 0) for entry in standings]
            total_managers = len(standings)
            average_points = sum(points_list) / total_managers if total_managers > 0 else 0
            highest_points = max(points_list) if points_list else 0
            lowest_points = min(points_list) if points_list else 0

            return {
                "league_id": league_id,
                "gameweek": gameweek,
                "total_managers": total_managers,
                "average_points": round(average_points, 2),
                "highest_points": highest_points,
                "lowest_points": lowest_points,
                "most_captained_player": {},  # TODO: Implement
                "most_transferred_in": [],    # TODO: Implement
                "most_transferred_out": [],   # TODO: Implement
                "chip_usage": {},             # TODO: Implement
            }

        except Exception as e:
            logger.error(f"Error getting league summary for {league_id}: {e}")
            return {"error": "Failed to get league summary"}

    async def get_league_transfer_trends(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any]:
        """Get transfer trends within a league."""
        try:
            # This would require analyzing transfer data for all managers in the league
            # For now, return placeholder data
            return {
                "league_id": league_id,
                "gameweek": gameweek,
                "most_transferred_in": [],
                "most_transferred_out": [],
                "total_transfers": 0,
                "average_transfers_per_manager": 0.0,
            }

        except Exception as e:
            logger.error(f"Error getting transfer trends for league {league_id}: {e}")
            return {"error": "Failed to get transfer trends"}

    async def get_captaincy_analysis(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any]:
        """Get captaincy analysis for a league."""
        try:
            # This would require analyzing team picks for all managers in the league
            # For now, return placeholder data
            return {
                "league_id": league_id,
                "gameweek": gameweek,
                "most_popular_captain": {},
                "most_effective_captain": {},
                "captain_choices": [],
                "differential_captains": [],
            }

        except Exception as e:
            logger.error(f"Error getting captaincy analysis for league {league_id}: {e}")
            return {"error": "Failed to get captaincy analysis"}
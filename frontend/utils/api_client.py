"""
API client for communicating with the backend service.

Handles HTTP requests to the FastAPI backend.
"""

import logging
from typing import Any

import requests


class APIClient:
    """Client for making requests to the FPL Analytics backend API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        # Set up logging
        self.logger = logging.getLogger(__name__)

    def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> dict[str, Any] | None:
        """Make HTTP request to the API."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {method} {url} - {e}")
            return None
        except ValueError as e:
            self.logger.error(f"JSON decode error: {e}")
            return None

    def get_health(self) -> dict[str, Any] | None:
        """Check API health status."""
        return self._make_request("GET", "/health")

    def get_league(self, league_id: int) -> dict[str, Any] | None:
        """Get league information."""
        return self._make_request("GET", f"/api/v1/leagues/{league_id}")

    def get_league_standings(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get league standings."""
        endpoint = f"/api/v1/leagues/{league_id}/standings"
        params = {}
        if gameweek:
            params["gameweek"] = gameweek

        return self._make_request("GET", endpoint, params=params)

    def get_league_history(self, league_id: int) -> dict[str, Any] | None:
        """Get league history."""
        return self._make_request("GET", f"/api/v1/leagues/{league_id}/history")

    def get_manager(self, manager_id: int) -> dict[str, Any] | None:
        """Get manager information."""
        return self._make_request("GET", f"/api/v1/managers/{manager_id}")

    def get_manager_team(
        self, manager_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get manager's team."""
        endpoint = f"/api/v1/managers/{manager_id}/team"
        params = {}
        if gameweek:
            params["gameweek"] = gameweek

        return self._make_request("GET", endpoint, params=params)

    def get_manager_history(self, manager_id: int) -> dict[str, Any] | None:
        """Get manager history."""
        return self._make_request("GET", f"/api/v1/managers/{manager_id}/history")

    def get_manager_transfers(
        self, manager_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get manager transfers."""
        endpoint = f"/api/v1/managers/{manager_id}/transfers"
        params = {}
        if gameweek:
            params["gameweek"] = gameweek

        return self._make_request("GET", endpoint, params=params)

    def compare_managers(
        self,
        manager1_id: int,
        manager2_id: int,
        gameweek_start: int | None = None,
        gameweek_end: int | None = None,
    ) -> dict[str, Any] | None:
        """Compare two managers."""
        params = {
            "manager1_id": manager1_id,
            "manager2_id": manager2_id,
        }
        if gameweek_start:
            params["gameweek_start"] = gameweek_start
        if gameweek_end:
            params["gameweek_end"] = gameweek_end

        return self._make_request("GET", "/api/v1/analytics/compare", params=params)

    def get_league_analytics(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get league analytics summary."""
        endpoint = f"/api/v1/analytics/league/{league_id}/summary"
        params = {}
        if gameweek:
            params["gameweek"] = gameweek

        return self._make_request("GET", endpoint, params=params)

    def get_transfer_trends(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get transfer trends for league."""
        endpoint = f"/api/v1/analytics/league/{league_id}/transfers"
        params = {}
        if gameweek:
            params["gameweek"] = gameweek

        return self._make_request("GET", endpoint, params=params)

    def get_captaincy_analysis(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get captaincy analysis for league."""
        endpoint = f"/api/v1/analytics/league/{league_id}/captaincy"
        params = {}
        if gameweek:
            params["gameweek"] = gameweek

        return self._make_request("GET", endpoint, params=params)
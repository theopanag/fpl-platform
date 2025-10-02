"""
FPL API service for fetching data from the official Fantasy Premier League API.

Handles API requests, response parsing, and data transformation.
"""

from typing import Any

import httpx
from loguru import logger

from app.core.config import settings
from app.services.cache import CacheService


class FPLAPIService:
    """Service for interacting with the FPL API."""

    def __init__(self):
        self.base_url = settings.FPL_API_BASE_URL
        self.cache = CacheService()
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _get(self, endpoint: str) -> dict[str, Any] | None:
        """Make GET request to FPL API with caching."""
        cache_key = f"fpl_api:{endpoint}"

        # Try cache first
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            logger.debug(f"Cache hit for {endpoint}")
            return cached_data

        try:
            url = f"{self.base_url}{endpoint}"
            logger.debug(f"Fetching from FPL API: {url}")

            response = await self.client.get(url)
            response.raise_for_status()

            data = response.json()

            # Cache the response
            await self.cache.set(
                cache_key, data, expire=settings.FPL_CACHE_DURATION
            )

            return data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching {endpoint}: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error fetching {endpoint}: {e}")
            return None

    async def get_bootstrap_static(self) -> dict[str, Any] | None:
        """Get general game information."""
        return await self._get("/bootstrap-static/")

    async def get_league(self, league_id: int) -> dict[str, Any] | None:
        """Get league information."""
        return await self._get(f"/leagues-classic/{league_id}/standings/")

    async def get_league_standings(
        self, league_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get league standings for a specific gameweek."""
        endpoint = f"/leagues-classic/{league_id}/standings/"
        if gameweek:
            endpoint += f"?page_standings=1&page_new_entries=1&event={gameweek}"

        return await self._get(endpoint)

    async def get_league_history(self, league_id: int) -> list[dict[str, Any]] | None:
        """Get historical performance data for the league."""
        # Note: FPL API doesn't have a direct league history endpoint
        # This would need to be constructed from individual manager histories
        # For now, return empty list
        return []

    async def get_manager(self, manager_id: int) -> dict[str, Any] | None:
        """Get manager information."""
        return await self._get(f"/entry/{manager_id}/")

    async def get_manager_team(
        self, manager_id: int, gameweek: int | None = None
    ) -> dict[str, Any] | None:
        """Get manager's team for a specific gameweek."""
        if gameweek:
            endpoint = f"/entry/{manager_id}/event/{gameweek}/picks/"
        else:
            # Get current gameweek team
            bootstrap = await self.get_bootstrap_static()
            if not bootstrap:
                return None

            current_event = next(
                (event["id"] for event in bootstrap["events"] if event["is_current"]),
                1
            )
            endpoint = f"/entry/{manager_id}/event/{current_event}/picks/"

        return await self._get(endpoint)

    async def get_manager_history(self, manager_id: int) -> dict[str, Any] | None:
        """Get manager's historical performance."""
        return await self._get(f"/entry/{manager_id}/history/")

    async def get_manager_transfers(
        self, manager_id: int, gameweek: int | None = None
    ) -> list[dict[str, Any]] | None:
        """Get manager's transfer history."""
        endpoint = f"/entry/{manager_id}/transfers/"
        if gameweek:
            endpoint += f"?event={gameweek}"

        data = await self._get(endpoint)
        return data if data else []

    async def get_gameweek_live(self, gameweek: int) -> dict[str, Any] | None:
        """Get live gameweek data."""
        return await self._get(f"/event/{gameweek}/live/")

    async def get_fixtures(self, gameweek: int | None = None) -> list[dict[str, Any]] | None:
        """Get fixture information."""
        endpoint = "/fixtures/"
        if gameweek:
            endpoint += f"?event={gameweek}"

        return await self._get(endpoint)
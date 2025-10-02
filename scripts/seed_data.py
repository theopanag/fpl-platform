#!/usr/bin/env python3
"""
Seed script for FPL Analytics Platform

This script populates the database with sample data for testing and development.
Run this script after the database is set up to get started quickly.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.database import AsyncSessionLocal, create_tables
from app.models.league import League
from app.models.manager import Manager
from app.models.gameweek import Gameweek
from app.services.fpl_api import FPLAPIService


async def seed_sample_league(league_id: int = 314) -> None:
    """Seed database with sample league data."""
    print(f"🌱 Seeding sample data for league {league_id}...")

    async with AsyncSessionLocal() as session:
        try:
            # Initialize FPL API service
            fpl_service = FPLAPIService()

            # Fetch league data
            print("📥 Fetching league data from FPL API...")
            league_data = await fpl_service.get_league_standings(league_id)

            if not league_data:
                print(f"❌ Could not fetch data for league {league_id}")
                return

            # Create league record
            league_info = league_data.get("league", {})
            league = League(
                fpl_id=league_id,
                name=league_info.get("name", f"League {league_id}"),
                league_type="classic",
                scoring="total",
                start_event=1,
                code_privacy="public",
                admin_entry=league_info.get("admin_entry"),
                rank=league_info.get("rank"),
            )

            session.add(league)
            await session.flush()  # Get the league.id

            # Create manager records
            standings = league_data.get("standings", {}).get("results", [])
            print(f"👥 Adding {len(standings)} managers...")

            for standing in standings[:10]:  # Limit to first 10 managers
                manager = Manager(
                    fpl_id=standing["entry"],
                    first_name=standing.get("player_first_name", ""),
                    last_name=standing.get("player_last_name", ""),
                    player_first_name=standing.get("player_first_name", ""),
                    player_last_name=standing.get("player_last_name", ""),
                    player_region_name=standing.get("player_region_name", ""),
                    player_region_id=standing.get("player_region_id", 0),
                    player_region_short_iso=standing.get("player_region_short_iso", ""),
                    summary_overall_points=standing.get("total", 0),
                    summary_overall_rank=standing.get("rank", 0),
                    summary_event_points=standing.get("event_total", 0),
                    league_id=league.id,
                )

                session.add(manager)

            await session.commit()
            print("✅ Sample data seeded successfully!")
            print(f"🔗 League: {league.name}")
            print(f"👥 Managers: {len(standings[:10])}")

        except Exception as e:
            print(f"❌ Error seeding data: {e}")
            await session.rollback()
            raise

        finally:
            await fpl_service.client.aclose()


async def main():
    """Main seeding function."""
    print("🌱 FPL Analytics Platform - Data Seeder")
    print("========================================")

    # Create tables first
    print("📋 Creating database tables...")
    await create_tables()

    # Get league ID from command line or use default
    league_id = int(sys.argv[1]) if len(sys.argv) > 1 else 314

    # Seed the data
    await seed_sample_league(league_id)

    print("\n🎉 Seeding complete!")
    print("💡 You can now test the application with real FPL data.")


if __name__ == "__main__":
    asyncio.run(main())
#!/bin/bash
# View FPL Analytics Platform logs

set -e

# Default to showing all logs
SERVICE=${1:-""}

if [ -z "$SERVICE" ]; then
    echo "📋 Showing logs for all services (use Ctrl+C to exit)"
    echo "💡 Usage: ./scripts/logs.sh [service_name]"
    echo "   Available services: backend, frontend, nginx, db, redis"
    echo ""
    docker compose logs -f
else
    echo "📋 Showing logs for $SERVICE (use Ctrl+C to exit)"
    docker compose logs -f "$SERVICE"
fi
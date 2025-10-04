#!/bin/bash
# Start FPL Analytics Platform services

set -e

echo "🚀 Starting FPL Analytics Platform..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Running setup first..."
    ./scripts/setup.sh
    exit 0
fi

# Start services
docker compose up -d

echo "✅ Services started"
echo "🔗 Frontend: http://localhost:8080"
echo "🔗 API Docs: http://localhost:8080/docs"

# Show status
docker compose ps
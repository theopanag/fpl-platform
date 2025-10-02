#!/bin/bash
# Start FPL Analytics Platform in development mode

set -e

echo "🔧 Starting FPL Analytics Platform in development mode..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
fi

# Use development compose file
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

echo "✅ Development services started"
echo "🔗 Frontend: http://localhost:8050 (direct)"
echo "🔗 Backend: http://localhost:8000 (direct)"
echo "🔗 NGINX: http://localhost:8080 (proxied)"
echo "🔗 API Docs: http://localhost:8080/docs"

# Show status
docker-compose ps
#!/bin/bash
# Stop FPL Analytics Platform services

set -e

echo "🛑 Stopping FPL Analytics Platform..."

# Stop services
docker-compose down

echo "✅ Services stopped"
#!/bin/bash
# Reset FPL Analytics Platform database

set -e

echo "⚠️  Database Reset"
echo "=================="
echo "This will delete all data in the database!"
read -p "Are you sure? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Reset cancelled"
    exit 1
fi

echo "🗑️  Resetting database..."

# Stop services
docker compose down

# Remove database volume
docker volume rm fpl-platform_postgres_data 2>/dev/null || echo "ℹ️  Database volume not found"

# Start services (database will be recreated)
docker compose up -d

echo "✅ Database reset complete"
echo "🔗 Frontend: http://localhost:8080"
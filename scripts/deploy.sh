#!/bin/bash
# Deploy FPL Analytics Platform to production

set -e

echo "🚀 FPL Analytics Platform Production Deployment"
echo "==============================================="

# Check if we're in production mode
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it first."
    exit 1
fi

# Check NODE_ENV
NODE_ENV=$(grep NODE_ENV .env | cut -d '=' -f2)
if [ "$NODE_ENV" != "production" ]; then
    echo "⚠️  Warning: NODE_ENV is not set to 'production' in .env file"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Deployment cancelled"
        exit 1
    fi
fi

echo "🔄 Pulling latest changes..."
git pull origin main || echo "⚠️  Not a git repository or no changes to pull"

echo "🏗️  Building images..."
docker compose build --no-cache

echo "🔄 Starting services..."
docker compose down
docker compose up -d

echo "⏳ Waiting for services..."
sleep 10

echo "🔍 Checking service health..."
if curl -sf http://localhost:8080/health > /dev/null; then
    echo "✅ Deployment successful!"
    echo "🔗 Application: http://localhost:8080"
else
    echo "❌ Deployment failed - health check failed"
    echo "📋 Checking logs:"
    docker compose logs --tail=50
    exit 1
fi

echo "📊 Final status:"
docker compose ps
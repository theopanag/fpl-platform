#!/bin/bash
# FPL Analytics Platform Setup Script
# Initializes the development environment

set -e  # Exit on any error

echo "🏈 FPL Analytics Platform Setup"
echo "================================"

# Check if required tools are installed
check_dependencies() {
    echo "📋 Checking dependencies..."

    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    echo "✅ Dependencies check passed"
}

# Copy environment file
setup_env() {
    echo "⚙️  Setting up environment configuration..."

    if [ ! -f .env ]; then
        cp .env.example .env
        echo "✅ Created .env file from template"
        echo "⚠️  Please review and update .env file with your settings"
    else
        echo "ℹ️  .env file already exists"
    fi
}

# Build and start services
start_services() {
    echo "🚀 Building and starting services..."

    # Build images
    docker-compose build

    # Start services
    docker-compose up -d

    echo "✅ Services started successfully"
}

# Wait for services to be healthy
wait_for_services() {
    echo "⏳ Waiting for services to be ready..."

    # Wait for database
    echo "  - Waiting for database..."
    while ! docker-compose exec -T db pg_isready -U fpl_user -d fpl_analytics &> /dev/null; do
        sleep 2
    done

    # Wait for backend
    echo "  - Waiting for backend..."
    while ! curl -sf http://localhost:8000/health &> /dev/null; do
        sleep 2
    done

    # Wait for NGINX (which proxies to frontend)
    echo "  - Waiting for NGINX proxy..."
    while ! curl -sf http://localhost:8080/health &> /dev/null; do
        sleep 2
    done

    echo "✅ All services are ready"
}

# Show status
show_status() {
    echo "📊 Service Status"
    echo "=================="

    echo "🔗 Frontend:  http://localhost:8080"
    echo "🔗 API:       http://localhost:8080/api/v1"
    echo "🔗 API Docs:  http://localhost:8080/docs"
    echo "🔗 Health:    http://localhost:8080/health"
    echo ""
    echo "📊 Container Status:"
    docker-compose ps
}

# Main execution
main() {
    check_dependencies
    setup_env
    start_services
    wait_for_services
    show_status

    echo ""
    echo "🎉 Setup complete! Your FPL Analytics Platform is ready."
    echo "   Visit http://localhost:8080 to get started."
    echo ""
    echo "💡 Useful commands:"
    echo "   ./scripts/start.sh     - Start all services"
    echo "   ./scripts/stop.sh      - Stop all services"
    echo "   ./scripts/logs.sh      - View logs"
    echo "   ./scripts/reset.sh     - Reset database"
}

# Run main function
main "$@"
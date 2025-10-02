# FPL Analytics Platform

A comprehensive Fantasy Premier League analytics platform designed to provide data-driven insights for mini-league competitions. Built with FastAPI backend, Dash frontend, and containerized for easy deployment.

## 🏈 Features

- **League Analytics**: Comprehensive mini-league statistics and standings
- **Manager Analysis**: Individual manager performance tracking and insights
- **Head-to-Head Comparisons**: Direct manager comparisons with detailed metrics
- **Transfer Trends**: League-wide transfer analysis and popular picks
- **Captaincy Analysis**: Captain choice effectiveness and differentials
- **Historical Data**: Performance tracking over time
- **Real-time Updates**: Live data from the official FPL API

## 🏗️ Architecture

This project uses a containerized microservices architecture:

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   NGINX     │    │   Frontend   │    │   Backend   │
│   Proxy     │◄───│    (Dash)    │◄───│  (FastAPI)  │
└─────────────┘    └──────────────┘    └─────────────┘
       │                                       │
       ▼                                       ▼
┌─────────────┐                    ┌─────────────────────┐
│ Static      │                    │  PostgreSQL + Redis │
│ Assets      │                    │    (Database)       │
└─────────────┘                    └─────────────────────┘
```

### Components

- **Frontend** (Dash): Interactive web dashboard with responsive design
- **Backend** (FastAPI): REST API with async support and automatic documentation
- **Database** (PostgreSQL): Persistent data storage with migrations
- **Cache** (Redis): High-performance caching for FPL API responses
- **Reverse Proxy** (NGINX): Load balancing, routing, and SSL termination

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd fpl-platform
./scripts/setup.sh
```

The setup script will:
- Check dependencies
- Create `.env` from template
- Build and start all services
- Wait for services to be ready

### 2. Access the Application

- **Web Dashboard**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

### 3. Load Sample Data (Optional)

```bash
# Seed with sample league data (league ID 314)
docker-compose exec backend python /app/../scripts/seed_data.py

# Or specify your own league ID
docker-compose exec backend python /app/../scripts/seed_data.py 12345
```

## 📁 Project Structure

```
fpl-platform/
├── backend/                    # FastAPI backend service
│   ├── app/
│   │   ├── api/               # API routes and endpoints
│   │   ├── core/              # Configuration and database
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic request/response models
│   │   ├── services/          # Business logic and external APIs
│   │   └── utils/             # Helper functions
│   ├── tests/                 # Backend tests
│   ├── Dockerfile
│   └── pyproject.toml
│
├── frontend/                   # Dash frontend application
│   ├── components/            # Reusable UI components
│   ├── layouts/               # Page layouts and navigation
│   ├── callbacks/             # Interactive functionality
│   ├── utils/                 # Frontend utilities and API client
│   ├── assets/                # CSS, JS, and static files
│   ├── Dockerfile
│   └── requirements.txt
│
├── nginx/                      # NGINX reverse proxy
│   ├── sites-available/       # Virtual host configurations
│   ├── nginx.conf
│   └── Dockerfile
│
├── database/                   # Database setup and migrations
│   ├── init.sql
│   └── migrations/
│
├── scripts/                    # Utility scripts
│   ├── setup.sh              # Initial setup
│   ├── start.sh              # Start services
│   ├── stop.sh               # Stop services
│   ├── dev.sh                # Development mode
│   ├── deploy.sh             # Production deployment
│   ├── logs.sh               # View logs
│   ├── reset.sh              # Reset database
│   └── seed_data.py          # Load sample data
│
├── docker-compose.yml          # Production compose
├── docker-compose.dev.yml     # Development overrides
├── .env.example               # Environment template
└── README.md
```

## 🛠️ Development

### Development Mode

Start the application in development mode with hot-reloading:

```bash
./scripts/dev.sh
```

This provides:
- Hot-reloading for both frontend and backend
- Direct access to services for debugging
- Verbose logging and debug information

### Environment Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Key settings:
- `NODE_ENV=development` - Enables debug mode and verbose logging
- `NODE_ENV=production` - Production optimizations
- `POSTGRES_*` - Database connection settings
- `SECRET_KEY` - Change for production deployment

### Available Scripts

```bash
./scripts/setup.sh      # Initial project setup
./scripts/start.sh      # Start all services
./scripts/stop.sh       # Stop all services
./scripts/dev.sh        # Development mode with hot-reload
./scripts/logs.sh       # View logs (optionally specify service)
./scripts/reset.sh      # Reset database (removes all data)
./scripts/deploy.sh     # Production deployment
```

### API Development

The backend API is automatically documented:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

Key API endpoints:
- `GET /api/v1/leagues/{league_id}` - Get league information
- `GET /api/v1/managers/{manager_id}` - Get manager details
- `GET /api/v1/analytics/compare` - Compare managers
- `GET /health` - Health check

### Database Management

```bash
# View database logs
./scripts/logs.sh db

# Connect to database
docker-compose exec db psql -U fpl_user -d fpl_analytics

# Reset database (WARNING: deletes all data)
./scripts/reset.sh
```

## 🚀 Deployment

### Production Deployment

1. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env and set NODE_ENV=production
   # Update secrets and database passwords
   ```

2. **Deploy**:
   ```bash
   ./scripts/deploy.sh
   ```

### Environment Variables

Key production settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment mode | `development` |
| `SECRET_KEY` | JWT signing key | `change-me` |
| `POSTGRES_PASSWORD` | Database password | `fpl_password` |
| `DOMAIN` | Your domain name | `localhost` |

### SSL/HTTPS Setup

For production with SSL:

1. Place SSL certificates in `./certs/` directory
2. Update `SSL_CERT_PATH` and `SSL_KEY_PATH` in `.env`
3. Uncomment HTTPS server block in `nginx/sites-available/fpl-platform.conf`

## 📊 Usage

### Basic Workflow

1. **Enter League ID**: Input your FPL mini-league ID in the dashboard
2. **View Analytics**: Explore league standings, manager performance, and trends
3. **Compare Managers**: Use head-to-head comparison tools
4. **Track Progress**: Monitor performance over multiple gameweeks

### API Usage

```python
import requests

# Get league standings
response = requests.get("http://localhost:8080/api/v1/leagues/12345/standings")
league_data = response.json()

# Compare two managers
response = requests.get(
    "http://localhost:8080/api/v1/analytics/compare",
    params={"manager1_id": 123, "manager2_id": 456}
)
comparison = response.json()
```

## 🧪 Testing

```bash
# Run backend tests
docker-compose exec backend python -m pytest

# Run with coverage
docker-compose exec backend python -m pytest --cov=app
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the existing code style
4. Add tests for new functionality
5. Submit a pull request

## 🔧 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis
- **Frontend**: Dash, Plotly, Bootstrap
- **Infrastructure**: Docker, NGINX
- **External APIs**: Official Fantasy Premier League API

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- Check the [Issues](../../issues) page for known problems
- View logs: `./scripts/logs.sh`
- Health check: `curl http://localhost:8080/health`

---

**Made with ⚽ for FPL enthusiasts**
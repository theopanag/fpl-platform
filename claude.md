# Project: FPL Analytics Platform

## Overview
We are building an FPL (Fantasy Premier League) analytics platform to make the mini league competitions more enjoyable for data-driven managers.

Generic flow:
- Users log into a web dashboard
- Input their team or league ID
- Platform fetches relevant FPL data
- It then provides analytics, insights, and tools to improve their FPL performance

## Functional Requirements

### Data Integration
- The platform must connect to the official FPL API
- Should be able to fetch individual team data for each gameweek, including points, transfers, captain choices, chip usage, etc
- Should be able to fetch data for a specific mini-league using its unique ID
- Should be able to ingest overall FPL player data (price, points, ownership stats, etc)

### Dashboard
A central homepage providing a high-level overview
- A mini-league table with current league standings, including rank and overall points
- A gameweek summary and a manager of the week sections

### Manager/Team Analysis
A detailed view for each manager in the league
- Performance over time
- Transfer history
- Captaincy analysis
- Bench analysis

### Head-to-Head Comparison
A feature to directly compare two managers
- Metric comparison (total points, captaincy success, transfer costs, bench points, etc)
- Team overlap

### League-wide Analytics
Fun stats about the mini-league as a whole
- King of the gameweek, a leaderboard showing historical performance of the managers from previous seasons
- Most transfered players, showing the most frequently transfered-in and transfered-out players within the mini-league
- Chip usage

## Non-Functional Requirements
- The platform should be responsive, with web pages loading under 5 seconds
- The interface should be intuitive and easy to navigate, with clear visualizations
- The platform should be consistently available, even when FPL API is down or returns an error, displaying a user-friendly message instead of crashing
- The system should be able to handle growth without a significant drop in performance


## MVP Features
- Predefined analysis pages for performance and league standings
- Backend fetches FPL API data and caches results
- Frontend displays tables and charts

## Future Features
- News aggregation
- Team optimization tools
- Chatbot integration for interactive experience
- Migration of frontend from Dash (Python) to React (JS) while keeping backend/NGINX unchanged

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: Dash (Python, with path to React in the future)
- Database: Postgres (containerized) or DuckDB
- Reverse Proxy: NGINX
- Containerization: Docker, docker-compose

## Goals
- Maintain separation of concerns (backend, frontend, db, proxy)
- Ensure backend API is stable, so frontend migration is seamless
- Start Python-first, transition-ready for React
- Deployable via docker-compose
- Codebase should be **modular, testable and well-documented**

## Coding Conventions
- Use **type hints** and **docstrings** whenever possible
- Build iteratively, one module at a time
- Provide **usage examples** in the README
- Optimize for performance when relevant, and justify trade-offs
- At the end of each iteration, update:
    - `README.md` with features & usage
    - `claude.md` if scope or conventions change
    - relevant poetry files if dependencies were added

## Notes for Claude
- Respect the conventions and requirements in this file
- Do not introduce unnecessary dependencies
- Prefer **readability + performance balance**
- Summarize what was done after each iteration and suggest next steps

Always use context7 when I need code generation, setup or configuration steps, or
library/API documentation. This means you should automatically use the Context7 MCP
tools to resolve library id and get library docs without me having to explicitly ask.
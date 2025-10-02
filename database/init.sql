-- Initial database setup for FPL Analytics Platform
-- This script will be executed when the PostgreSQL container starts

-- Create database if it doesn't exist (handled by docker-compose environment variables)
-- CREATE DATABASE IF NOT EXISTS fpl_analytics;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'UTC';

-- Create initial schema (tables will be created by SQLAlchemy)
-- This file is mainly for any initial data or setup that needs to happen
-- before the application starts

-- Insert initial configuration or reference data if needed
-- (This would be executed before SQLAlchemy creates its tables)

-- Create indexes for better performance (these can be added via migrations later)
-- Note: SQLAlchemy will handle the main table creation

-- Log that initialization is complete
INSERT INTO pg_catalog.pg_stat_statements_info (userid, queryid, query)
VALUES (0, 0, 'Database initialized successfully')
ON CONFLICT DO NOTHING;
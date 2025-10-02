-- Migration 001: Initial schema for FPL Analytics Platform
-- This migration sets up the basic tables and relationships

-- Create leagues table
CREATE TABLE IF NOT EXISTS leagues (
    id SERIAL PRIMARY KEY,
    fpl_id INTEGER UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    league_type VARCHAR(50) NOT NULL,
    scoring VARCHAR(50) NOT NULL,
    admin_entry INTEGER,
    start_event INTEGER NOT NULL,
    code_privacy VARCHAR(50) NOT NULL,
    rank INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create managers table
CREATE TABLE IF NOT EXISTS managers (
    id SERIAL PRIMARY KEY,
    fpl_id INTEGER UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    player_first_name VARCHAR(255) NOT NULL,
    player_last_name VARCHAR(255) NOT NULL,
    player_region_name VARCHAR(255) NOT NULL,
    player_region_id INTEGER NOT NULL,
    player_region_short_iso VARCHAR(10) NOT NULL,
    summary_overall_points INTEGER DEFAULT 0,
    summary_overall_rank INTEGER,
    summary_event_points INTEGER DEFAULT 0,
    summary_event_rank INTEGER,
    current_event INTEGER DEFAULT 1,
    total_transfers INTEGER DEFAULT 0,
    league_id INTEGER REFERENCES leagues(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create gameweeks table
CREATE TABLE IF NOT EXISTS gameweeks (
    id SERIAL PRIMARY KEY,
    manager_id INTEGER NOT NULL REFERENCES managers(id),
    event INTEGER NOT NULL,
    points INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    rank INTEGER,
    rank_sort INTEGER,
    overall_rank INTEGER,
    bank INTEGER DEFAULT 0,
    value INTEGER DEFAULT 0,
    event_transfers INTEGER DEFAULT 0,
    event_transfers_cost INTEGER DEFAULT 0,
    points_on_bench INTEGER DEFAULT 0,
    picks JSONB,
    automatic_subs JSONB,
    entry_history JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(manager_id, event)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_leagues_fpl_id ON leagues(fpl_id);
CREATE INDEX IF NOT EXISTS idx_managers_fpl_id ON managers(fpl_id);
CREATE INDEX IF NOT EXISTS idx_managers_league_id ON managers(league_id);
CREATE INDEX IF NOT EXISTS idx_gameweeks_manager_id ON gameweeks(manager_id);
CREATE INDEX IF NOT EXISTS idx_gameweeks_event ON gameweeks(event);
CREATE INDEX IF NOT EXISTS idx_gameweeks_manager_event ON gameweeks(manager_id, event);

-- Create updated_at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_leagues_updated_at
    BEFORE UPDATE ON leagues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_managers_updated_at
    BEFORE UPDATE ON managers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gameweeks_updated_at
    BEFORE UPDATE ON gameweeks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for development (optional)
-- INSERT INTO leagues (fpl_id, name, league_type, scoring, start_event, code_privacy)
-- VALUES (12345, 'Sample League', 'classic', 'total', 1, 'public')
-- ON CONFLICT (fpl_id) DO NOTHING;
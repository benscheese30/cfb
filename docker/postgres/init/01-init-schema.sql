-- Initialize CFB Database Schema
-- This file will be executed when the container starts for the first time

-- Create database schema for college football data
CREATE SCHEMA IF NOT EXISTS cfb;

-- Teams table
CREATE TABLE IF NOT EXISTS cfb.teams (
    id SERIAL PRIMARY KEY,
    team_id INTEGER UNIQUE NOT NULL,
    school VARCHAR(255) NOT NULL,
    mascot VARCHAR(255),
    abbreviation VARCHAR(10),
    conference VARCHAR(255),
    division VARCHAR(255),
    color VARCHAR(7), -- hex color
    alt_color VARCHAR(7), -- hex color
    logos JSONB,
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Games table
CREATE TABLE IF NOT EXISTS cfb.games (
    id SERIAL PRIMARY KEY,
    game_id INTEGER UNIQUE NOT NULL,
    season INTEGER NOT NULL,
    week INTEGER,
    season_type VARCHAR(50), -- 'regular', 'postseason', etc.
    start_date TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    neutral_site BOOLEAN DEFAULT FALSE,
    conference_game BOOLEAN DEFAULT FALSE,
    attendance INTEGER,
    venue_id INTEGER,
    venue VARCHAR(255),
    home_team_id INTEGER REFERENCES cfb.teams(team_id),
    away_team_id INTEGER REFERENCES cfb.teams(team_id),
    home_points INTEGER,
    away_points INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FPI Rankings table
CREATE TABLE IF NOT EXISTS cfb.fpi_rankings (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES cfb.teams(team_id),
    season INTEGER NOT NULL,
    week INTEGER NOT NULL,
    fpi_rating DECIMAL(10,6),
    fpi_rank INTEGER,
    trend VARCHAR(10), -- 'up', 'down', 'same'
    projected_wins DECIMAL(4,2),
    projected_losses DECIMAL(4,2),
    strength_of_record DECIMAL(10,6),
    remaining_strength_of_schedule DECIMAL(10,6),
    efficiency DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, season, week)
);

-- SP+ Rankings table
CREATE TABLE IF NOT EXISTS cfb.sp_rankings (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES cfb.teams(team_id),
    season INTEGER NOT NULL,
    week INTEGER,
    rating DECIMAL(10,6),
    ranking INTEGER,
    second_order_wins DECIMAL(4,2),
    sos DECIMAL(10,6), -- strength of schedule
    offense DECIMAL(10,6),
    defense DECIMAL(10,6),
    special_teams DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, season, week)
);

-- Game Predictions table
CREATE TABLE IF NOT EXISTS cfb.game_predictions (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES cfb.games(game_id),
    prediction_source VARCHAR(50) NOT NULL, -- 'fpi', 'sp_plus', etc.
    home_win_probability DECIMAL(5,4), -- 0.0000 to 1.0000
    away_win_probability DECIMAL(5,4),
    spread DECIMAL(4,1),
    total DECIMAL(4,1),
    home_team_rating DECIMAL(10,6),
    away_team_rating DECIMAL(10,6),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game_id, prediction_source, prediction_date::date)
);

-- Luck Rankings table (from TeamRankings)
CREATE TABLE IF NOT EXISTS cfb.luck_rankings (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES cfb.teams(team_id),
    season INTEGER NOT NULL,
    ranking_date DATE NOT NULL,
    rank INTEGER,
    luck_rating DECIMAL(10,6),
    source VARCHAR(50) DEFAULT 'teamrankings',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, season, ranking_date, source)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_games_season_week ON cfb.games(season, week);
CREATE INDEX IF NOT EXISTS idx_games_teams ON cfb.games(home_team_id, away_team_id);
CREATE INDEX IF NOT EXISTS idx_fpi_rankings_season_week ON cfb.fpi_rankings(season, week);
CREATE INDEX IF NOT EXISTS idx_sp_rankings_season_week ON cfb.sp_rankings(season, week);
CREATE INDEX IF NOT EXISTS idx_game_predictions_game_id ON cfb.game_predictions(game_id);
CREATE INDEX IF NOT EXISTS idx_luck_rankings_date ON cfb.luck_rankings(ranking_date);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON cfb.teams FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_games_updated_at BEFORE UPDATE ON cfb.games FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA cfb TO cfb_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cfb TO cfb_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA cfb TO cfb_user;

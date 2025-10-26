-- AUREX.AI - Database Initialization Script
-- PostgreSQL with TimescaleDB Extension
-- Version: 1.0
-- Date: 2025-10-26

-- ==========================================
-- Enable Extensions
-- ==========================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "timescaledb";

-- ==========================================
-- Create Tables
-- ==========================================

-- News Table
CREATE TABLE IF NOT EXISTS news (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    source VARCHAR(100) NOT NULL,
    url TEXT,
    content TEXT,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    sentiment_label VARCHAR(20),  -- positive, negative, neutral
    sentiment_score FLOAT,  -- confidence score 0-1
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create hypertable for time-series optimization
SELECT create_hypertable('news', 'timestamp', if_not_exists => TRUE);

-- Price Table
CREATE TABLE IF NOT EXISTS price (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(20) NOT NULL,  -- e.g., XAUUSD
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    price FLOAT NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT,
    change_pct FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create hypertable for time-series optimization
SELECT create_hypertable('price', 'timestamp', if_not_exists => TRUE);

-- Sentiment Summary Table
CREATE TABLE IF NOT EXISTS sentiment_summary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    avg_sentiment FLOAT NOT NULL,  -- Average sentiment score
    positive_count INT DEFAULT 0,
    negative_count INT DEFAULT 0,
    neutral_count INT DEFAULT 0,
    sample_size INT NOT NULL,
    symbol VARCHAR(20) DEFAULT 'XAUUSD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create hypertable for time-series optimization
SELECT create_hypertable('sentiment_summary', 'timestamp', if_not_exists => TRUE);

-- Alert Table (for future use)
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type VARCHAR(50) NOT NULL,  -- divergence, threshold_breach, etc.
    severity VARCHAR(20) DEFAULT 'info',  -- info, warning, critical
    message TEXT NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- Create Indexes
-- ==========================================

-- News indexes
CREATE INDEX IF NOT EXISTS idx_news_timestamp ON news (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_news_source ON news (source);
CREATE INDEX IF NOT EXISTS idx_news_sentiment_label ON news (sentiment_label);

-- Price indexes
CREATE INDEX IF NOT EXISTS idx_price_timestamp ON price (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_price_symbol ON price (symbol);
CREATE INDEX IF NOT EXISTS idx_price_symbol_timestamp ON price (symbol, timestamp DESC);

-- Sentiment summary indexes
CREATE INDEX IF NOT EXISTS idx_sentiment_timestamp ON sentiment_summary (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sentiment_symbol ON sentiment_summary (symbol);

-- Alert indexes
CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_acknowledged ON alerts (acknowledged);

-- ==========================================
-- Create Functions
-- ==========================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for news table
DROP TRIGGER IF EXISTS update_news_updated_at ON news;
CREATE TRIGGER update_news_updated_at
    BEFORE UPDATE ON news
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ==========================================
-- Data Retention Policies
-- ==========================================

-- Keep raw news for 30 days
SELECT add_retention_policy('news', INTERVAL '30 days', if_not_exists => TRUE);

-- Keep raw price data for 90 days
SELECT add_retention_policy('price', INTERVAL '90 days', if_not_exists => TRUE);

-- Keep sentiment summaries for 180 days
SELECT add_retention_policy('sentiment_summary', INTERVAL '180 days', if_not_exists => TRUE);

-- ==========================================
-- Continuous Aggregates (Optional)
-- ==========================================

-- Hourly sentiment aggregation
CREATE MATERIALIZED VIEW IF NOT EXISTS sentiment_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', timestamp) AS bucket,
    symbol,
    AVG(avg_sentiment) AS avg_sentiment,
    SUM(positive_count) AS positive_count,
    SUM(negative_count) AS negative_count,
    SUM(neutral_count) AS neutral_count,
    SUM(sample_size) AS sample_size
FROM sentiment_summary
GROUP BY bucket, symbol;

-- Add refresh policy for continuous aggregate
SELECT add_continuous_aggregate_policy('sentiment_hourly',
    start_offset => INTERVAL '2 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE
);

-- ==========================================
-- Sample Data (Development Only)
-- ==========================================

-- Insert sample news
INSERT INTO news (title, source, sentiment_label, sentiment_score, timestamp) VALUES
('Gold prices surge on economic uncertainty', 'ForexFactory', 'positive', 0.85, NOW() - INTERVAL '1 hour'),
('Federal Reserve signals rate hike', 'Investing.com', 'negative', 0.78, NOW() - INTERVAL '2 hours'),
('Gold market remains stable', 'ForexFactory', 'neutral', 0.65, NOW() - INTERVAL '3 hours')
ON CONFLICT DO NOTHING;

-- Insert sample price data
INSERT INTO price (symbol, price, change_pct, timestamp) VALUES
('XAUUSD', 2050.50, 0.5, NOW() - INTERVAL '1 hour'),
('XAUUSD', 2048.30, -0.1, NOW() - INTERVAL '2 hours'),
('XAUUSD', 2049.00, 0.3, NOW() - INTERVAL '3 hours')
ON CONFLICT DO NOTHING;

-- Insert sample sentiment summary
INSERT INTO sentiment_summary (avg_sentiment, positive_count, negative_count, neutral_count, sample_size, timestamp) VALUES
(0.72, 15, 5, 10, 30, NOW() - INTERVAL '1 hour'),
(0.65, 12, 8, 10, 30, NOW() - INTERVAL '2 hours')
ON CONFLICT DO NOTHING;

-- ==========================================
-- Grant Permissions
-- ==========================================

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aurex;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO aurex;

-- ==========================================
-- Complete
-- ==========================================

\echo 'Database initialization completed successfully!'


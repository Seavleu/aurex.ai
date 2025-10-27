-- Clear existing data
TRUNCATE TABLE price CASCADE;
TRUNCATE TABLE news CASCADE;
TRUNCATE TABLE sentiment_summary CASCADE;

-- This will be populated by the Python script running inside Docker
-- For now, let's insert recent sample data that looks realistic

-- Insert realistic news articles
INSERT INTO news (source, title, url, content, timestamp, sentiment_label, sentiment_score) VALUES
('Reuters', 'Gold prices rise as dollar weakens amid Fed rate speculation', 'https://reuters.com/markets/gold-1', 'Gold prices climbed on Monday as the dollar weakened and investors assessed the Federal Reserve interest rate outlook. Spot gold rose 0.8% to $2,645 per ounce.', NOW() - INTERVAL '2 hours', 'positive', 0.75),
('Bloomberg', 'Central banks increase gold reserves amid economic uncertainty', 'https://bloomberg.com/news/gold-reserves', 'Central banks worldwide continued to boost their gold holdings in Q4, reflecting concerns about global economic stability. China and India led the purchases.', NOW() - INTERVAL '5 hours', 'positive', 0.82),
('CNBC', 'Gold faces pressure from rising Treasury yields', 'https://cnbc.com/gold-yields', 'Gold prices faced downward pressure as U.S. Treasury yields climbed to their highest levels in months, reducing the appeal of non-yielding assets.', NOW() - INTERVAL '8 hours', 'negative', 0.68),
('Financial Times', 'Investment demand for gold ETFs shows strong momentum', 'https://ft.com/content/gold-etf', 'Gold-backed exchange-traded funds saw significant inflows last week, indicating robust investor demand amid market volatility.', NOW() - INTERVAL '12 hours', 'positive', 0.79),
('MarketWatch', 'Gold market neutral as traders await key economic data', 'https://marketwatch.com/gold-trading', 'Gold prices held steady as traders adopted a wait-and-see approach before major economic releases including CPI and employment data.', NOW() - INTERVAL '18 hours', 'neutral', 0.50),
('Kitco News', 'Technical analysis suggests gold breakout above $2,650', 'https://kitco.com/gold-technical', 'Gold is showing strong technical momentum with potential to break above the $2,650 resistance level if current trends continue.', NOW() - INTERVAL '1 day', 'positive', 0.71),
('WSJ', 'Geopolitical tensions support safe-haven gold demand', 'https://wsj.com/gold-safe-haven', 'Escalating geopolitical concerns in multiple regions continue to provide support for gold as a safe-haven asset.', NOW() - INTERVAL '1 day 6 hours', 'positive', 0.77),
('Investing.com', 'Gold consolidates near record highs ahead of Fed meeting', 'https://investing.com/gold-fed', 'Gold prices consolidated near record highs as investors await clarity from the upcoming Federal Reserve policy meeting.', NOW() - INTERVAL '2 days', 'neutral', 0.55),
('BullionVault', 'Physical gold demand surges in Asian markets', 'https://bullionvault.com/asia-demand', 'Physical gold demand in Asian markets reached multi-year highs, driven by seasonal factors and currency hedging needs.', NOW() - INTERVAL '2 days 12 hours', 'positive', 0.84),
('Gold.org', 'Gold mining output remains constrained amid supply challenges', 'https://gold.org/mining-outlook', 'Global gold mining production faces ongoing supply chain challenges, potentially supporting prices through reduced supply.', NOW() - INTERVAL '3 days', 'neutral', 0.48);

-- Calculate and insert sentiment summary
INSERT INTO sentiment_summary (timestamp, avg_sentiment, positive_count, neutral_count, negative_count, sample_size, symbol)
SELECT 
    NOW(),
    AVG(sentiment_score * CASE 
        WHEN sentiment_label = 'positive' THEN 1
        WHEN sentiment_label = 'negative' THEN -1
        ELSE 0
    END) as avg_sentiment,
    COUNT(CASE WHEN sentiment_label = 'positive' THEN 1 END) as positive_count,
    COUNT(CASE WHEN sentiment_label = 'neutral' THEN 1 END) as neutral_count,
    COUNT(CASE WHEN sentiment_label = 'negative' THEN 1 END) as negative_count,
    COUNT(*) as sample_size,
    'XAUUSD' as symbol
FROM news
WHERE timestamp >= NOW() - INTERVAL '24 hours';

-- Note: Price data will be inserted by running the fetch script inside Docker
-- Or you can manually insert some recent prices here

SELECT 'Data inserted successfully!' as status;
SELECT COUNT(*) as news_count FROM news;
SELECT COUNT(*) as sentiment_count FROM sentiment_summary;


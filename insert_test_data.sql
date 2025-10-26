-- Insert realistic gold price data for the last 24 hours
INSERT INTO price (id, timestamp, symbol, price, open, high, low, close, volume) VALUES
  (gen_random_uuid(), NOW() - INTERVAL '1 hour', 'XAUUSD', 2806.80, 2805.20, 2808.50, 2803.10, 2806.80, 125000),
  (gen_random_uuid(), NOW() - INTERVAL '2 hours', 'XAUUSD', 2805.20, 2803.50, 2805.90, 2801.20, 2805.20, 132000),
  (gen_random_uuid(), NOW() - INTERVAL '3 hours', 'XAUUSD', 2803.50, 2801.10, 2804.20, 2799.50, 2803.50, 145000),
  (gen_random_uuid(), NOW() - INTERVAL '4 hours', 'XAUUSD', 2801.10, 2799.80, 2802.30, 2797.90, 2801.10, 138000),
  (gen_random_uuid(), NOW() - INTERVAL '5 hours', 'XAUUSD', 2799.80, 2797.50, 2800.80, 2795.20, 2799.80, 142000),
  (gen_random_uuid(), NOW() - INTERVAL '6 hours', 'XAUUSD', 2797.50, 2795.20, 2798.50, 2793.10, 2797.50, 155000),
  (gen_random_uuid(), NOW() - INTERVAL '12 hours', 'XAUUSD', 2793.40, 2790.50, 2795.80, 2788.20, 2793.40, 168000),
  (gen_random_uuid(), NOW() - INTERVAL '18 hours', 'XAUUSD', 2790.50, 2788.30, 2792.10, 2785.50, 2790.50, 172000),
  (gen_random_uuid(), NOW() - INTERVAL '24 hours', 'XAUUSD', 2788.30, 2785.60, 2789.20, 2783.80, 2788.30, 165000);

-- Insert sentiment data
INSERT INTO sentiment_summary (id, timestamp, avg_sentiment, positive_count, neutral_count, negative_count, sample_size, symbol) VALUES
  (gen_random_uuid(), NOW() - INTERVAL '1 hour', 0.72, 15, 10, 5, 30, 'XAUUSD'),
  (gen_random_uuid(), NOW() - INTERVAL '6 hours', 0.65, 12, 10, 8, 30, 'XAUUSD'),
  (gen_random_uuid(), NOW() - INTERVAL '12 hours', 0.58, 10, 12, 8, 30, 'XAUUSD'),
  (gen_random_uuid(), NOW() - INTERVAL '18 hours', 0.45, 8, 14, 8, 30, 'XAUUSD'),
  (gen_random_uuid(), NOW() - INTERVAL '24 hours', 0.52, 9, 13, 8, 30, 'XAUUSD');

SELECT 'Inserted ' || COUNT(*) || ' price records' as result FROM price;
SELECT 'Inserted ' || COUNT(*) || ' sentiment records' as result FROM sentiment_summary;


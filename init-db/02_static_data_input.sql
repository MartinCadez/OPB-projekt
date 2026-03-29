INSERT INTO app_user (username, email, password) VALUES 
('admin', 'admin@example.com', 'mysecretpassword');

-- INSERT INTO dim_price_type VALUES 
-- (1, 'open'),
-- (2, 'high'), 
-- (3, 'low'),
-- (4, 'close');

-- INSERT INTO dim_volume_type VALUES
-- (1, 'base_volume'),
-- (2, 'quote_volume'),
-- (3, 'taker_buy_base_volume'),
-- (4, 'taker_buy_quote_volume');

INSERT INTO dim_exchange VALUES
(1, 'Binance'),
(2, 'Coinbase'),
(3, 'Kucoin'),
(4, 'Bitstamp'),
(5, 'Kraken'),
(6, 'Bitfinex'),
(7, 'Huobi'),
(8, 'OKX'),
(9, 'Bybit'),
(10, 'Gemini');

INSERT INTO dim_symbol VALUES 
(1, 'BTCUSDT'),
(2, 'ETCUSDT'), 
(3, 'XRPUSDT'),
(4, 'BNBUSDT'),
(5, 'SOLUSDT');

INSERT INTO dim_timeframe VALUES
(1, '1m'),
(2, '3m'),
(3, '5m'),
(4, '15m'),
(5, '30m'),
(6, '1h'),
(7, '2h'),
(8, '4h'),
(9, '6h'),
(10, '8h'),
(11, '12h'),
(12, '1d'),
(13, '3d'),
(14, '1w'),
(15, '1mo');

COPY dim_country(iso_numeric_code, full_name, alpha2_code, alpha3_code)
FROM '/docker-entrypoint-initdb.d/data/country_codes.csv'
DELIMITER ','
CSV HEADER
QUOTE '"'
ESCAPE '"';

COPY dim_holiday(alpha3_code, date, name)
FROM '/docker-entrypoint-initdb.d/data/holidays.csv'
DELIMITER ','
CSV HEADER;

COPY fact_daily_kline(
    date,
    symbol_id,
    exchange_id,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    quote_asset_volume,
    number_of_trades,
    taker_buy_base_volume,
    taker_buy_quote_volume
)
FROM '/docker-entrypoint-initdb.d/data/binance_klines.csv'
DELIMITER ','
CSV HEADER;
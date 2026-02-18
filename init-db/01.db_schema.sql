CREATE TABLE IF NOT EXISTS app_user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(80) NOT NULL
);

-- CREATE TABLE IF NOT EXISTS amanda (
--     user_id SERIAL PRIMARY KEY,
--     username VARCHAR(20) UNIQUE NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     password VARCHAR(80) NOT NULL
-- );

CREATE TABLE IF NOT EXISTS dim_country (
    iso_numeric_code INT PRIMARY KEY,
    full_name TEXT NOT NULL UNIQUE,
    alpha2_code CHAR(2) NOT NULL UNIQUE,
    alpha3_code CHAR(3) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS dim_holiday (
    alpha3_code CHAR(3) NOT NULL REFERENCES dim_country(alpha3_code),
    date DATE NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (alpha3_code, date)
);


CREATE TABLE IF NOT EXISTS dim_symbol (
    symbol_id INT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS dim_timeframe (
    timeframe_id INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS dim_exchange (
    exchange_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS fact_daily_kline (
    date DATE NOT NULL, 
    symbol_id INT NOT NULL REFERENCES dim_symbol(symbol_id),
    exchange_id INT NOT NULL REFERENCES dim_exchange(exchange_id),
    open_price DECIMAL(20,8) NOT NULL,
    high_price DECIMAL(20,8) NOT NULL,
    low_price DECIMAL(20,8) NOT NULL,
    close_price DECIMAL(20,8) NOT NULL,
    volume DECIMAL(20,8) NOT NULL,
    quote_asset_volume DECIMAL(20,8),
    number_of_trades INT,
    taker_buy_base_volume DECIMAL(20,8),
    taker_buy_quote_volume DECIMAL(20,8),
    PRIMARY KEY (date, symbol_id, exchange_id)
);

-- TODO: update those tables lol :)
-- CREATE TABLE IF NOT EXISTS fact_yield (
--     date DATE NOT NULL,
--     yield DECIMAL(20, 8) NOT NULL
-- );



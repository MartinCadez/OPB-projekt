CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_country (
    country_id INT PRIMARY KEY,
    country_code VARCHAR(20) NOT NULL UNIQUE
    alpha2_code VARCHAR(20) NOT NULL UNIQUE
    alpha3_code VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_holiday (
    holiday_id INT PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    country_id INT REFERENCES dim_country(country_id),
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_symbol (
    symbol_id INT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_price_type (
    price_type_id INT PRIMARY KEY,
    price_type_name VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_volume_type (
    volume_type_id INT PRIMARY KEY,
    volume_type_name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_exchange (
    exchange_id INT PRIMARY KEY,
    exchange_name VARCHAR(50) NOT NULL UNIQUE,
);

CREATE TABLE IF NOT EXISTS bridge_trade_context (
    bridge_id INT PRIMARY KEY AUTO_INCREMENT,
    date_key INT NOT NULL REFERENCES dim_date(date_id),
    symbol_key INT NOT NULL REFERENCES dim_symbol(symbol_id),
    exchange_key INT NOT NULL REFERENCES dim_exchange(exchange_id),
    UNIQUE KEY (date_key, symbol_key, exchange_key)
);

CREATE TABLE IF NOT EXISTS fact_price (
    bridge_key INT NOT NULL REFERENCES bridge_trade_context(bridge_id),
    price_type_key INT NOT NULL REFERENCES dim_price_type(price_type_id),
    price FLOAT,
    PRIMARY KEY (bridge_key, price_type_key)
);

CREATE TABLE IF NOT EXISTS fact_volume (
    bridge_key INT NOT NULL REFERENCES bridge_trade_context(bridge_id),
    volume_type_key INT NOT NULL REFERENCES dim_volume_type(volume_type_id),
    volume FLOAT,
    PRIMARY KEY (bridge_key, volume_type_key)
);

CREATE TABLE IF NOT EXISTS fact_num_trades (
    bridge_key INT NOT NULL REFERENCES bridge_trade_context(bridge_id),
    number_of_trades INT,
    PRIMARY KEY (bridge_key)
);

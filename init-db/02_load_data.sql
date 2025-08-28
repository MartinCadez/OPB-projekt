INSERT INTO dim_price_type VALUES 
(1, 'open'),
(2, 'high'), 
(3, 'low'),
(4, 'close');

INSERT INTO dim_volume_type VALUES
(1, 'base_volume'),
(2, 'quote_volume'),
(3, 'taker_buy_base_volume'),
(4, 'taker_buy_quote_volume');

INSERT INTO dim_exchange (exchange_id, exchange_name) VALUES
(1, 'Binance'),
(2, 'Coinbase'),
(3, 'Kucoin'),
(4, 'Bitstamp'),
(5, 'Kraken'),
(6, 'Bitfinex'),
(7, 'Huobi'),
(8, 'OKX'),
(9, 'Bybit'),
(10, 'Gemini')

INSERT INTO dim_sym VALUES 
(1, 'BTCUSDT'),
(2, 'ETCUSDT'), 
(3, 'XRPUSDT'),
(4, 'BNBUSDT');
(5, 'SOLUSDT');

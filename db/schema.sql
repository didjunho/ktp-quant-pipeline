CREATE TABLE stocks (
    uid SERIAL PRIMARY KEY,
    ticker VARCHAR(250),
    timestamp TIMESTAMP,
    price DECIMAL
); 


-- initdb/init.sql

CREATE DATABASE ecommerce;

\c ecommerce

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id     TEXT PRIMARY KEY,
    process_id         TEXT,
    product_name       TEXT,
    product_category   TEXT,
    product_price      FLOAT,
    product_quantity   INT,
    total_amount       FLOAT,
    product_brand      TEXT,
    currency           TEXT,
    customer_id        TEXT,
    transaction_date   TEXT,
    payment_method     TEXT
);

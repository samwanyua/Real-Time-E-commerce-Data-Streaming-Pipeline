-- Create the 'ecommerce' database only if it doesn't exist
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'ecommerce'
   ) THEN
      CREATE DATABASE ecommerce;
   END IF;
END
$$;

-- Connect to the ecommerce database
\connect ecommerce

-- Create the 'transactions' table if it doesn't exist
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

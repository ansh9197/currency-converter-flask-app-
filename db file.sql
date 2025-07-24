CREATE DATABASE IF NOT EXISTS currencydb;
USE currencydb;
CREATE TABLE IF NOT EXISTS conversions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  base_currency VARCHAR(10),
  target_currency VARCHAR(10),
  amount DOUBLE,
  converted_amount DOUBLE,
  rate DOUBLE,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)

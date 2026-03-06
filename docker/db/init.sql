-- Connect to terrastack database
CREATE DATABASE IF NOT EXISTS terrastack;
\c terrastack;

-- Table for yard work quotes based on square footage
CREATE TABLE IF NOT EXISTS yard_quotes (
    id SERIAL PRIMARY KEY,
    min_sqft INT NOT NULL,
    max_sqft INT NOT NULL,
    task VARCHAR(255) NOT NULL,
    estimated_hours FLOAT,
    rate_per_hour FLOAT
);

-- Example data
INSERT INTO yard_quotes (min_sqft, max_sqft, task, estimated_hours, rate_per_hour)
VALUES
    (0, 500, 'Mow the lawn', 2, 25),
    (501, 1000, 'Mow and edge lawn', 3.5, 25),
    (1001, 2000, 'Mow, edge, and trim shrubs', 5, 30),
    (2001, 5000, 'Full yard service', 8, 35)
ON CONFLICT DO NOTHING;
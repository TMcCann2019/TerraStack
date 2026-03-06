CREATE TABLE IF NOT EXISTS quotes (
  id SERIAL PRIMARY KEY,
  quote TEXT NOT NULL,
  author VARCHAR(255)
);ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO quotes(quote, author)
VALUES("Be the change you want to see in the world.", "Ghandi"), ("Master patterns in life, and  you'll never suffer is the secret","someone");
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    author VARCHAR(255) DEFAULT NULL
);

INSERT INTO quotes (quote, author)
VALUES
('Be the change you want to see in your yard.', 'Gandhi'),
('Master yard patterns, and your grass will never suffer.', 'Someone'),
('A tidy yard is a happy yard.', 'Anonymous')
ON CONFLICT DO NOTHING;
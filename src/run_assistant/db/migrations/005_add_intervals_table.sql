CREATE TABLE IF NOT EXISTS intervals (
    id UUID PRIMARY KEY,
    run_id UUID REFERENCES runs (id) NOT NULL,
    interval_type STRING,
    distance_meters INT,
    duration_minutes FLOAT,
    rythm FLOAT,
    cardiac_frequency INT,
    cadence INT
)

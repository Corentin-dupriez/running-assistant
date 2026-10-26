ALTER TABLE laps
ADD COLUMN elevation_gain float;
ALTER TABLE laps
ADD COLUMN cadence float;

CREATE TABLE IF NOT EXISTS hr_zones (
    id uuid PRIMARY KEY,
    run_id uuid REFERENCES runs (id) NOT NULL,
    zone_name string,
    min_hr int,
    max_hr int,
    time float
);

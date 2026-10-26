SELECT
    id,
    run_id,
    time_minutes,
    cardiac_freq,
    elevation_gain,
    cadence
FROM {{ source("raw_laps", "laps") }}

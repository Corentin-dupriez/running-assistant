SELECT
    id,
    run_id,
    time_minutes,
    min_per_km,
    cardiac_freq
FROM {{ source("raw_laps", "laps") }}

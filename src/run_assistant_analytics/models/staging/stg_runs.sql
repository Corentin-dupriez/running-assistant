SELECT
    id,
    length_kilometers,
    time_minutes,
    elevation_gain,
    min_per_km,
    cardiac_freq,
    date
FROM {{ source('raw_runs', 'runs') }}

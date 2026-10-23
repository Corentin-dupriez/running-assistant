SELECT
    id,
    length_kilometers,
    time_minutes,
    elevation_gain,
    min_per_km,
    cardiac_freq,
    date,
    equipment_name,
    equipment_id,
    max_pace,
    avg_pace,
    perceived_effort,
    run_type
FROM {{ source('raw_runs', 'runs') }}

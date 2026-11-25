SELECT
    id,
    run_id,
    interval_type,
    distance_meters,
    duration_minutes,
    rythm,
    cardiac_frequency,
    cadence
FROM {{ ref('stg_intervals') }}

SELECT
    id,
    length_km,
    time_minutes,
    elevation_gain,
    min_per_km,
    cardiac_freq,
    date,
    equipment_name,
    equipment_id,
    max_pace AS max_cadence,
    avg_pace AS avg_cadence,
    intensity,
    training_load,
    run_type,
    source
FROM {{ ref('int_run_information') }}

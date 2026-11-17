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
    run_type,
    1 AS id_in_file
FROM {{ source('raw_runs', 'runs') }}

UNION DISTINCT

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
    run_type,
    id_in_file
FROM {{ source('raw_runs', 'csv_runs') }}
ORDER BY date, id_in_file

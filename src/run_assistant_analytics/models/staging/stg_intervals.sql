select
    id,
    run_id,
    interval_type,
    distance_meters,
    duration_minutes,
    rythm,
    cardiac_frequency,
    cadence
from
    {{ source('raw_intervals', 'intervals_csv') }}

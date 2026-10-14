SELECT
    activity_date,
    activity_type,
    elapsed_time_s,
    distance,
    max_heart_rate,
    average_heart_rate,
    elevation_gain,
    equipment_name,
    equipment_id,
    max_pace,
    avg_pace,
    equipment_name,
    equipment_id
FROM {{ source('raw_strava_runs', 'strava_activities_data') }}

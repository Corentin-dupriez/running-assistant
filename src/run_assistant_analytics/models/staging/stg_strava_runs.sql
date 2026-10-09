SELECT
    activity_date,
    activity_type,
    elapsed_time_s,
    distance,
    max_heart_rate,
    average_heart_rate,
    elevation_gain
FROM {{ source('raw_strava_runs', 'strava_activities_data') }}

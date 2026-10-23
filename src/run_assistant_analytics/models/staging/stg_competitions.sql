SELECT
    id,
    location,
    length_km,
    elevation_gain,
    date,
    CASE
        WHEN lower(race_type) = 'trail' THEN 'trail'
        WHEN lower(race_type) = 'road' THEN 'road'
        ELSE 'unknown'
    END AS race_type
FROM {{ source('raw_competitions', 'competitions') }}

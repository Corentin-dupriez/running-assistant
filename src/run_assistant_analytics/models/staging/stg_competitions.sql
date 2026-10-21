SELECT *
FROM {{ source('raw_competitions', 'competitions') }}

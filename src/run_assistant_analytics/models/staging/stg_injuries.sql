SELECT *
FROM {{ source('raw_injuries', 'injuries') }}

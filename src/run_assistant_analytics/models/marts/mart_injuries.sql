SELECT
    id,
    date,
    comment
FROM {{ ref('stg_injuries') }}

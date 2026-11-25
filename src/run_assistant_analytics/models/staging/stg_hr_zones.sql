SELECT *
FROM {{ source('raw_hr_zones', 'hr_zones') }}

UNION DISTINCT

SELECT *
FROM {{ source('raw_hr_zones', 'hr_zones_csv') }}

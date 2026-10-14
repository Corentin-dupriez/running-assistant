SELECT
    equipment_name,
    equipment_id,
    sum(length_km)
FROM {{ ref('int_run_information') }}
GROUP BY equipment_name, equipment_id

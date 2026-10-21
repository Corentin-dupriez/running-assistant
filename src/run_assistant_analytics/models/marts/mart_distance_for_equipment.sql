SELECT
    equipment_name,
    equipment_id,
    sum(length_km) AS distance_with_equipment
FROM {{ ref('int_run_information') }}
GROUP BY equipment_name, equipment_id

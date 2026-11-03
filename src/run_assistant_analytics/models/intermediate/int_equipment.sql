with equipments_cte as (
    select distinct equipment_name
    from {{ ref('stg_runs') }}
),

strava_equipment_cte as (
    select distinct equipment_name
    from {{ ref('stg_strava_runs') }}
),

joined_equipments_cte as (
    select equipment_name
    from equipments_cte
    union distinct
    select equipment_name
    from strava_equipment_cte
)

select
    uuid() as id,
    equipment_name
from joined_equipments_cte

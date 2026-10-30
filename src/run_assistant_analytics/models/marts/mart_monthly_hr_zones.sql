with date_spine_cte as (
    select
        date_day,
        month_number,
        month_name,
        year_number
    from {{ ref('date_spine') }}
),

hr_data AS (
    SELECT *
    FROM {{ ref('stg_hr_zones') }}
    PIVOT (
        SUM(time) as sum_time
        FOR zone_name IN ('Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5')
    )
),

run_data as (
    select
        id,
        date
    from {{ ref('int_run_information' ) }}
)

select
    month_number || '-' || year_number as month_year,
    month_name,
    sum(h."Zone 1_sum_time") as total_time_zone_1,
    sum(h."Zone 2_sum_time")as total_time_zone_2,
    sum(h."Zone 3_sum_time")as total_time_zone_3,
    sum(h."Zone 4_sum_time")as total_time_zone_4,
    sum(h."Zone 5_sum_time")as total_time_zone_5
from hr_data h
join run_data r on r.id = h.run_id
join date_spine_cte d on d.date_day::date = r.date::date
group by month_year, month_name, year_number

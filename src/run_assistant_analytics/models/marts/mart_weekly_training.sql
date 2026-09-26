with date_spine_cte as (
    select
        date_day,
        week_number,
        month_name,
        year_number
    from {{ ref('date_spine' ) }}
),

trainings_cte as (
    select
        length_kilometers,
        time_minutes,
        elevation_gain,
        min_per_km,
        cardiac_freq,
        date
    from {{ ref('stg_runs' ) }}
)

select
    week_number,
    month_name,
    year_number,
    sum(length_kilometers) as total_kilometers,
    avg(length_kilometers) as average_kilometers_per_run,
    sum(time_minutes) as total_time_minutes,
    avg(time_minutes) as average_run_duration_minutes,
    sum(elevation_gain) as total_elevation_gain,
    avg(elevation_gain) as average_elevation_gain_per_run,
    avg(min_per_km) as average_rythm,
    avg(cardiac_freq) as average_cardiac_frequency
from trainings_cte t
join
    date_spine_cte d
    on cast(d.date_day as timestamp) = cast(t.date as timestamp)
group by d.week_number, d.year_number, d.month_name

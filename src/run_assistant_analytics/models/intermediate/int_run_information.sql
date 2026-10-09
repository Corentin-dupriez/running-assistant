with strava_data as (
    select
        cast(
            regexp_replace(
                distance,
                ',',
                '.'
            )
            as float
        )
            as length_km,
        cast(elapsed_time_s as int) as time_minutes,
        cast(
            regexp_replace(
                elevation_gain,
                ',',
                '.'
            )
            as float
        )
            as elevation_gain,
        round(
            (cast(elapsed_time_s as int) / 60)
            / cast(
                regexp_replace(
                    distance,
                    ',',
                    '.'
                )
                as float
            ),
            2
        )
            as min_per_km,
        cast(average_heart_rate as int) as cardiac_freq,
        cast (
          concat(
            {{ extract_from_date('activity_date', 3) }}, '-',
            CASE 
              WHEN {{ extract_from_date('activity_date', 2) }} = 'sept.' then '09'
              WHEN {{ extract_from_date('activity_date', 2)}} = 'juin' then '06'
              WHEN {{ extract_from_date('activity_date', 2) }} = 'juil.' then '07'
              WHEN {{extract_from_date('activity_date', 2) }} = 'août' THEN '08'
            ELSE {{ extract_from_date('activity_date', 2)}}
            END,
            '-',
            lpad({{ extract_from_date('activity_date', 1)}}, 2, '0')
        ) as date)
        as date,
        'strava' as source
    from {{ ref('stg_strava_runs') }}
    where activity_type like '%Course%'
),

manual_data as (
    select
        length_kilometers as length_km,
        time_minutes,
        elevation_gain,
        round(min_per_km, 2) as min_per_km,
        cardiac_freq,
        date as date,
        'manual' as source
    from {{ ref('stg_runs') }}
)

select *
from manual_data
union distinct
select *
from strava_data

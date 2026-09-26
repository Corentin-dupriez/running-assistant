with date_spine as (
  {{dbt_utils.date_spine(
      datepart="day",
      start_date="cast('2026-01-01' as timestamp)",
      end_date="cast('2030-12-31' as timestamp)"
    )
  }}
)
SELECT 
  date_day,
  extract(year from date_day) as year_number,
  extract(month from date_day) as month_number,
  extract(day from date_day) as day_number,
  extract(quarter from date_day) as quarter_number,
  concat(extract(year from date_day), '-Q', extract(quarter from date_day)) as year_quarter
from date_spine


select
    date_day,
    year_number,
    month_number,
    month_name,
    day_number,
    quarter_number,
    year_quarter,
    week_number
from {{ ref('date_spine') }}

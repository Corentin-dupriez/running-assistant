SELECT date
FROM {{ ref('int_run_information') }}
ORDER BY date DESC
LIMIT 1

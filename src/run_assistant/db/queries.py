import duckdb
from run_assistant.db.initialize_db import db_path
from typing import List


def _query_to_recors(con, query: str, params: list | None) -> List[dict]:
    results = con.execute(query, params or [])
    columns = [c[0] for c in results.description]
    rows = results.fetchall()
    return [dict(zip(columns, row)) for row in rows]


def retrieve_run(run_id: str):
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(
            con,
            """
           SELECT * 
           FROM runs 
           WHERE id = ?
        """,
            [run_id],
        )
        if res:
            return res


def retrieve_runs():
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(
            con,
            """
            SELECT *
            FROM run_assistant.main.mart_all_runs
            """,
            [],
        )
        return res


def retrieve_injuries():
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(
            con,
            """
            SELECT *
            FROM run_assistant.main.mart_injuries
            """,
            [],
        )
        return res


def retrieve_breakdown_per_km(run_id: str):
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(
            con,
            """
            SELECT *
            FROM run_assistant.main.mart_breakdown_per_km
            WHERE run_id = ?
            """,
            [run_id],
        )
        return res


def retrieve_hr_zones(run_id: str):
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(
            con,
            """
            SELECT *
            FROM run_assistant.main.mart_hr_zones
            WHERE run_id = ?
            """,
            [run_id],
        )
        return res


def retrieve_weekly_hr_data():
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(
            con,
            """
            with total_run_time as (
            select 
                sum(time) as total,
                week_number
            from mart_hr_zones h 
            join mart_all_runs r on r.id = run_id 
            join dim_date d on d.date_day = r.date 
            group by d.week_number)

            select  
                zone_name, 
                d.week_number, 
                min_hr,
                max_hr,
                round(sum(time), 2) as time_in_zone,
                round(sum(time) / t.total * 100, 2) as percentage_in_zone
            from mart_hr_zones h 
            join mart_all_runs r on r.id = run_id 
            join dim_date d on d.date_day = r.date 
            join total_run_time t on t.week_number = d.week_number
            group by d.week_number, zone_name, min_hr, max_hr, t.total
            order by d.week_number desc, zone_name asc
            """,
            [],
        )
        return res


def retrieve_planned_competitions():
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(
            con,
            """
            SELECT *
            FROM run_assistant.main.mart_competitions_plan
            """,
            [],
        )
        return res


def retrieve_weekly_run_info(start_year: int | None = None):
    query = """
            SELECT * 
            FROM run_assistant.main.mart_weekly_training
            """
    params = []

    if start_year is not None:
        query += "where year_number >= ?"
        params.append(start_year)
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(con, query, params)
        return res


def retrieve_monthly_run_info(start_year: int | None = None):
    query = """
            SELECT * 
            FROM run_assistant.main.mart_monthly_training
            """
    params = []

    if start_year is not None:
        query += "where year_number >= ?"
        params.append(start_year)
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(con, query, params)
        return res


def retrieve_intervals_breakdown(run_id: str):
    query = """
        SELECT * FROM 
        run_assistant.main.fact_all_intervals
        """
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(con, query, [])
        return res

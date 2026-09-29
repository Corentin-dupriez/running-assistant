import duckdb
from run_assistant.db.initialize_db import db_path
from typing import List


def _query_to_recors(con, query: str, params: list | None) -> List[dict]:
    results = con.execute(query, params or [])
    columns = [c[0] for c in results.description]
    rows = results.fetchall()
    return [dict(zip(columns, rows)) for row in rows]


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
            FROM runs
            """,
            [],
        )
        return res


def retrieve_weekly_run_info(start_year: int | None = None):
    query = """
            SELECT * 
            FROM run_assistant.main.mart_weekly_training
            """

    if start_year is not None:
        query += f"where year_number >= {start_year}"
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(con, query, [])
        return res


def retrieve_monthly_run_info(start_year: int | None = None):
    query = """
            SELECT * 
            FROM run_assistant.main.mart_monthly_training
            """

    if start_year is not None:
        query += f"where year_number >= {start_year}"
    with duckdb.connect(db_path) as con:
        res = _query_to_recors(con, query, [])
        return res

import duckdb
from run_assistant.db.initialize_db import db_path
from run_assistant.ingest.ingestion_helpers import run_dbt


def read_activities_file(file_path: str):
    with duckdb.connect(db_path) as con:
        con.execute("DELETE * from strava_activities_data")
        con.execute(
            f"INSERT INTO strava_activities_data SELECT * FROM read_csv('{file_path}')"
        )
    run_dbt()

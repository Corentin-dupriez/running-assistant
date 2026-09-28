import duckdb
from run_assistant.db.initialize_db import db_path


def read_activities_file(file_path: str):
    with duckdb.connect(db_path) as con:
        con.execute(
            f"INSERT INTO strava_activities_data SELECT * FROM read_csv('{file_path}')"
        )

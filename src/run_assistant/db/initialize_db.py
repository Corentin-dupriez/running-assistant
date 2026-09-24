import os
import duckdb
from pathlib import Path

db_path = Path(os.getcwd()).parent.parent / "run_assistant.duckdb"


def create_db() -> None:
    with duckdb.connect(db_path) as con:
        con.sql("""
            CREATE TABLE IF NOT EXISTS runs (
                id UUID PRIMARY KEY,
                length_kilometers FLOAT NOT NULL,
                time_minutes FLOAT NOT NULL,
                elevation_gain FLOAT,
                min_per_km FLOAT,
                cardiac_freq INTEGER,
                date DATE
            )
        """)

        con.sql(
            """
            CREATE TABLE IF NOT EXISTS laps (
                id UUID PRIMARY KEY,
                run_id UUID REFERENCES runs(id) NOT NULL,
                time_minutes FLOAT NOT NULL,
                min_per_km FLOAT,
                cardiac_freq INTEGER
            )
            """
        )

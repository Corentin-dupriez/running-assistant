import duckdb
from run_assistant import config

db_path = config.db_path


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
                date DATE,
                equipment_name STRING,
                equipment_id STRING,
                max_pace FLOAT,
                avg_pace FLOAT
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


def drop_tables() -> None:
    with duckdb.connect(db_path) as con:
        con.sql("DROP TABLE IF EXISTS laps")
        con.sql("DROP TABLE IF EXISTS runs")


if __name__ == "__main__":
    create_db()

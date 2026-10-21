import duckdb
from run_assistant import config

db_path = config.db_path


def create_db(tables: list = []) -> None:
    with duckdb.connect(db_path) as con:
        if "runs" in tables:
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
                    avg_pace FLOAT,
                    perceived_effort INT
                )
            """)

        if "laps" in tables:
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

        if "injuries" in tables:
            con.sql(
                """
                CREATE TABLE IF NOT EXISTS injuries (
                    id UUID PRIMARY KEY,
                    date DATE,
                    comment STRING
                )
                """
            )
        if "competitions" in tables:
            con.sql(
                """
                CREATE TABLE IF NOT EXISTS competitions (
                    id UUID PRIMARY KEY,
                    location STRING,
                    length_km FLOAT,
                    date DATE,
                    race_type STRING
                )
                """
            )


def drop_tables(tables: list = []) -> None:
    with duckdb.connect(db_path) as con:
        if "laps" in tables:
            con.sql("DROP TABLE IF EXISTS laps")
        if "runs" in tables:
            con.sql("DROP TABLE IF EXISTS runs")
        con.sql("DROP TABLE IF EXISTS injuries")
        con.sql("DROP TABLE IF EXISTS competitions")


if __name__ == "__main__":
    create_db()

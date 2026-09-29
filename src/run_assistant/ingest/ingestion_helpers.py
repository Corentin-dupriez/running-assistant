import argparse
from datetime import date
import duckdb
from run_assistant.db.initialize_db import db_path
from dbt.cli.main import dbtRunner


def run_dbt() -> None:
    dbt_runner = dbtRunner()
    cli_args = ["run", "--project-dir", "../run_assistant_analytics/"]
    _ = dbt_runner.invoke(args=cli_args)


def insert_run(args: argparse.Namespace) -> str | None:
    return _insert_run(
        args.kilometers,
        args.time,
        args.date,
        args.elevation,
        args.rythm,
        args.cardiac_freq,
    )


def _insert_run(
    km: float,
    time: float,
    date: date,
    elevation_gain: float,
    rythm: float,
    cardiac_frequency: int,
) -> str | None:
    with duckdb.connect(db_path) as con:
        con.execute(
            """
            INSERT INTO runs
                (
                    id,
                    length_kilometers, 
                    time_minutes, 
                    date, 
                    elevation_gain, 
                    min_per_km, 
                    cardiac_freq
                ) 
            values 
                (
                    uuid(), 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?
                )
            RETURNING id
        """,
            [km, time, date, elevation_gain, rythm, cardiac_frequency],
        )
        res = con.fetchone()
        if res:
            run_dbt()
            return str(res[0])
        return None


def insert_lap(args: argparse.Namespace) -> str | None:
    return _insert_lap(args.run, args.time, args.min_per_km, args.cardiac_freq)


def _insert_lap(
    run_id: str, time_minutes: float, min_per_km: float, cardiac_frequency: int
) -> str | None:
    with duckdb.connect(db_path) as con:
        res = con.execute(
            """
            INSERT INTO laps (id, run_id, time_minutes, min_per_km, cardiac_freq) values (uuid(), ?, ?, ?, ?)
            RETURNING ID
            """,
            [run_id, time_minutes, min_per_km, cardiac_frequency],
        )
        res = res.fetchone()
        if res:
            run_dbt()
            return str(res[0])

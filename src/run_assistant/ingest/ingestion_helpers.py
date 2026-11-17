import argparse
from datetime import date
import duckdb
import pandas as pd
from run_assistant.db.initialize_db import db_path
from run_assistant.db.dbt_helpers import run_dbt


def insert_run(args: argparse.Namespace) -> str | None:
    return _insert_run(
        args.kilometers,
        args.time,
        args.date,
        args.elevation,
        args.rythm,
        args.cardiac_freq,
        args.equipment_name or None,
        args.equipment_id or None,
        args.max_pace or None,
        args.average_pace or None,
        args.perceived_effort or None,
        args.run_type or None,
    )


def _insert_run(
    km: float,
    time: float,
    date: date,
    elevation_gain: float,
    rythm: float,
    cardiac_frequency: int,
    equipment_name: str | None = None,
    equipment_id: str | None = None,
    max_pace: float | None = None,
    avg_pace: float | None = None,
    perceived_effort: int | None = None,
    run_type: str | None = None,
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
                    cardiac_freq,
                    equipment_name,
                    equipment_id,
                    max_pace,
                    avg_pace,
                    perceived_effort,
                    run_type
                ) 
            values 
                (
                    uuid(), 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?, 
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
            RETURNING id
        """,
            [
                km,
                time,
                date,
                elevation_gain,
                rythm,
                cardiac_frequency,
                equipment_name,
                equipment_id,
                max_pace,
                avg_pace,
                perceived_effort,
                run_type,
            ],
        )
        res = con.fetchone()
        if res:
            run_dbt()
            return str(res[0])
        return None


def insert_run_csv(file_path: str, test: bool = False) -> list | None:
    with duckdb.connect(db_path) as con:
        con.execute(f"""
        CREATE TABLE IF NOT EXISTS {"csv_runs_test" if test else "csv_runs"}(
            ID uuid primary key,
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
            perceived_effort INT,
            run_type STRING,
            file_name STRING,
            id_in_file INT
            )
        """)
        res = con.execute(
            f"""INSERT INTO {"csv_runs_test" if test else "csv_runs"} 
            SELECT uuid() as id,
                    length_kilometers, 
                    time_minutes, 
                    elevation_gain, 
                    min_per_km, 
                    cardiac_freq,
                    date,
                    equipment_name,
                    equipment_id,
                    max_pace,
                    avg_pace,
                    perceived_effort,
                    run_type,
                    'runs' || today(),
                    id as id_in_file,
            from read_csv('{file_path}') RETURNING ID, id_in_file"""
        )
        res = res.fetchall()
        print(
            f"Inserted {len(res)} row(s) in {'csv_runs_test' if test else 'csv_runs'}"
        )
        for result in res:
            print(f"New run {result[0]} inserted (row {result[1]} in csv)")
        if res:
            # run_dbt()
            return res


def insert_lap_csv(file_path: str, runs_data: list, test: bool = False):
    df = pd.DataFrame(data=runs_data, columns=["id", "id_in_file"])
    with duckdb.connect(db_path) as con:
        con.execute(f"""
                create table if not exists {"laps_csv_test" if test else "laps_csv"} (
                    id uuid primary key,
                    run_id uuid references {"csv_runs_test" if test else "csv_runs"}(id) not null,
                    time_minutes float not null,
                    min_per_km float,
                    cardiac_freq integer,
                    elevation_gain FLOAT,
                    cadence FLOAT
                )
        """)
        res = con.execute(
            f"""INSERT INTO {"laps_csv_test" if test else "laps_csv"}(
            id, 
            run_id,
            time_minutes,
            min_per_km,
            cardiac_freq,
            elevation_gain,
            cadence) 
                SELECT uuid() as id,
                d.id as run_id,
                time_minutes,
                min_per_km,
                cardiac_freq,
                elevation_gain,
                cadence
                from read_csv('{file_path}') f
                join df d on d.id_in_file = f.run_id 
                RETURNING id, run_id """
        )
        res = res.fetchall()
        print(f"Inserted {len(res)} new laps")
        for result in res:
            print(f"Inserted {result[0]} linked to run {result[1]}")


def insert_hr_zones_csv(file_path: str, runs_data: list, test: bool = False):
    df = pd.DataFrame(data=runs_data, columns=["id", "id_in_file"])
    with duckdb.connect(db_path) as con:
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {"hr_zones_csv_test" if test else "hr_zones_csv"} (
                id uuid PRIMARY KEY,
                run_id uuid REFERENCES {"csv_runs_test" if test else "csv_runs"}(id) NOT NULL,
                zone_name string,
                min_hr int,
                max_hr int,
                time float
            );
            """
        )
        res = con.execute(
            f"""
            INSERT INTO {"hr_zones_csv_test" if test else "hr_zones_csv"}
            SELECT uuid() as id ,
                d.id as run_id,
                zone_name,
                min_hr,
                max_hr,
                time
            from read_csv('{file_path}') f
            join df d on d.id_in_file = f.run_id
            RETURNING id, run_id"""
        )
        res = res.fetchall()
        print(f"Inserted {len(res)} new hr zones")
        for result in res:
            print(f"Inserted {result[0]} linked to run {result[1]}")


def insert_interval_csv(file_path: str, runs_data: list, test: bool = False):
    df = pd.DataFrame(data=runs_data, columns=["id", "id_in_file"])
    with duckdb.connect(db_path) as con:
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {"intervals_csv_test" if test else "intervals_csv"} (
                id UUID PRIMARY KEY,
                run_id UUID REFERENCES {"csv_runs_test" if test else "csv_runs"} (id) NOT NULL,
                interval_type STRING,
                distance_meters INT,
                duration_minutes FLOAT,
                rythm FLOAT,
                cardiac_frequency INT,
                cadence INT
            )"""
        )
        res = con.execute(
            f"""
            INSERT INTO {"intervals_csv_test" if test else "intervals_csv"}
            SELECT uuid() as id,
                d.id as run_id,
                interval_type,
                distance_meters,
                duration_minutes,
                rythm,
                cardiac_frequency,
                cadence
            from read_csv('{file_path}') f
            join df d on d.id_in_file = f.run_id 
            RETURNING id, run_id"""
        )
        res = res.fetchall()
        print(f"Inserted {len(res)} new intervals")
        for result in res:
            print(f"Inserted {result[0]} linked to run {result[1]}")


def destroy_test_resources():
    print("Destroying resources following dry run")
    with duckdb.connect(db_path) as con:
        con.execute(
            """
            DROP TABLE IF EXISTS hr_zones_csv_test;
            DROP TABLE IF EXISTS laps_csv_test;
            DROP TABLE IF EXISTS intervals_csv_test;
            DROP TABLE IF EXISTS csv_runs_test;
            """
        )


def insert_lap(args: argparse.Namespace) -> str | None:
    return _insert_lap(
        args.run,
        args.time,
        args.min_per_km,
        args.cardiac_freq,
        args.elevation_gain,
        args.cadence,
    )


def _insert_lap(
    run_id: str,
    time_minutes: float,
    min_per_km: float,
    cardiac_frequency: int,
    elevation_gain: float,
    cadence: int,
) -> str | None:
    with duckdb.connect(db_path) as con:
        res = con.execute(
            """
            INSERT INTO laps (
                id, 
                run_id, 
                time_minutes, 
                min_per_km, 
                cardiac_freq,
                elevation_gain,
                cadence
                )
            values (uuid(), ?, ?, ?, ?, ?, ?)
            RETURNING ID
            """,
            [
                run_id,
                time_minutes,
                min_per_km,
                cardiac_frequency,
                elevation_gain,
                cadence,
            ],
        )
        res = res.fetchone()
        if res:
            run_dbt()
            return str(res[0])


def insert_injury(args: argparse.Namespace) -> str | None:
    return _insert_injury(args.date, args.comment)


def _insert_injury(injury_date: str, comment: str) -> str | None:
    with duckdb.connect(db_path) as con:
        res = con.execute(
            """
            INSERT INTO injuries(id, date, comment) values (uuid(), ?, ?)
            """,
            [injury_date, comment],
        )
        res = res.fetchone()
        if res:
            run_dbt()
            return str(res[0])


def insert_competition(args: argparse.Namespace) -> str | None:
    return _insert_competition(
        args.location, args.kilometers, args.date, args.type_race, args.elevation_gain
    )


def _insert_competition(
    location: str,
    kilometers: float,
    competition_date: str,
    race_type: str,
    elevation_gain: float,
) -> str | None:
    with duckdb.connect(db_path) as con:
        res = con.execute(
            """
            INSERT INTO competitions(id, location, length_km, date, race_type, elevation_gain)
            values(uuid(), ?, ?, ?, ?, ?)
            """,
            [location, kilometers, competition_date, race_type, elevation_gain],
        )
        res = res.fetchone()
        if res:
            run_dbt()
            return str(res[0])

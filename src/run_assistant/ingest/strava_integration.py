from pathlib import Path
import duckdb
import unicodedata
import re
from run_assistant.db.initialize_db import db_path
from run_assistant.ingest.ingestion_helpers import run_dbt

STRAVA_COLUMN_ALIASES: dict[str, list[str]] = {
    "activity_id": ["Activity ID", "Identifiant de l'activité"],
    "activity_date": ["Activity Date", "Date de l'activité"],
    "activity_type": ["Activity Type", "Type d'activité"],
    "elapsed_time_s": ["Elapsed Time", "Temps écoulé"],
    "moving_time_s": ["Moving Time", "Temps de déplacement"],
    "distance": ["Distance"],
    "max_heart_rate": [
        "Max Heart Rate",
        "Fréquence cardiaque maximale",
        "Fréquence cardiaque max.",
    ],
    "average_heart_rate": ["Average Heart Rate", "Fréquence cardiaque moyenne"],
    "elevation_gain": ["Elevation Gain", "Dénivelé positif"],
    # Pas besoin de mapper les 103 colonnes — seulement celles que tu utilises vraiment
}


def _slugify(header: str) -> str:
    header = unicodedata.normalize("NFKD", header).encode("ascii", "ignore").decode()
    header = re.sub(r"[^\w\s]", "", header).strip().lower()
    return re.sub(r"\s+", "_", header)


def _build_rename_map(headers: list) -> dict[str, str]:
    alias_lookup = {
        v: k for k, variants in STRAVA_COLUMN_ALIASES.items() for v in variants
    }
    rename_map, unknown = {}, []
    for h in headers:
        if h in alias_lookup:
            rename_map[h] = alias_lookup[h]
        else:
            rename_map[h] = _slugify(h)
            unknown.append(h)
    return rename_map


def insert_activities_file(file_path: str) -> None:
    with duckdb.connect(db_path) as con:
        headers = [
            c[0]
            for c in con.execute(
                """
                SELECT * from read_csv(?, header=true) LIMIT 0
                """,
                [file_path],
            ).description
        ]
        rename_map: dict = _build_rename_map(headers)
        con.execute("DROP TABLE IF EXISTS strava_activities_data")
        cols_sql = ", ".join(f'"{old}" AS "{new}"' for old, new in rename_map.items())
        con.execute(
            f"""CREATE TABLE strava_activities_data AS 
            SELECT {cols_sql}
            FROM read_csv(?, header=true, all_varchar=true)
            """,
            [file_path],
        )
    run_dbt()


if __name__ == "__main__":
    file_path = "~/Downloads/export_1591951165/activities.csv"
    insert_activities_file(file_path)

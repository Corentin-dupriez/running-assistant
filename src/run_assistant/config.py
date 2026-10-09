from pathlib import Path

package_root = Path(__file__).resolve().parent


def get_db_path() -> Path:
    return package_root.parent.parent / "run_assistant.duckdb"


db_path = get_db_path()

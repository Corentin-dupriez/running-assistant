import os
from pathlib import Path
from run_assistant.db.initialize_db import db_path
import duckdb

if __name__ == "__main__":
    migrations_folder = Path(os.getcwd()) / "db" / "migrations"
    last_migration = sorted(os.listdir(migrations_folder))[-1]
    with open(migrations_folder / last_migration, "r") as f:
        migration_content = f.read()
        if migration_content.strip()[-1] == ";":
            migration_content = migration_content.strip()[:-1]
            print(migration_content)
        with duckdb.connect(db_path) as con:
            con.execute(migration_content)

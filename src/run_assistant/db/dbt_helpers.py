import os
from pathlib import Path
from dbt.cli.main import dbtRunner


def run_dbt() -> None:
    file_path = Path(os.path.dirname(__file__))
    dbt_folder = file_path.parent.parent / "run_assistant_analytics"
    print(dbt_folder)
    dbt_runner = dbtRunner()
    cli_args = ["run", "--project-dir", f"{dbt_folder}"]
    _ = dbt_runner.invoke(args=cli_args)


if __name__ == "__main__":
    run_dbt()

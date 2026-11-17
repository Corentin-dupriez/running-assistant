from os import listdir, rename, chdir, path, mkdir
from pathlib import Path
from shutil import move
from datetime import datetime
from run_assistant.config import package_root
from run_assistant.ingest.ingestion_helpers import (
    insert_run_csv,
    insert_lap_csv,
    insert_hr_zones_csv,
    insert_interval_csv,
    destroy_test_resources,
)


def insert_files(test: bool = False, destroy: bool = False) -> None:
    functions_mapper = {
        "run": insert_run_csv,
        "laps": insert_lap_csv,
        "hr_zones": insert_hr_zones_csv,
        "intervals": insert_interval_csv,
    }

    inbox_folder = package_root.parent.parent / "inbox"

    files_to_process = {file.split(".")[0]: file for file in listdir(inbox_folder)}

    res = None

    for action, file in sorted(files_to_process.items(), reverse=True):
        if res is not None:
            functions_mapper[action](Path(inbox_folder) / file, res, test)
        else:
            res = functions_mapper[action](Path(inbox_folder) / file, test)

        clean_up_file(file, inbox_folder, test)

    if test and destroy:
        destroy_test_resources()


def clean_up_file(file: str, inbox_folder: Path, test: bool = False):
    archive_folder = package_root.parent.parent / "archive"
    source = inbox_folder / file
    dest = (
        archive_folder
        / f"{file.split('.')[0]}-{datetime.now().strftime('%Y-%m-%d')}.csv"
    )
    print(f"Moving file {source} to {dest}")
    if not test:
        if not path.exists(archive_folder):
            mkdir(archive_folder)
        move(
            src=source,
            dst=archive_folder,
        )
        chdir(archive_folder)
        rename(file, f"{file.split('.')[0]}-{datetime.now().strftime('%Y-%m-%d')}.csv")


if __name__ == "__main__":
    insert_files()

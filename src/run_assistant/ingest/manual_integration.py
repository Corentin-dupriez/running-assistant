import argparse
from run_assistant.ingest.ingestion_helpers import (
    insert_run,
    insert_lap,
    insert_injury,
    insert_competition,
)
from run_assistant.db.initialize_db import db_path, create_db
from run_assistant.db.queries import retrieve_runs

create_db()

parser = argparse.ArgumentParser(prog="Run assistant")
subparsers = parser.add_subparsers()

# Sub parser to add run information
parser_run = subparsers.add_parser("add-run")
parser_run.add_argument("-km", "--kilometers")
parser_run.add_argument("-t", "--time")
parser_run.add_argument("-d", "--date")
parser_run.add_argument("-r", "--rythm")
parser_run.add_argument("-c", "--cardiac_freq")
parser_run.add_argument("-e", "--elevation")
parser_run.add_argument("-en", "--equipment_name")
parser_run.add_argument("-ei", "--equipment_id")
parser_run.add_argument("-mp", "--max_pace")
parser_run.add_argument("-ap", "--average_pace")
parser_run.add_argument("-pe", "--perceived_effort")
parser_run.set_defaults(func=insert_run)

# Sub parser to add lap information
parser_laps = subparsers.add_parser("add-lap")
parser_laps.add_argument("-r", "--run")
parser_laps.add_argument("-t", "--time")
parser_laps.add_argument("-m", "--min_per_km")
parser_laps.add_argument("-c", "--cardiac_freq")
parser_laps.set_defaults(func=insert_lap)

parser_display_runs = subparsers.add_parser("show-runs")
parser_display_runs.set_defaults(func=retrieve_runs)

parser_injuries = subparsers.add_parser("add-injury")
parser_injuries.add_argument("-d", "--date")
parser_injuries.add_argument("-c", "--comment")
parser_injuries.set_defaults(func=insert_injury)

parser_competitions = subparsers.add_parser("add-competition")
parser_competitions.add_argument("-l", "--location")
parser_competitions.add_argument("-km", "--kilometers")
parser_competitions.add_argument("-d", "--date")
parser_competitions.add_argument("-t", "--type_race")
parser_competitions.set_defaults(func=insert_competition)

args = parser.parse_args()

res = args.func(args)

print(f"Inserted row: {res}")

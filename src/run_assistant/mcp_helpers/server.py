from typing import Any, List
from mcp.server import MCPServer
from datetime import date
from run_assistant.db import queries
from run_assistant.ingest import ingestion_helpers

mcp = MCPServer()


@mcp.tool()
def add_running_session(
    km: float,
    time: float,
    date: date,
    elevation_gain: float,
    rythm: float,
    cardiac_frequency: int,
) -> str | None:
    """
    This function is used to create a new running session.
    Args:
        km: The distance of the run in kilometers. A float value.
        time: The duration of the run in minutes. A float value.
        date: The date of the run.
        elevation_gain: The elevation gain in meters during the run. A float value
        rythm: The average rythm in minutes per km. A float value
        cardiac_frequency: The average cardiac frequency during the run. An integer value
    Returns:
        The UUID of the created row in a string
    """
    res: str | None = ingestion_helpers._insert_run(
        km, time, date, elevation_gain, rythm, cardiac_frequency
    )
    return res


@mcp.tool()
def add_running_lap(
    running_id: str, time: float, min_per_km: float, cardiac_frequency: int
) -> str | None:
    """
    This function is used to create a lap and attach it to an existing run.
    Laps are not necessarily litteral laps, they can be 1km chunks of a run. This is used in order
    to calculate the best km sections.
    Args:
        running_id: The ID of the run to attach the lap to
        time: The time of the lap
        min_per_km: The rythm of the lap in minutes per kilometers
        cardiac_frequency: The average cardiac frequency during this lap
    Returns:
        The ID of the inserted lap
    """
    res: str | None = ingestion_helpers._insert_lap(
        running_id, time, min_per_km, cardiac_frequency
    )
    return res


@mcp.tool()
def get_runs() -> List[dict[str, Any]]:
    """
    This function is used to retrieve all the runs in the database.
    The returned data is the raw data as inserted, and doesn't use any dbt mart.
    For this reason, if the goal is to have analytical insight, it is preferred to use a
    function retrieving data from marts, such as get_monthly_run_statistics or get_weekly_run_statistics
    Returns:
        A list of dictionary items containing the column names and the value contained in the column
    """
    return queries.retrieve_runs()


@mcp.tool()
def get_weekly_run_statistics(start_year: int | None = None) -> List[dict[str, Any]]:
    """
    This function is used to retrieve the weekly statistics of the user.
    It uses a custom dbt mart that consolidates all of the running sessions of the week into week chunks.
    The start_year parameter can be used in order to limit the results returned from a certain year.
    Args:
        start_year: The year from which the results should be displayed. Runs from before that year will not be returned
    Returns:
        A list of dictionary items containing the name of the column and the values associated to it
    """
    return queries.retrieve_weekly_run_info(start_year)


@mcp.tool()
def get_monthly_run_statistics(start_year: int | None = None):
    """
    This function is used to retrieve the monthly statistics of the user.
    It uses a custom dbt mart that consolidates all of the running sessions of the month into month chunks.
    The start_year parameter can be used in order to limit the results returned from a certain year.
    Args:
        start_year: The year from which the results should be displayed. Runs from before that year will not be returned
    Returns:
        A list of dictionary items containing the name of the column and the values associated to it
    """

    return queries.retrieve_monthly_run_info(start_year)


if __name__ == "__main__":
    mcp.run(transport="stdio")

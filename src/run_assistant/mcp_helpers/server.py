from mcp.server import MCPServer
from datetime import date
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
    res: str | None = ingestion_helpers._insert_lap(
        running_id, time, min_per_km, cardiac_frequency
    )
    return res


@mcp.tool()
def get_runs():
    return ingestion_helpers.retrieve_runs()


@mcp.tool()
def get_weekly_run_statistics(start_year: int | None = None):
    return ingestion_helpers.retrieve_weekly_run_info(start_year)


@mcp.tool()
def get_monthly_run_statistics(start_year: int | None = None):
    return ingestion_helpers.retrieve_monthly_run_info(start_year)


if __name__ == "__main__":
    mcp.run(transport="stdio")

# Run assistant

This repo is a run assistant using Claude, that understands your running
experience and schedule to tailor its advice.

The idea of creating such an assistant came from the useful functionality
of Strava Athlete intelligence, that is sadly hidden behind a subscription.
Here, this solution is using open source tools, and requires only an Anthropic
API key to give you tailored advice.

## Project structure

This project is composed of the `run_assistant` folder, containing all
the database, data integration and MCP logic, and the `run_assistant_analytics`
folder, that contains the dbt transformations, to transform the raw data about
running schedules, trainings ... into marts that can be easily used by the AI to
provide meaningful analysis and tailored advice.

The idea of using `dbt` as a transformation layer is to limit the cost of transforming
data with the AI itself, and instead provide ready-to-use resources, that can
be called by the AI via MCP tools.

```tree
run_assistant/
  src/
    run_assistant/
      core/
      db/
      ingest/
      mcp_helpers/
      main.py
    run_assistant_analytics/
```

import argparse
import os
from datetime import datetime

import requests

from src.clubelo.update import update_clubelo
from src.footballdata.update import update_footballdata
from src.fpl.fetch import fetch_bootstrap_static, fetch_event_status
from src.fpl.update import update_fpl
from src.theoddsapi.update import update_theoddsapi
from src.understat.update import update_understat


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Update FPL data")
    parser.add_argument(
        "command", choices=["update"], help="The command to run (e.g., 'update')"
    )
    args = parser.parse_args()

    if args.command == "update":
        update()


def update():
    """Fetch and update data from all sources."""

    theoddsapi_api_key = os.getenv("THEODDSAPI_API_KEY")
    if not theoddsapi_api_key:
        raise ValueError("THEODDSAPI_API_KEY environment variable is not set.")

    # Fetch current data and game state
    bootstrap_static = fetch_bootstrap_static()
    event_status = fetch_event_status()
    static_events = bootstrap_static["events"]
    current_season = get_current_season(static_events)
    current_gameweek = get_current_gameweek(static_events)
    next_gameweek = get_next_gameweek(static_events)

    if current_season == 2025:
        overall_league_id = 314
    else:
        raise ValueError("Overall league ID for current season is not set.")

    # Update all data
    update_fpl(
        current_season,
        current_gameweek,
        next_gameweek,
        overall_league_id,
        bootstrap_static,
        event_status,
    )
    update_understat(current_season, bootstrap_static)
    update_theoddsapi(
        theoddsapi_api_key, current_season, next_gameweek, bootstrap_static
    )
    update_footballdata(current_season, bootstrap_static)

    try:
        update_clubelo(bootstrap_static)
    except requests.exceptions.ConnectionError:
        print("Failed to update Club Elo data due to connection error.")


def get_current_season(static_events: list[dict]) -> int:
    return datetime.fromisoformat(static_events[0]["deadline_time"]).year


def get_current_gameweek(static_events: list[dict]) -> int | None:
    for event in static_events:
        if event["is_current"]:
            return event["id"]
    return None


def get_next_gameweek(static_events: list[dict]) -> int | None:
    for event in static_events:
        if event["is_next"]:
            return event["id"]
    return None


if __name__ == "__main__":
    main()

import argparse
from datetime import datetime

from src.fetch.fpl import fetch_bootstrap_static, fetch_event_status
from src.update.clubelo import update_clubelo
from src.update.fpl import update_fpl
from src.update.understat import update_understat


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

    # Fetch current data and game state
    bootstrap_static = fetch_bootstrap_static()
    event_status = fetch_event_status()
    static_events = bootstrap_static["events"]
    current_season = get_current_season(static_events)
    current_gameweek = get_current_gameweek(static_events)
    next_gameweek = get_next_gameweek(static_events)

    if current_season == "2025-26":
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
    update_clubelo(bootstrap_static)
    update_understat(current_season, bootstrap_static)


def get_current_season(static_events: list[dict]) -> str:
    year = datetime.fromisoformat(static_events[0]["deadline_time"]).year
    return f"{year}-{str(year + 1)[-2:]}"


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

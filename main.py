import argparse
from datetime import datetime

from src.fetch.fpl import fetch_bootstrap_static
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

    # Determine the current season and the next gameweek
    bootstrap_static = fetch_bootstrap_static()
    static_events = bootstrap_static["events"]
    current_season = get_current_season(static_events)
    next_gameweek = get_next_gameweek(static_events)

    # Update all data
    update_fpl(current_season, next_gameweek, bootstrap_static)
    update_clubelo(bootstrap_static)
    update_understat(current_season, bootstrap_static)


def get_current_season(static_events: list[dict]) -> str:
    year = datetime.fromisoformat(static_events[0]["deadline_time"]).year
    return f"{year}-{str(year + 1)[-2:]}"


def get_next_gameweek(static_events: list[dict]) -> int | None:
    for event in static_events:
        if event["is_next"]:
            return event["id"]
    return None


if __name__ == "__main__":
    main()

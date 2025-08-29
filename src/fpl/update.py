from tqdm import tqdm

from src.fpl.fetch import (
    fetch_element_summary,
    fetch_entry_picks,
    fetch_fixtures,
    fetch_league_standings,
)
from src.utils import DATA_DIR, write_compressed_json, write_csv


def update_fpl(
    current_season: str,
    current_gameweek: int | None,
    next_gameweek: int | None,
    overall_league_id: int,
    bootstrap_static: dict,
    event_status: dict,
):
    update_bootstrap_static(current_season, next_gameweek, bootstrap_static)
    update_fixtures(current_season)
    update_elements(current_season, bootstrap_static)
    update_top_10k(current_season, current_gameweek, overall_league_id, event_status)


def update_bootstrap_static(
    current_season: str, next_gameweek: int | None, bootstrap_static: dict
):
    if next_gameweek:
        path = DATA_DIR / f"fpl/{current_season}/static/{next_gameweek}.json.xz"
    else:
        path = DATA_DIR / f"fpl/{current_season}/static/final.json.xz"
    write_compressed_json(bootstrap_static, path)


def update_fixtures(current_season: str):
    fixtures = fetch_fixtures()
    path = DATA_DIR / f"fpl/{current_season}/fixtures.csv"
    write_csv(fixtures, path)


def update_elements(current_season: str, bootstrap_static: dict):
    static_elements = bootstrap_static["elements"]
    element_ids = [element["id"] for element in static_elements]
    for element_id in tqdm(element_ids, desc="Updating elements"):
        element_summary = fetch_element_summary(element_id)
        history = element_summary["history"]
        path = DATA_DIR / f"fpl/{current_season}/elements/{element_id}.csv"
        write_csv(history, path)


def update_top_10k(
    current_season: str,
    current_gameweek: int | None,
    overall_league_id: int,
    event_status: dict,
):
    # Retrieve standings only once and after each gameweek
    if (current_gameweek is None) or (event_status["leagues"] != "Updated"):
        return
    path = DATA_DIR / f"fpl/{current_season}/top_10k/{current_gameweek}.json.xz"
    if path.exists():
        return

    standings = []
    for i in tqdm(range(1, 201), desc="Fetching top 10k standings"):
        data = fetch_league_standings(overall_league_id, i)
        standings.extend(data["standings"]["results"])

    picks = {}
    for item in tqdm(standings, desc="Fetching top 10k picks"):
        data = fetch_entry_picks(item["entry"], current_gameweek)
        picks[item["entry"]] = data

    for manager in standings:
        manager["picks"] = picks[manager["entry"]]

    write_compressed_json(standings, path)

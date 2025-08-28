from tqdm import tqdm

from src.fetch.fpl import (
    fetch_element_summary,
    fetch_entry_picks,
    fetch_fixtures,
    fetch_league_standings,
)
from src.utils import DATA_DIR, write_csv, write_json_xz


def update_fpl(
    current_season: str,
    current_gameweek: int | None,
    next_gameweek: int | None,
    overall_league_id: int,
    bootstrap_static: dict,
    event_status: dict,
):
    # Update bootstrap static
    if next_gameweek:
        path = DATA_DIR / f"fpl/{current_season}/static/{next_gameweek}.json.xz"
    else:
        path = DATA_DIR / f"fpl/{current_season}/static/final.json.xz"
    write_json_xz(bootstrap_static, path)

    # Update fixtures
    fixtures = fetch_fixtures()
    path = DATA_DIR / f"fpl/{current_season}/fixtures.csv"
    write_csv(fixtures, path)

    # Update elements
    static_elements = bootstrap_static["elements"]
    element_ids = [element["id"] for element in static_elements]
    for element_id in tqdm(element_ids, desc="Updating elements"):
        element_summary = fetch_element_summary(element_id)
        history = element_summary["history"]
        path = DATA_DIR / f"fpl/{current_season}/elements/{element_id}.csv"
        write_csv(history, path)

    # Update top 10K picks. This should be done only once for each gameweek.
    if (current_gameweek is not None) and (event_status["leagues"] == "Updated"):
        path = DATA_DIR / f"fpl/{current_season}/top_10k/{current_gameweek}.json.xz"
        if not path.exists():
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

            write_json_xz(standings, path)

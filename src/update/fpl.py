from tqdm import tqdm

from src.fetch.fpl import fetch_element_summary, fetch_fixtures
from src.utils import DATA_DIR, write_csv, write_json_xz


def update_fpl(current_season: str, next_gameweek: int | None, bootstrap_static: dict):
    # Update bootstrap static
    path = DATA_DIR / f"fpl/{current_season}/static/{next_gameweek}.json.xz"
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

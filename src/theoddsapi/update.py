from src.theoddsapi.fetch import fetch_odds
from src.utils import DATA_DIR, write_compressed_json


def update_theoddsapi(api_key: str, current_season: str, next_gameweek: int):
    data = fetch_odds(api_key, "soccer_epl", "uk", "h2h")
    path = DATA_DIR / f"theoddsapi/{current_season[:4]}/{next_gameweek}.json.xz"
    write_compressed_json(data, path)

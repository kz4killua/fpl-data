from src.utils import DATA_DIR, read_compressed_json, read_csv


def read_odds(season: str, gameweek: int) -> dict:
    path = DATA_DIR / f"theoddsapi/{season[:4]}/{gameweek}.json.xz"
    return read_compressed_json(path)


def read_team_ids() -> dict:
    path = DATA_DIR / "theoddsapi/team_ids.csv"
    return read_csv(path)

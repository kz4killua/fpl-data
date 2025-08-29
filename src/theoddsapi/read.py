import csv
import json
import lzma

from src.utils import DATA_DIR


def read_odds(season: str, gameweek: int) -> dict:
    path = DATA_DIR / f"theoddsapi/{season[:4]}/{gameweek}.json.xz"
    with lzma.open(path, "rt") as f:
        data = json.load(f)
    return data


def read_team_ids() -> dict:
    path = DATA_DIR / "theoddsapi/team_ids.csv"
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
import csv

from src.utils import DATA_DIR


def read_historical_data(season: str):
    path = DATA_DIR / f"footballdata/data/{season[:4]}.csv"
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def read_team_ids():
    path = DATA_DIR / "footballdata/team_ids.csv"
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

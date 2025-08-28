import csv

from src.utils import DATA_DIR


def read_fixtures(season: str):
    path = DATA_DIR / f"fpl/{season}/fixtures.csv"
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

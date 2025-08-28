import csv

from src.utils import DATA_DIR


def read_team_ids():
    path = DATA_DIR / "clubelo/team_ids.csv"
    with open(path, encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

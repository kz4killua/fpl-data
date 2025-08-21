import csv

from src.utils import DATA_DIR


def read_player_ids():
    path = DATA_DIR / "understat/player_ids.csv"
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def read_team_ids():
    path = DATA_DIR / "understat/team_ids.csv"
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

from src.utils import DATA_DIR, read_csv


def read_player_ids():
    path = DATA_DIR / "understat/player_ids.csv"
    return read_csv(path)


def read_team_ids():
    path = DATA_DIR / "understat/team_ids.csv"
    return read_csv(path)

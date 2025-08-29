from src.utils import DATA_DIR, read_csv


def read_team_ids():
    path = DATA_DIR / "clubelo/team_ids.csv"
    return read_csv(path)

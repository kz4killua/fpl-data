from src.utils import DATA_DIR, read_csv


def read_historical_data(season: str):
    path = DATA_DIR / f"footballdata/data/{season[:4]}.csv"
    return read_csv(path)


def read_team_ids():
    path = DATA_DIR / "footballdata/team_ids.csv"
    return read_csv(path)

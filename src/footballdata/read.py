from src.utils import DATA_DIR, read_csv


def read_historical_data(season: int):
    """Load historical results & betting odds for a given season."""
    path = DATA_DIR / f"footballdata/data/{season}.csv"
    return read_csv(path)


def read_team_ids():
    """Load Football Data team ID mappings."""
    path = DATA_DIR / "footballdata/team_ids.csv"
    return read_csv(path)

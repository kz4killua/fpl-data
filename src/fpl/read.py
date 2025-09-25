from src.utils import DATA_DIR, read_csv


def read_fixtures(season: int):
    """Load FPL fixture information from disk."""
    path = DATA_DIR / f"fpl/{season}/fixtures.csv"
    return read_csv(path)

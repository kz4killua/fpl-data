from src.footballdata.fetch import fetch_historical_data
from src.utils import DATA_DIR, write_csv


def update_footballdata(current_season: str):
    data = fetch_historical_data(current_season)
    path = DATA_DIR / f"footballdata/{current_season[:4]}.csv"
    write_csv(data, path)

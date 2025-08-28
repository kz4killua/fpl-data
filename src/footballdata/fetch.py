from csv import DictReader
from io import StringIO

import requests

BASE_URL = "https://www.football-data.co.uk"


def fetch_historical_data(season: str):
    """Fetch historical results & betting odds for a given season."""
    year = int(season[:4])
    key = str(year)[2:] + str(year + 1)[2:]
    response = requests.get(f"{BASE_URL}/mmz4281/{key}/E0.csv")
    reader = DictReader(StringIO(response.text))
    return list(reader)

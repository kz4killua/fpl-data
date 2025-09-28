import requests

BASE_URL = "https://api.the-odds-api.com"


def fetch_odds(api_key: str):
    """Fetch odds for live and upcoming matches from The Odds API."""
    params = {
        "apiKey": api_key,
        "regions": "us,uk,eu",
        "markets": "h2h,spreads,totals",
        "dateFormat": "iso",
        "oddsFormat": "decimal",
    }
    response = requests.get(f"{BASE_URL}/v4/sports/soccer_epl/odds", params=params)
    response.raise_for_status()
    return response.json()

import requests

BASE_URL = "https://api.the-odds-api.com"


def fetch_odds(api_key: str, sport: str, regions: str, markets: str):
    """Fetch betting odds from The Odds API."""
    params = {"apiKey": api_key, "regions": regions, "markets": markets}
    response = requests.get(f"{BASE_URL}/v4/sports/{sport}/odds", params=params)
    response.raise_for_status()
    return response.json()

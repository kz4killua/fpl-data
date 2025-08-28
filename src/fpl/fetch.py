import requests

BASE_URL = "https://fantasy.premierleague.com/api"


def fetch_element_summary(element_id: int) -> dict:
    """Fetches data for a specific FPL element (a player or manager)."""
    response = requests.get(f"{BASE_URL}/element-summary/{element_id}/")
    response.raise_for_status()
    return response.json()


def fetch_fixtures() -> list[dict]:
    """Fetches FPL fixture information."""
    response = requests.get(f"{BASE_URL}/fixtures/")
    response.raise_for_status()
    return response.json()


def fetch_bootstrap_static() -> dict:
    """Fetches the current FPL game state."""
    response = requests.get(f"{BASE_URL}/bootstrap-static/")
    response.raise_for_status()
    return response.json()


def fetch_event_status() -> dict:
    """Fetch the current FPL event status."""
    response = requests.get(f"{BASE_URL}/event-status/")
    response.raise_for_status()
    return response.json()


def fetch_league_standings(league_id: int, page: int) -> dict:
    """Fetch overall standings for a given league."""
    params = {"page_new_entries": 1, "page_standings": page, "phase": 1}
    response = requests.get(
        f"{BASE_URL}/leagues-classic/{league_id}/standings/", params=params
    )
    response.raise_for_status()
    return response.json()


def fetch_entry_picks(entry_id: int, event_id: int) -> dict:
    """Fetch picks, chip usage, bank amounts, etc. for a user."""
    response = requests.get(f"{BASE_URL}/entry/{entry_id}/event/{event_id}/picks/")
    response.raise_for_status()
    return response.json()

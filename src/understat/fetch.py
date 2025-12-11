import requests

BASE_URL = "https://understat.com"
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
}


def fetch_player_data(player_id: int) -> dict:
    response = requests.get(f"{BASE_URL}/getPlayerData/{player_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def fetch_league_data(league: str, season: int) -> dict:
    response = requests.get(
        f"{BASE_URL}/getLeagueData/{league}/{season}", headers=HEADERS
    )
    response.raise_for_status()
    return response.json()


def fetch_match_data(match_id: int) -> dict:
    response = requests.get(f"{BASE_URL}/getMatchData/{match_id}/", headers=HEADERS)
    response.raise_for_status()
    return response.json()

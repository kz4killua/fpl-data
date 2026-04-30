import httpx

BASE_URL = "https://understat.com"
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
}
TIMEOUT = 60


def fetch_player_data(player_id: int) -> dict:
    response = httpx.get(
        f"{BASE_URL}/getPlayerData/{player_id}", headers=HEADERS, timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def fetch_league_data(league: str, season: int) -> dict:
    response = httpx.get(
        f"{BASE_URL}/getLeagueData/{league}/{season}", headers=HEADERS, timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def fetch_match_data(match_id: int) -> dict:
    response = httpx.get(
        f"{BASE_URL}/getMatchData/{match_id}/", headers=HEADERS, timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()

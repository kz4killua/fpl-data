from tqdm import tqdm

from src.fetch.understat import (
    fetch_league_dates,
    fetch_league_players,
    fetch_league_teams,
    fetch_player_matches,
)
from src.utils import DATA_DIR, write_csv


def update_understat(current_season: str):
    current_year = int(current_season.split("-")[0])

    # Update dates
    dates = fetch_league_dates("EPL", current_year)
    for date in dates:
        date["h"] = date["h"]["id"]
        date["a"] = date["a"]["id"]
    path = DATA_DIR / f"understat/season/{current_year}/dates.csv"
    write_csv(dates, path)

    # Update teams
    teams = fetch_league_teams("EPL", current_year)
    for team in teams.values():
        history = team["history"]
        history["id"] = team["id"]
        history["title"] = team["title"]
        path = DATA_DIR / f"understat/season/{current_year}/teams/{team['id']}.csv"
        write_csv(history, path)

    # Update matches
    players = fetch_league_players("EPL", current_year)
    for player in tqdm(players, desc="Updating understat players"):
        player_id = int(player["id"])
        player_matches = fetch_player_matches(player_id)
        path = DATA_DIR / f"understat/player/matches/{player_id}.csv"
        write_csv(player_matches, path)

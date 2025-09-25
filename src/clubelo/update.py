from tqdm import tqdm

from src.clubelo.fetch import fetch_rating_history
from src.clubelo.read import read_team_ids
from src.utils import DATA_DIR, write_csv


def update_clubelo(bootstrap_static: dict):
    """Update Club Elo ratings for all teams in the current season."""
    static_teams = bootstrap_static["teams"]
    team_codes = [team["code"] for team in static_teams]

    # Load all Club Elo teams in the current season
    clubelo_teams = read_team_ids()
    clubelo_teams = [t for t in clubelo_teams if int(t["fpl_code"]) in team_codes]

    for team in tqdm(clubelo_teams, desc="Updating Club Elo ratings"):
        club_name = team["clubelo_name"]
        ratings = fetch_rating_history(club_name)
        path = DATA_DIR / f"clubelo/ratings/{club_name}.csv"
        write_csv(ratings, path)

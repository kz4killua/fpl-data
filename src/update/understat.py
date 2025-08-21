import difflib

from tqdm import tqdm

from src.fetch.understat import (
    fetch_league_dates,
    fetch_league_players,
    fetch_league_teams,
    fetch_player_matches,
)
from src.read.fpl import read_fixtures
from src.read.understat import read_player_ids, read_team_ids
from src.utils import DATA_DIR, append_csv, write_csv


def update_understat(current_season: str, bootstrap_static: dict):
    current_year = int(current_season.split("-")[0])

    # Update fixtures (dates)
    dates = fetch_league_dates("EPL", current_year)
    for date in dates:
        date["h_title"] = date["h"]["title"]
        date["a_title"] = date["a"]["title"]
        date["h"] = date["h"]["id"]
        date["a"] = date["a"]["id"]
    path = DATA_DIR / f"understat/season/{current_year}/dates.csv"
    write_csv(dates, path)

    # Update teams
    teams = fetch_league_teams("EPL", current_year)
    for team in tqdm(teams.values(), desc="Updating understat teams"):
        team_id = int(team["id"])
        history = team["history"]
        for item in history:
            item["id"] = team["id"]
            item["title"] = team["title"]
        path = DATA_DIR / f"understat/season/{current_year}/teams/{team_id}.csv"
        write_csv(history, path)

    # Update matches
    players = fetch_league_players("EPL", current_year)
    for player in tqdm(players, desc="Updating understat players"):
        player_id = int(player["id"])
        player_matches = fetch_player_matches(player_id)
        path = DATA_DIR / f"understat/player/matches/{player_id}.csv"
        write_csv(player_matches, path)

    # Update player, team, and fixture IDs
    update_understat_player_ids(players, bootstrap_static)
    update_understat_team_ids(teams, bootstrap_static)
    update_understat_fixture_ids(current_season, current_year, dates, bootstrap_static)


def update_understat_player_ids(uds_players: dict, bootstrap_static: dict):
    # Get existing mappings
    player_ids = read_player_ids()
    mapped_fpl = {int(row["fpl_code"]) for row in player_ids}
    mapped_uds = {int(row["understat_id"]) for row in player_ids}

    # Get all FPL players who have been involved in a match
    fpl_players = [
        e
        for e in bootstrap_static["elements"]
        if (e["minutes"] > 0) and (e["element_type"] in {1, 2, 3, 4})
    ]

    # Get all unmapped player codes / IDs
    unmapped_fpl = {p["code"] for p in fpl_players if p["code"] not in mapped_fpl}
    unmapped_uds = {int(p["id"]) for p in uds_players if int(p["id"]) not in mapped_uds}

    # Map player codes / IDs to their full names
    fpl_names = {
        p["code"]: get_fpl_name(p) for p in fpl_players if p["code"] in unmapped_fpl
    }
    uds_names = {
        int(p["id"]): p["player_name"]
        for p in uds_players
        if int(p["id"]) in unmapped_uds
    }

    # Update the CSV file with new mappings
    mappings = map_closest_names(fpl_names, uds_names)
    path = DATA_DIR / "understat/player_ids.csv"
    rows = [
        (fpl_code, uds_id, fpl_names[fpl_code], uds_names[uds_id])
        for fpl_code, uds_id in mappings.items()
    ]
    append_csv(rows, path)


def update_understat_team_ids(uds_teams: dict, bootstrap_static: dict):
    # Get existing mappings
    team_ids = read_team_ids()
    mapped_fpl = {int(row["fpl_code"]) for row in team_ids}
    mapped_uds = {int(row["understat_id"]) for row in team_ids}

    # Get all FPL codes that have not been mapped to understat IDs
    fpl_teams = bootstrap_static["teams"]
    unmapped_fpl = {t["code"] for t in fpl_teams if t["code"] not in mapped_fpl}
    unmapped_uds = {
        int(t["id"]) for t in uds_teams.values() if int(t["id"]) not in mapped_uds
    }

    # Map team codes / IDs to their full names
    fpl_names = {t["code"]: t["name"] for t in fpl_teams if t["code"] in unmapped_fpl}
    uds_names = {
        int(t["id"]): t["title"]
        for t in uds_teams.values()
        if int(t["id"]) in unmapped_uds
    }

    # Update the CSV file with new mappings
    mappings = map_closest_names(fpl_names, uds_names)
    path = DATA_DIR / "understat/team_ids.csv"
    rows = [
        (fpl_code, uds_id, fpl_names[fpl_code], uds_names[uds_id])
        for fpl_code, uds_id in mappings.items()
    ]
    append_csv(rows, path)


def update_understat_fixture_ids(
    current_season: str, current_year: int, uds_fixtures: list, bootstrap_static: dict
):
    # Load fixture and team data
    team_ids = read_team_ids()
    fpl_fixtures = read_fixtures(current_season)
    fpl_teams = bootstrap_static["teams"]

    # Start with FPL fixture and team IDs
    mappings = [
        {
            "fpl_fixture_id": int(f["id"]),
            "team_h_fpl_id": int(f["team_h"]),
            "team_a_fpl_id": int(f["team_a"]),
        }
        for f in fpl_fixtures
    ]

    # Add FPL team names
    fpl_team_names = {t["id"]: t["name"] for t in fpl_teams}
    for entry in mappings:
        entry["team_h_fpl_name"] = fpl_team_names[entry["team_h_fpl_id"]]
        entry["team_a_fpl_name"] = fpl_team_names[entry["team_a_fpl_id"]]

    # Add FPL team codes
    fpl_team_codes = {t["id"]: t["code"] for t in fpl_teams}
    for entry in mappings:
        entry["team_h_fpl_code"] = fpl_team_codes[entry["team_h_fpl_id"]]
        entry["team_a_fpl_code"] = fpl_team_codes[entry["team_a_fpl_id"]]

    # Add understat team IDs
    uds_team_ids = {int(row["fpl_code"]): int(row["understat_id"]) for row in team_ids}
    for entry in mappings:
        entry["team_h_uds_id"] = uds_team_ids[entry["team_h_fpl_code"]]
        entry["team_a_uds_id"] = uds_team_ids[entry["team_a_fpl_code"]]

    # Add understat fixture IDs
    uds_fixture_ids = {(int(f["h"]), int(f["a"])): int(f["id"]) for f in uds_fixtures}
    for entry in mappings:
        entry["uds_fixture_id"] = uds_fixture_ids[
            (entry["team_h_uds_id"], entry["team_a_uds_id"])
        ]

    # Add understat team names
    uds_fixture_team_names = {
        int(f["id"]): (f["h_title"], f["a_title"]) for f in uds_fixtures
    }
    for entry in mappings:
        entry["team_h_uds_name"], entry["team_a_uds_name"] = uds_fixture_team_names[
            entry["uds_fixture_id"]
        ]

    # Write the mappings to a CSV file
    mappings = [
        {
            "fpl_id": entry["fpl_fixture_id"],
            "understat_id": entry["uds_fixture_id"],
            "h_fpl": entry["team_h_fpl_name"],
            "a_fpl": entry["team_a_fpl_name"],
            "h_understat": entry["team_h_uds_name"],
            "a_understat": entry["team_a_uds_name"],
        }
        for entry in mappings
    ]
    path = DATA_DIR / f"understat/season/{current_year}/fixture_ids.csv"
    write_csv(mappings, path)


def get_fpl_name(element: dict) -> str:
    """Generate a full name for an FPL element."""
    first_name = element["first_name"]
    second_name = element["second_name"]
    web_name = element["web_name"]

    full_name = f"{first_name} {second_name}"
    if web_name not in full_name:
        full_name += f" ({web_name})"

    return full_name


def map_closest_names(a: dict, b: dict):
    """Maps each name in a.values() with the most similar name in b.values()"""
    mappings = dict()
    # Get all possible pairs
    pairs = [(k1, k2) for k1 in a for k2 in b]
    # Rank the pairs by similarity
    pairs.sort(
        key=lambda pair: calculate_similarity(a[pair[0]], b[pair[1]]), reverse=True
    )
    # Map each key in a to the closest key in b
    mapped_a = set()
    mapped_b = set()

    for pair in pairs:
        if not (pair[0] in mapped_a or pair[1] in mapped_b):
            # Add the mapping
            mappings[pair[0]] = pair[1]
            # Keep track of what we have already mapped
            mapped_a.add(pair[0])
            mapped_b.add(pair[1])

    return mappings


def calculate_similarity(s1: str, s2: str):
    """Returns a score indicating how similar two strings are."""
    s1 = s1.lower().strip()
    s2 = s2.lower().strip()
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()

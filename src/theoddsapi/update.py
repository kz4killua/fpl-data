from src.theoddsapi.fetch import fetch_odds
from src.theoddsapi.read import read_odds, read_team_ids
from src.utils import DATA_DIR, append_csv, map_closest_names, write_compressed_json


def update_theoddsapi(
    api_key: str, current_season: str, next_gameweek: int, bootstrap_static: dict
):
    update_odds(api_key, current_season, next_gameweek)
    update_team_ids(bootstrap_static, current_season, next_gameweek)


def update_odds(api_key: str, current_season: str, next_gameweek: int):
    data = fetch_odds(api_key, "soccer_epl", "uk", "h2h")
    path = DATA_DIR / f"theoddsapi/{current_season[:4]}/{next_gameweek}.json.xz"
    write_compressed_json(data, path)


def update_team_ids(bootstrap_static: dict, current_season: str, next_gameweek: int):
    fpl_teams = bootstrap_static["teams"]

    # List all team names from theoddsapi
    toa_data = read_odds(current_season, next_gameweek)
    toa_team_names = set()
    for match in toa_data:
        toa_team_names.add(match["home_team"])
        toa_team_names.add(match["away_team"])

    # Get existing mappings
    team_ids = read_team_ids()
    mapped_fpl = {int(row["fpl_code"]) for row in team_ids}
    mapped_toa = {row["theoddsapi_name"] for row in team_ids}

    # Get unmapped FPL codes and theoddsapi names
    unmapped_fpl = {t["code"] for t in fpl_teams if t["code"] not in mapped_fpl}
    unmapped_toa = {name for name in toa_team_names if name not in mapped_toa}

    # Map FPL team codes to their full names
    fpl_names = {t["code"]: t["name"] for t in fpl_teams if t["code"] in unmapped_fpl}
    toa_names = {name: name for name in unmapped_toa}

    # Update the CSV file with new mappings
    mappings = map_closest_names(fpl_names, toa_names)
    path = DATA_DIR / "theoddsapi/team_ids.csv"
    rows = [
        (fpl_code, fpl_names[fpl_code], toa_name)
        for fpl_code, toa_name in mappings.items()
    ]
    append_csv(rows, path)

from src.footballdata.fetch import fetch_historical_data
from src.footballdata.read import read_historical_data, read_team_ids
from src.utils import DATA_DIR, append_csv, map_closest_names, write_csv


def update_footballdata(current_season: str, bootstrap_static: dict):
    update_historical_data(current_season)
    update_team_ids(bootstrap_static, current_season)


def update_historical_data(current_season: str):
    data = fetch_historical_data(current_season)
    path = DATA_DIR / f"footballdata/data/{current_season[:4]}.csv"
    write_csv(data, path)


def update_team_ids(bootstrap_static: dict, current_season: str):
    fpl_teams = bootstrap_static["teams"]

    # List all team names from footballdata historical data
    fbd_data = read_historical_data(current_season)
    fbd_team_names = set()
    for row in fbd_data:
        fbd_team_names.add(row["HomeTeam"])
        fbd_team_names.add(row["AwayTeam"])

    # Get existing mappings
    team_ids = read_team_ids()
    mapped_fpl = {int(row["fpl_code"]) for row in team_ids}
    mapped_fbd = {row["footballdata_name"] for row in team_ids}

    # Get unmapped FPL codes and footballdata names
    unmapped_fpl = {t["code"] for t in fpl_teams if t["code"] not in mapped_fpl}
    unmapped_fbd = {name for name in fbd_team_names if name not in mapped_fbd}

    # Map FPL team codes to their full names
    fpl_names = {t["code"]: t["name"] for t in fpl_teams if t["code"] in unmapped_fpl}
    fbd_names = {name: name for name in unmapped_fbd}

    # Update the CSV file with new mappings
    mappings = map_closest_names(fpl_names, fbd_names)
    path = DATA_DIR / "footballdata/team_ids.csv"
    rows = [
        (fpl_code, fpl_names[fpl_code], fbd_name)
        for fpl_code, fbd_name in mappings.items()
    ]
    append_csv(rows, path)

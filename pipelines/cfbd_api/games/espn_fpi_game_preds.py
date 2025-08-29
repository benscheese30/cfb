from utils import cfbd
import os
import json
import requests

# getting game week
year = 2025
game_week = cfbd.get_week(year)

# pulling game data
raw_games = cfbd.get_data(
    endpoint="/games",
    params={
        "year": year,
        "division": "fbs"
    }
)

# filtering down to just fbs games
games_filtered = []
for gf in raw_games:
    if gf["homeClassification"] == "fbs" or gf["awayClassification"] == "fbs":
        games_filtered.append(gf)

# saving raw game data
with open("data/games/2025_game_list.json", "w", encoding="utf-8") as f:
    json.dump(raw_games, f, indent=2, ensure_ascii=False)

# saving filtered game data
local_path = f"data/games/2025_game_list_filtered.json"
with open(local_path, "w", encoding="utf-8") as f:
    json.dump(games_filtered, f, indent=2, ensure_ascii=False)

game_predictions = []
for g in games_filtered:
    if g["week"] >= game_week:
        print(g["id"])
        espn_url = f"http://sports.core.api.espn.com/v2/sports/football/leagues/college-football/events/{g['id']}/competitions/{g['id']}/predictor"
        response = requests.get(espn_url)
        if response.status_code == 200:
            game_predictions.append(response.json())
            print("success")

local_path = f"data/fpi_predictor/2025_game_week_{game_week}.json"

os.makedirs(os.path.dirname(local_path), exist_ok=True)

with open(local_path, "w", encoding="utf-8") as f:
    json.dump(game_predictions, f, indent=2, ensure_ascii=False)





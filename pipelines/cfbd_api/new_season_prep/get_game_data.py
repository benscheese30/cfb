from utils import cfbd
import json

# pulling game data
games = cfbd.get_data(
    endpoint="/games",
    params={
        "year": 2025,
        "division": "fbs"
    }
)

games_filtered = []
for g in games:
    if g["homeClassification"] == "fbs" or g["awayClassification"] == "fbs":
        games_filtered.append(g)

# saving raw game data
with open("data/games/2025_game_list.json", "w", encoding="utf-8") as f:
    json.dump(games, f, indent=2, ensure_ascii=False)

# saving filtered game data
local_path = f"data/games/2025_game_list_filtered.json"
with open(local_path, "w", encoding="utf-8") as f:
    json.dump(games_filtered, f, indent=2, ensure_ascii=False)
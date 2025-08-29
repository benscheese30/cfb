from utils import cfbd
from io import BytesIO
import json

year = 2025
team_info = cfbd.get_data(
    endpoint="/teams",
    params={"year": year}
)

with open(f"data/team_info/{year}.json", "wb") as f:
    f.write(json.dumps(team_info, indent=4, ensure_ascii=False).encode("utf-8"))


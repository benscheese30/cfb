from utils import cfbd, aws
from io import BytesIO
import json

year = 2025
game_week = cfbd.get_week(year)
# game_week = 14
game_week = "minus_1"

sp_plus_rankings = cfbd.get_data(
    endpoint="/ratings/sp",
    params={"year": year}
)

sp_plus_rankings

with open(f"data/sp_pull_rankings/{year}_week_{game_week}.json", "wb") as f:
    f.write(json.dumps(sp_plus_rankings, indent=4, ensure_ascii=False).encode("utf-8"))

# s3 = aws.aws_client(
#     aws.aws_config(service="s3", localstack=True)
# )

# s3.upload_fileobj(
#     Fileobj=BytesIO(json.dumps(sp_plus_rankings).encode()),
#     Bucket="college-football",
#     Key=f"data/espn/sp_rankings/{year}_week_{game_week}.json"
# )
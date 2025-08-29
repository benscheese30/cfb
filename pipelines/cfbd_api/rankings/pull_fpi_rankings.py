from utils import cfbd, aws
import json
from io import BytesIO


year = 2025
game_week = cfbd.get_week(year)
# game_week = "minus_1"

fpi_rankings = cfbd.get_data(
    endpoint="/ratings/fpi",
    params={"year": year}
)

with open(f"data/fpi_rankings/{year}_week_{game_week}.json", "wb") as f:
    f.write(json.dumps(fpi_rankings, indent=4, ensure_ascii=False).encode("utf-8"))

# upload to s3
# s3 = aws.aws_client(
#     aws.aws_config(service="s3", localstack=True)
# )

# s3.upload_fileobj(
#     Fileobj=BytesIO(json.dumps(fpi_rankings).encode()),
#     Bucket="college-football",
#     Key=f"data/espn/fpi_rankings/{year}_week_{game_week}.json"
# )

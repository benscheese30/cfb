from utils import cfbd, aws
from io import BytesIO
import json

year = 2024
game_week = cfbd.get_week(year)

sp_plus_rankings = cfbd.get_data(
    endpoint="/ratings/sp",
    params={"year": year}
)

s3 = aws.aws_client(
    aws.aws_config(service="s3", localstack=True)
)

s3.upload_fileobj(
    Fileobj=BytesIO(json.dumps(sp_plus_rankings).encode()),
    Bucket="college-football",
    Key=f"data/espn/sp_rankings/{year}_week_{game_week}.json"
)
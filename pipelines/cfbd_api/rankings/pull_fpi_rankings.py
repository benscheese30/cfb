from utils import cfbd, aws
import json
from io import BytesIO

year = 2024
game_week = cfbd.get_week(year)

fpi_rankings = cfbd.get_data(
    endpoint="/ratings/fpi",
    params={"year": year}
)

# upload to s3
s3 = aws.aws_client(
    aws.aws_config(service="s3", localstack=True)
)

s3.upload_fileobj(
    Fileobj=BytesIO(json.dumps(fpi_rankings).encode()),
    Bucket="college-football",
    Key=f"data/espn/fpi_rankings/{year}_week_{game_week}.json"
)

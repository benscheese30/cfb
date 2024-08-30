from utils import cfbd, aws
from io import BytesIO
import json

sp_plus_rankings = cfbd.get_data(
    endpoint="/ratings/sp",
    params={"year": 2024}
)

s3 = aws.aws_client(
    aws.aws_config(service="s3", localstack=True)
)

s3.upload_fileobj(
    Fileobj=BytesIO(json.dumps(sp_plus_rankings).encode()),
    Bucket="college-football",
    Key="data/espn/sp_rankings/2024_week_1.json"
)
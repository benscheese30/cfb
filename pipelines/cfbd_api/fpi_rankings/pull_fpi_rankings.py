from utils import cfbd
from utils import aws
import json
from io import BytesIO
from datetime import datetime

fpi_rankings = cfbd.get_data(
    endpoint="/ratings/fpi",
    params={"year": 2024}
)

open("fpi_rankings.json", "w").write(json.dumps(fpi_rankings))

# upload to s3
s3 = aws.aws_client(
    aws.aws_config(service="s3", localstack=True)
)

s3.upload_fileobj(
    Fileobj=BytesIO(json.dumps(fpi_rankings).encode()),
    Bucket="college-football",
    Key="data/espn/fpi_rankings/2024_week_1.json"
)

# TODO: make this ouput dynamic based on the week using the /calendar endpoint
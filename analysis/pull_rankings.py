from concurrent.futures import ThreadPoolExecutor
from utils import aws

def download_file(wk, key = None, file_path = None):
    """
    Downloads a specific week's SP rankings JSON file from an S3 bucket.

    This function retrieves the rankings data for a given week and saves it to a local file. The file is stored in the specified directory with a naming convention that includes the week number.

    Args:
        wk: The week number for which the rankings file is to be downloaded.

    Returns:
        None
    """
    s3.download_file(
        Bucket="college-football",
        Key=f"{key}/2024_week_{wk}.json",
        Filename=f"{file_path}/week_{wk}.json"
    )

s3 = aws.aws_client(
    aws.aws_config(service="s3", localstack=True)
)

bucket = "college-football"
sp_plus_folder = "data/espn/sp_rankings"
fpi_folder = "data/espn/fpi_rankings"

sp_files = s3.list_objects_v2(
    Bucket=bucket, Prefix=sp_plus_folder
)

fpi_files = s3.list_objects_v2(
    Bucket=bucket, Prefix=fpi_folder
)

sp_wks = len(sp_files["Contents"])
fpi_wks = len(fpi_files["Contents"])

# pull sp+ rankings
# pull sp+ rankings
with ThreadPoolExecutor() as executor:
    executor.map(lambda wk: download_file(wk, key=sp_plus_folder, file_path="analysis/rankings/sp_plus"), range(1, sp_wks + 1))
    executor.map(lambda wk: download_file(wk, key=fpi_folder, file_path="analysis/rankings/fpi"), range(1, fpi_wks + 1))


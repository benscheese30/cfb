from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import boto3
from contextlib import contextmanager
import os

# connect to localstack s3
s3_config = {
    'service_name': 's3',
    'aws_access_key_id': os.getenv("LOCALSTACK_ACCESS_KEY"),
    'aws_secret_access_key': os.getenv("LOCALSTACK_SECRET_KEY"),
    'endpoint_url': os.getenv("LOCALSTACK_ENDPOINT")
}

s3 = boto3.client(**s3_config)

# download backfill_60_in_60.json from s3
s3.download_file(
    Bucket="college-football",
    Key="data/web_scraping/ksl/60_in_60_backfill.json",
    Filename="resources/backfill_60_in_60.json"
)

with open("resources/backfill_60_in_60.json", "r") as f:
    backfill = json.load(f)

player_data = [row for row in backfill if row["year"] in [2019, 2021]]

urls = {
    2022: "https://kslsports.com/487728/hans-scotty-60-in-60-list/",
    2023: "https://kslsports.com/502045/60-in-60-best-college-football-players-in-utah/",
    2024: "https://kslsports.com/518377/hans-scottys-2024-60-in-60-list/"
}


@contextmanager
def get_webdriver():
    driver = webdriver.Chrome()
    try:
        yield driver
    finally:
        driver.quit()


def process_team_name(team_name):
    if team_name == "Weber":
        return "Weber State"
    elif team_name == "USU":
        return "Utah State"
    return team_name.split(",")[0]


def process_player_name(p, year):
    team_name = process_team_name(p.split("(")[1].split(")")[0].strip())
    player_name = p.split(".")[1].split("(")[0].strip()
    if player_name == "Cam Rising":
        player_name = "Cameron Rising"
    return {
        "name": player_name,
        "team": team_name,
        "rank": p.split(".")[0].strip().split(" ")[-1],
        "year": year
    }

with get_webdriver() as driver:
    for year, url in urls.items():
        driver.get(url)
        story_body_element = driver.find_element(By.CLASS_NAME, "story_body")
        paragraph_elements = story_body_element.find_elements(By.TAG_NAME, "p")

        player_names = [
            p.text for p in paragraph_elements
            if any(team in p.text for team in ["BYU", "Utah", "USU", "Weber", "SUU"]) and any(str(i) in p.text for i in range(1, 61))
        ]

        player_names = [p for p in player_names if len(p) < 50]

        for p in player_names:
            player_data.append(process_player_name(p, year))

# write player_list to json file
with open("python/60_in_60/60_in_60_list.json", "w") as f:
    json.dump(player_data, f, indent=4)

# upload 60_in_60_list.json to s3
s3.upload_file(
    Filename="python/60_in_60/60_in_60_list.json",
    Bucket="college-football",
    Key="data/web_scraping/ksl/60_in_60_list.json"
)

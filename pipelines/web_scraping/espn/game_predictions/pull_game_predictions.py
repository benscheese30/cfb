from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract.web_scraping import get_webdriver
from utils import cfbd, aws
from io import BytesIO
import json

# getting a list of game ids for the season
games = cfbd.get_data(
    endpoint="/games",
    params={
        "year": 2024,
        "division": "fbs",
        "team": "Utah"
    }
)

# saving as a set to avoid duplicates
game_ids = (game["id"] for game in games)
game_ids = list(game_ids)

for index, game_id in enumerate(game_ids):
    if index < 10:
        print(f"Game ID: {game_id}")

# TODO: make this loop more scalable by adding a retry or a dynamic list to retry on
fpi_game_predictions = []
retry_list = []
for index, game_id in enumerate(retry_list):
    print(index + 1)
    try:
        with get_webdriver() as driver:
            driver.get(f"https://www.espn.com/college-football/game/_/gameId/{game_id}")

            wait = WebDriverWait(driver, 15)
            game_prediction = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "matchupPredictor"))
            )

            preds = game_prediction.text.split('\n')

            fpi_game_predictions.append({
                "game_id": game_id,
                "home_team": preds[2].float(),
                "away_team": preds[0].float(),
            })
    except Exception as e:
        retry_list.append(game_id)


s3 = aws.aws_client(
    aws.aws_config(service="s3", localstack=True)
)

s3.upload_fileobj(
    Fileobj=BytesIO(json.dumps(fpi_game_predictions).encode()),
    Bucket="college-football",
    Key="data/espn/fpi_game_predictions/2024_week_2.json"
)



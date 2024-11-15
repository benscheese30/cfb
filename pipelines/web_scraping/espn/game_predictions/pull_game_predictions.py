from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract.web_scraping import get_webdriver
from utils import cfbd, aws
from io import BytesIO
import json

# get the current week
year = 2024
game_week = cfbd.get_week(year)

# getting a list of game ids for the season
games = cfbd.get_data(
    endpoint="/games",
    params={
        "year": 2024,
        "division": "fbs"
    }
)

games_dict = {}
for g in games:
    week = g["week"]
    game_id = g["id"]

    if week >= game_week and g['away_points'] is None:
        if week in games_dict:
            games_dict[week].append(game_id)
        else:
            games_dict[week] = [game_id]


fpi_game_predictions = {} # Initialize retry_list with all game_ids
for w, game_ids in games_dict.items():
    print(f"Processing Week: {w}")
    retry_list = game_ids.copy()

    while retry_list:
        game_id = retry_list.pop(0)  # Get the first game_id from retry_list

        try:
            with get_webdriver() as driver:
                driver.get(f"https://www.espn.com/college-football/game/_/gameId/{game_id}")

                wait = WebDriverWait(driver, 15)
                game_prediction = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "matchupPredictor"))
                )

                preds = game_prediction.text.split('\n')

                fpi_game_predictions[game_id] = [float(preds[2]), float(preds[0])]
        except Exception as e:
            print(f"Error processing Game ID: {game_id}")
            retry_list.append(game_id)  # Add the game_id back to retry_list for retrying

print("All game_ids processed successfully.")

s3 = aws.aws_client(
    aws.aws_config(service="s3", localstack=True)
)

s3.upload_fileobj(
    Fileobj=BytesIO(json.dumps(fpi_game_predictions).encode()),
    Bucket="college-football",
    Key=f"data/espn/fpi_game_predictions/{year}_week_{game_week}.json"
)


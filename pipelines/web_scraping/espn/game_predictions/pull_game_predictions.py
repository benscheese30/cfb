from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract.web_scraping import get_webdriver


with get_webdriver() as driver:
    driver.get("https://www.espn.com/college-football/game/_/gameId/401636618/baylor-utah")

    wait = WebDriverWait(driver, 10)
    game_prediction = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "matchupPredictor"))
    )
    print(game_prediction.text)

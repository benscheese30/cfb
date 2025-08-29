from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract.web_scraping import get_webdriver
from utils import aws
from io import BytesIO
import json
from datetime import datetime

def extract_luck_rankings(date_str="2025-01-21"):
    """
    Extract luck rankings from TeamRankings.com
    
    Args:
        date_str: Date in YYYY-MM-DD format for the rankings
    """
    url = f"https://www.teamrankings.com/college-football/ranking/luck-by-other?date={date_str}"
    
    rankings = []
    
    with get_webdriver() as driver:
        driver.get(url)
        
        # Wait for the table to load
        wait = WebDriverWait(driver, 10)
        table = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.tr-table"))
        )
        
        # Extract table headers
        header_row = table.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr")
        headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, "th")]
        
        # Extract table body rows
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= len(headers):
                row_data = {}
                for i, cell in enumerate(cells[:len(headers)]):
                    # Handle team name links
                    if i == 1:  # Assuming team name is in second column
                        link = cell.find_element(By.TAG_NAME, "a") if cell.find_elements(By.TAG_NAME, "a") else None
                        row_data[headers[i]] = link.text.strip() if link else cell.text.strip()
                    else:
                        row_data[headers[i]] = cell.text.strip()
                
                # Clean up the data
                if row_data.get("Rank"):
                    try:
                        row_data["Rank"] = int(row_data["Rank"])
                    except ValueError:
                        pass
                
                if row_data.get("Luck"):
                    try:
                        row_data["Luck"] = float(row_data["Luck"])
                    except ValueError:
                        pass
                
                rankings.append(row_data)
    
    return {
        "date": date_str,
        "source": "teamrankings.com",
        "ranking_type": "luck",
        "extracted_at": datetime.now().isoformat(),
        "rankings": rankings
    }

if __name__ == "__main__":
    # Extract current rankings
    luck_data = extract_luck_rankings()
    
    # Save locally
    date_str = luck_data["date"].replace("-", "_")
    local_path = f"data/luck_rankings/teamrankings_{date_str}.json"
    
    import os
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    with open(local_path, "w", encoding="utf-8") as f:
        json.dump(luck_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved luck rankings to {local_path}")
    
    # Optional: Upload to S3 if you want
    # s3 = aws.aws_client(aws.aws_config(service="s3", localstack=True))
    # s3.upload_fileobj(
    #     Fileobj=BytesIO(json.dumps(luck_data, indent=2).encode("utf-8")),
    #     Bucket="college-football",
    #     Key=f"data/web_scraping/teamrankings/luck_rankings_{date_str}.json"
    # )
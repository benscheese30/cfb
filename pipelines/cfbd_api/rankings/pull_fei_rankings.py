from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract.web_scraping import get_webdriver
from utils import aws
from io import BytesIO
import json
from datetime import datetime
import time

def extract_pfei_rankings(year=2025):
    """
    Extract FEI rankings from bcftoys.com
    
    Args:
        year: Year for the rankings (default 2025)
    """
    url = f"https://bcftoys.com/{year}-pfei"
    
    rankings = []
    
    with get_webdriver() as driver:
        driver.get(url)
        
        # Wait a moment for the page to fully load
        time.sleep(3)
        
        # Wait for the table to load - FEI rankings are typically in a table
        wait = WebDriverWait(driver, 15)
        
        # Try different possible table selectors
        table_selectors = [
            "table.table",
            "table.ranking-table", 
            "table.fei-table",
            "table",
            ".table-responsive table",
            "#rankings-table"
        ]
        
        table = None
        for selector in table_selectors:
            try:
                table = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"Found table with selector: {selector}")
                break
            except:
                continue
        
        if not table:
            # If no table found, try to find any structured data
            print("No table found, looking for alternative structure...")
            # You might need to inspect the actual page structure
            raise Exception("Could not locate FEI rankings table")
        
        # Extract table headers
        try:
            header_row = table.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr")
            headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, "th")]
        except:
            # If no thead, try first row of tbody
            rows = table.find_elements(By.TAG_NAME, "tr")
            if rows:
                headers = [th.text.strip() for th in rows[0].find_elements(By.TAG_NAME, "th")]
                if not headers:
                    headers = [td.text.strip() for td in rows[0].find_elements(By.TAG_NAME, "td")]
            else:
                headers = ["Rank", "Team", "FEI", "Offense", "Defense", "Special Teams"]  # Default headers
        
        print(f"Headers found: {headers}")
        
        # Extract table body rows
        try:
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
        except:
            # If no tbody, get all rows except first (header)
            all_rows = table.find_elements(By.TAG_NAME, "tr")
            rows = all_rows[1:] if len(all_rows) > 1 else all_rows
        
        print(f"Found {len(rows)} data rows")
        
        for i, row in enumerate(rows):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:  # At least rank and team
                row_data = {}
                for j, cell in enumerate(cells):
                    header_name = headers[j] if j < len(headers) else f"Column_{j+1}"
                    
                    # Handle team name links
                    if "team" in header_name.lower() or j == 1:
                        link = cell.find_element(By.TAG_NAME, "a") if cell.find_elements(By.TAG_NAME, "a") else None
                        row_data[header_name] = link.text.strip() if link else cell.text.strip()
                    else:
                        row_data[header_name] = cell.text.strip()
                
                # Clean up the data
                for key, value in row_data.items():
                    if "rank" in key.lower() and value.isdigit():
                        row_data[key] = int(value)
                    elif key.lower() in ["fei", "offense", "defense", "special teams", "rating"]:
                        try:
                            # Remove any non-numeric characters except decimal point and minus
                            clean_value = ''.join(c for c in value if c.isdigit() or c in '.-')
                            if clean_value and clean_value not in ['-', '.']:
                                row_data[key] = float(clean_value)
                        except ValueError:
                            pass  # Keep as string if can't convert
                
                if row_data:  # Only add if we got some data
                    rankings.append(row_data)
        
        print(f"Extracted {len(rankings)} rankings")
    
    return {
        "year": year,
        "source": "bcftoys.com",
        "ranking_type": "fei",
        "extracted_at": datetime.now().isoformat(),
        "url": url,
        "rankings": rankings
    }

if __name__ == "__main__":
    # Extract current FEI rankings
    year = 2025
    fei_data = extract_fei_rankings(year)
    
    # Save locally
    local_path = f"data/fei_rankings/{year}_week_current.json"
    
    import os
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    with open(local_path, "w", encoding="utf-8") as f:
        json.dump(fei_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved FEI rankings to {local_path}")
    print(f"Total teams ranked: {len(fei_data['rankings'])}")
    
    # Show sample of first few rankings
    if fei_data['rankings']:
        print("\nSample rankings:")
        for i, team in enumerate(fei_data['rankings'][:5]):
            print(f"{i+1}. {team}")
    
    # Optional: Upload to S3 if you want
    # s3 = aws.aws_client(aws.aws_config(service="s3", localstack=True))
    # s3.upload_fileobj(
    #     Fileobj=BytesIO(json.dumps(fei_data, indent=2).encode("utf-8")),
    #     Bucket="college-football",
    #     Key=f"data/web_scraping/bcftoys/fei_rankings_{year}.json"
    # )
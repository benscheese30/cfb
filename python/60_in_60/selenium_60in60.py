from selenium import webdriver
from selenium.webdriver.common.by import By
import py.dbs as dbs

urls = {
    2022: "https://kslsports.com/487728/hans-scotty-60-in-60-list/",
    2023: "https://kslsports.com/502045/60-in-60-best-college-football-players-in-utah/"
}

def pull_60in60_list(year, url):
    # setting up driver
    driver = webdriver.Chrome()

    # connecting to url
    driver.get(url)

    # getting list of players
    story_body_element = driver.find_element(By.CLASS_NAME, "story_body")
    paragraph_elements = story_body_element.find_elements(By.TAG_NAME, "p")

    player_names = [
        p.text
        for p in paragraph_elements
        if (
            "BYU" in p.text
            or "Utah" in p.text
            or "USU" in p.text
            or "Weber" in p.text
            or "SUU" in p.text
        )
        and any(str(i) in p.text for i in range(1, 61))
    ]
    # closing connection to url
    driver.close()

    # excluding elements from player_names that have more than 50 characters
    player_names = [p for p in player_names if len(p) < 50]

    # preparing data for database
    player_list = []
    for p in player_names:
     # setting team name to "Weber State" if team name is "Weber"
     if p.split("(")[1].split(")")[0].strip() == "Weber":
         team_name = "Weber State"
     elif p.split("(")[1].split(")")[0].strip() == "USU":
         team_name = "Utah State"
     else:
         team_name = p.split("(")[1].split(")")[0].strip()

     player_list.append({
         "name": p.split(".")[1].split("(")[0].strip(),
         "team": team_name,
         "rank": p.split(".")[0].strip().split(" ")[-1],
         "year": year
     })

    # inserting data into postgres
    dbs.data_insert("cfb_60in60", player_list)

# only run if not already created
# creating table in postgres
sql = """
 create table cfb.cfb_60in60 (
     id serial primary key,
     name varchar(100),
     team varchar(100),
     rank integer,
     year integer
 )
"""
dbs.postgres_create_table(sql)

# get player list for each year
for year, url in urls.items():
    pull_60in60_list(year, url)

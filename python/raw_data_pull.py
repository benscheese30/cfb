import requests
import os
import json

# read in local json file
with open("resources/cfbd_api_structure.json", "r") as f:
    json = json.load(f)

# extract endpoint names and parameters
paths = json["paths"]
endpoint_dict ={}

# loop through endpoints
for k in paths:
    print(k)
    path_base = paths[k]["get"]
    # get parameters
    if "parameters" in path_base:
        params = {}
        # get parameter names and data types
        for p in path_base["parameters"]:
            params[p["name"]] = {
                "type": p["type"],
                "required": p["required"]
            }
    # add to dictionary
    endpoint_dict[k] = {
        "params": params
    }

url = "https://api.collegefootballdata.com"
headers = {"Authorization": f"Bearer {os.environ['CFBD_API_KEY']}"}

endpoint = "/games"

# create parameters based on /games endpoint
params = {
    "year": 2019
}

games = requests.get(
    url=f'{url}{endpoint}',
    headers=headers,
    params=params
)

games_json = games.json()


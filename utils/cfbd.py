import cfbd
import os
import requests
import logging
import json
import datetime

# setup logging message with timestamp
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

def signin():
    config = cfbd.Configuration()
    config.api_key["Authorization"] = os.environ["CFBD_API_KEY"]
    config.api_key_prefix['Authorization'] = 'Bearer'
    return cfbd.ApiClient(config)

def get_data(endpoint, params=None):
    url = "https://api.collegefootballdata.com"
    headers = {"Authorization": f"Bearer {os.environ['CFBD_API_KEY']}"}

    if params is None:
        params = {}

    data = requests.get(
        url=f'{url}{endpoint}',
        headers=headers,
        params=params
    )

    if data.status_code == 200:
        return data.json()
    logging.error(f"Error {data.status_code} in {endpoint} with params {params}. Reason: {data.reason}")
    return None

def get_params(endpoint, js="resources/cfbd_endpoint_details.json"):
    with open(js, "r") as f:
        endpoint_structure = json.load(f)

    params = endpoint_structure[endpoint]["params"]

    param_structure = {}
    param_dict = {}
    for p in params:
        param_structure[p] = {
            "type": params[p]["type"],
            "required": params[p]["required"]
        }
        param_dict[p] = None

    print(param_structure)
    return param_dict


def get_week(year):
    global week
    calendar = get_data(
        endpoint="/calendar",
        params={"year": year}
    )

    current_time = datetime.datetime.now().isoformat()

    for c in calendar:
        if c["firstGameStart"] < current_time < c["lastGameStart"]:
            week = c["week"]
            break

    return week


import cfbd
import os
import requests
import logging
import json
import time

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

def get_data(endpoint, params):
    url = "https://api.collegefootballdata.com"
    headers = {"Authorization": f"Bearer {os.environ['CFBD_API_KEY']}"}

    data = requests.get(
        url=f'{url}{endpoint}',
        headers=headers,
        params=params
    )

    if data.status_code == 200:
        return data.json()
    else:
        logging.error(f"Error {data.status_code} in {endpoint} with params {params}. Reason: {data.reason}")
        return None

    time.sleep(5)

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


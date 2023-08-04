import cfbd
import os

def cfbd_signin():
    config = cfbd.Configuration()
    config.api_key["Authorization"] = os.environ["CFBD_API_KEY"]
    config.api_key_prefix['Authorization'] = 'Bearer'
    return cfbd.ApiClient(config)

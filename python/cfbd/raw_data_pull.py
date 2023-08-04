import py.cfbd as cfbd

endpoint = "/games"

cfbd.get_params(endpoint=endpoint)

params = {'year': 2015}

games_raw = cfbd.get_data(endpoint, params)


from py.dbs import postgres_connect_async
import py.cfbd as cfbd

endpoint = "/games"

# create parameters based on /games endpoint
cfbd.get_params(endpoint=endpoint)

params = {'year': 2015}

games = cfbd.get_data(endpoint, params)

sql = """
    create table if not exists games (
        id serial primary key,
        game_id integer
    )
"""

with postgres_connect_async() as cur:
    cur.execute(sql)


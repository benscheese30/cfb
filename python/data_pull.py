import cfbd
from py.cfb import cfbd_signin

# signing into api
api = cfbd_signin()



games_api = cfbd.GamesApi(api)
games = games_api.get_games(
    year = 1913
)


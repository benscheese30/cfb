import py.dbs as dbs
import py.cfbd as cfbd
import datetime

current_year = datetime.datetime.now().year
year = 2003

# getting games endpoint requirements
endpoint = "/games"
cfbd.get_params(endpoint=endpoint)

# create table statement
games_sql = """
    create table if not exists cfb.games (  
        id integer primary key,
        season integer,
        week integer,
        season_type varchar(20),
        start_date date,
        start_time_tbd boolean,
        completed boolean,
        neutral_site boolean,
        conference_game boolean,
        attendance integer,
        venue_id integer,
        venue varchar(100),
        home_id integer,
        home_team varchar(100),
        home_conference varchar(20),
        home_division varchar(20),
        home_points integer,
        home_line_scores integer[],
        home_post_win_prob float,
        home_pregame_elo float,
        home_postgame_elo float,
        away_id integer,
        away_team varchar(100),
        away_conference varchar(20),
        away_division varchar(20),
        away_points integer,
        away_line_scores integer[],
        away_post_win_prob float,
        away_pregame_elo float,
        away_postgame_elo float,
        excitement_index float,
        highlights integer[],
        notes varchar(1000)
)        
"""

# create a table in postgres
dbs.postgres_create_table(games_sql)

# insert data into postgres
for year in range(2003, current_year + 1):
    print(year)
    games_params = {"year": year}
    df = cfbd.get_data(endpoint, games_params)
    if df is not None:
        dbs.data_insert("games", df)

for row in df:
    print(row["id"])
    if df is not None:
        dbs.data_insert("games", df)
# build code for soccerstats.us

### transform text data to structured data

The build runs locally (macOS); production (bert) only serves the result.
The full flow is: data repos -> mongo (this repo) -> postgres (s2 repo) -> ship to bert.

### how to build the database

    # mongo (macOS)
    brew tap mongodb/brew && brew install mongodb-community
    brew services start mongodb-community

    # clone this repo, metadata, parse, and the data repos as siblings in ~/soccer/
    # (usd1_data, us_minor_data, world_data, ... see the list in make/load.py)

    # python environment
    cd ~/soccer/build
    uv venv --python 3.12
    uv pip install -p .venv/bin/python -r requirements3.txt

    # your hostname must be in the roots dict of settings.py (and metadata/settings.py)

    # build: load -> normalize -> lift -> transform -> merge -> generate -> denormalize
    PYTHONPATH=~/soccer:~/soccer/build .venv/bin/python make/

#### how to run the tests

    cd ~/soccer/build
    .venv/bin/python -m pytest

No mongo needed: the stages that talk to it are given an in-memory stand-in
(`tests/fakedb.py`). `pytest.ini` puts `make/` on the path so tests import the
stage modules flat, the same way the build does.

Tests marked `xfail` are known bugs, pinned so they announce themselves when
fixed rather than being silently forgotten. See ROADMAP.md.

Then load postgres and ship (see the s2 repo):

    cd ../s2
    ./build.sh     # mongo -> postgres
    ./upload.sh    # pg_dump -> bert


#### What is going on here?

The creating and normalizing a database consists of a series of steps.

The data is loaded first, then names and structures are regularized and transformed.

Then, data is merged, and finally additional data is generated.

Finally, data is denormalized (time and location-specific names) and (optionally) checked for accuracy.


#### Data repositories


* usd1_data
* us_minor_data
* nwsl_data
* us_cup_data
* asl2_data
* ncaa_data

* world_data
* afc_data
* caf_data
* concacaf_data
* conmebol_data
* ofc_data
* uefa_data

* international_data
* usmnt_data
* indoor_data
* friendly_data
* isl_data
* ltrack_data

* sidekicks_data
* spalding_data
* bethlehem_data

* metadata
* soccerdata


#### load

load all data from text files

#### normalize

convert data into canonical forms and normalize formatting differences

* player names: Damarcus Beasley -> DaMarcus Beasley
* team names: Dallas Burn -> FC Dallas
* place names: New York City -> New York, NY

#### lift

* convert abbreviated player names using roster data into full names

    Lift('Henry', ['Thierry Henry', 'Patrick Vieira']) -> Thierry Henry

#### transform

* some random stuff

#### merge

* merge data from various sources into a single representation

   Merge([{'date': datetime.datetime(1996, 7, 1), 'team1': 'San Jose Earthquakes', 'team1_score': 1, 'team2': 'DC United', 'team2_score': 0 }, 
       {'date': datetime.datetime(1996, 7, 1), 'team1': 'San Jose Earthquakes', 'team1_score': None, 'team2': 'DC United', 'team2_score': None, 'location': 'San Jose, CA' }] -> 
       {'date': datetime.datetime(1996, 7, 1), 'team1': 'San Jose Earthquakes', 'team1_score': 1, 'team2': 'DC United', 'team2_score': 0, 'location': 'San Jose, CA' })


#### generate

* generate secondary data from known data

* Generated data includes:
  1. various stats - GameStat, standard Stat, TeamStat, CompetitionStat, CareerStat, etc.
  2. various standings - 

#### denormalize

* add time-specific data to canonical representations
* give time-specific team names, player names



#### build steps

* check aliases for loops
* clear all database data
* load metadata (place, source, competition, team, player data, mappings (team->name,team->stadium,competition->name))
* load game data (game results, stats, rosters, standings, awards)
* load extra data (drafts, transactions, salaries, news [disabled])

* normalize metadata (seasons, stadiums, teams, player data, mappings)
* normalize game data (games, goals, lineups, game stats, stats, game stats, rosters, stats, standings
* normalize extra data (drafts, transactions, positions, awards)

* lift player names (use roster data to convert abbreviated names into full names)
* transform team names for given competitions - mostly Youth competitions

* merge data (metadata, game data, extra data)

* generate game data - infer location / home team using metadata
* generate game stats
* generate competition standings, competition statistics



Check data (standing validity, game fields)





### Outstanding tasks

See [ROADMAP.md](ROADMAP.md).


# build code for soccerstats.us

### transform text data to structured data

For how to set up a new server see new.md

### how to build the database yourself on Ubuntu 16.04

This is how to build the database

    # add mongo sources
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list

    # update apt
    sudo apt-get update
    sudo apt-get upgrade

    # Install dependencies
    sudo apt-get install git-core mongodb-org emacs python3-setuptools
    sudo easy_install3 pip

    # A little more mongo.
    # This isn't really working right now. Right? 
    Add /etc/systemd/system/mongodb.service from https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04
    
    sudo systemctl start mongodb
    sudo systemctl status mongodb # SHOULD SAY WHAT?

    # Postgresql
    # (this could be done later, but probably best now.)
    * sudo apt-get install postgresql
    * sudo -u postgres -i
    * createuser -d soccerstats

    # NEED TO KNOW POSTGRES PASSWORD HERE
    * sudo emacs /etc/postgresql/9.5/main/pg_hba.conf
    * Change:
    # local   all             all peer
    # local   all             all trust
    # (I know this is terribly dangerous...)

    # Add to pythonpath

    emacs .bashrc 
    # add to .bashrc
    # export PYTHONPATH=$PYTHONPATH:/home/chris/bin:/home/chris/www:/home/chris/repos:/home/chris/soccer
    source .bashrc

    # Clone repositories

    mkdir soccer/
    cd soccer/
    git clone https://github.com/SoccerstatsUS/parse.git
    git clone https://github.com/SoccerstatsUS/metadata.git
    git clone https://github.com/SoccerstatsUS/build.git
    git clone https://github.com/SoccerstatsUS/usd1_data.git
    git clone https://github.com/SoccerStatsUS/soccerdata.git

    # git clone https://github.com/SoccerstatsUS/nwsl_data.git

    # Install

    cd build/
    sudo pip3 install -r requirements3.txt

    sudo pip3 install django psycopg2

    python3 make/
    # Fix this problem:  ROOT_DIR = roots[host] KeyError: 'ubuntu'
    # Also fix the problem that this is duplicated in metadata.


The end. With luck you should have a functioning install now. 


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





### Outstanding tasks.

* Need to define parser, data formats better.

* Outstanding data gaps.

* 2010 World Cup
* MLS 2012 season data.
* Gold Cup champions; non-us results/goals/lineups
* United States game location information; scattered unknown opponent lineups.
* Open Cup information is spotty; watch out for release of new Open Cup data.
* NASL lineup and goal info.
* ASL game locations/refs; lineups + goals
* CCL lineup/goal info is very weak.
* SuperLiga non-US goals/lineups
* CCC information is quite weak.
* Copa America everything - available at RSSSF
* USL-1, USL-2 2001-2003 lineups/goals; 2008-2009 lineups/goals
* ISL data incomplete.
* PDL everything.
* Everything APSL pre-1993; 1994-1995 is spotty.
* ASL2 entirely terrible.

* Fix Brooklyn Hakoah name mapping (other ASL name mappings.)
* Draw graph of seasons.

0. Fix giant ASL team name bug issue - easy but producing a lot of errors.
1. Convert bios to yaml.
2. Consider moving aliases into data.

## Error detection


Data notes:
I moved Dallas - Apollon game on 7/8/1971 forward a day for convenience. Please look up the actual date.; Likewise the Hapoel gameo on 6/30/1970, and Veracruz in 7/11/1973 (Dallas/Atlanta)b. and 6/28/1970 Hapoel /St. Louis / Washington




import socket

host = socket.gethostname()

roots = {
    'agni.local': '/Users/chris/soccer',
    'agni': '/Users/chris/soccer',
    'bert': '/home/chris/www',
    }

ROOT_DIR = roots[host]



# What items are shown on the dashboard
STAT_TABLES = [
    'games', 
    'goals', 
    'fouls', 
    'lineups', 
    'stats', 
    'gstats',
    'standings', 

    'rosters',
    'gen_rosters',
    'awards',
    'bios',
    ]


# Sources are listed in terms of reliability; Order affects priority when merging games.
# need to reduce this dramatically.
SOURCES = [

    'world_i',
    'fifa',

    'concacaf_i',
    'conmebol_i',
    'oceania_i',
    'usa',

    'england',

    'world',
    'concacaf',
    'conmebol',
    'oceania',

    #'uncaf',
    #'cfu',

    'alpf',
    'asl',
    'nasl',
    'mls',
    'mls2',
    'mls3',


    #'nafbl',
    'asl2',
    'us_minor',

    #'us_d2',
    #'us_d3',
    #'us_d4',
    'us_lower',
    'ltrack',

    'us_cups',
    'us_friendly',

    'ncaa',
    'state',
    'city',

    'women',

    'canada',
    'mexico',

    'colombia',
    'uruguay',
    'chile',
    'argentina',
    'brazil',

    'afc',

    #'china',
    #'japan',
    #'korea',
    #'australia',

    'uefa',
    'epl',



    'mediotiempo',

    'indoor',
        ]



SINGLE_SOURCES = [
    'competitions',
    'seasons',
    'teams', 
    'stadiums', 
    'cities',
    'states',
    'countries',

    'news',
    'sources',

    'awards', 
    'drafts',
    'picks',

    'salaries', # player, date -> integer
    'positions', # player, date -> team
    'state_populations', # state -> integer
    'name_maps', # team, date -> string
    'stadium_maps', # team, date -> stadium
    'competition_maps', # competition, date -> string

    # 'prerosters', # huh?#
    ]

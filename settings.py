

import socket

host = socket.gethostname()

roots = {
    'agni.local': '/Users/chris/soccer',
    'agni': '/Users/chris/soccer',
    'Christophers-MacBook-Air.local': '/Users/chirs/soccer',
    'Christophers-MacBook-Air': '/Users/chirs/soccer',
    'bert': '/home/chris/www',
    'oscar': '/home/chris/soccer',
    'li1014-58': '/home/chris/soccer',
    'jason': '/home/chris/soccer',
    'ubuntu': '/home/chris/soccer', # Need to fix.
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
    'transactions',

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

    # espn is a second look at leagues that already have their own source here,
    # so it sits last: merge_games keeps the first source to record a game and
    # lets later ones fill only the fields it left empty. espn never overwrites
    # a league's own record of its own game, it just fills the holes.
    'espn',
        ]



SINGLE_SOURCES = [
    'competitions',
    'seasons',
    'teams', 
    'stadiums', 
    'cities',
    'city_coordinates',
    'states',
    'countries',

    'news',
    'sources',
    'blurbs',

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

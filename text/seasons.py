

import os

# FIXME
SEASON_DIR = '/home/chris/www/soccerdata/data/seasons'

SEASONS = [

    #'asl',
    'nasl',
    'mls',

    'mexico',

    'australia',
    'japan',
    'china',

    'argentina',
    'uruguay',
    'chile',
    ]

def load_seasons():
    l = []
    for fn in SEASONS:
        p = os.path.join(SEASON_DIR, fn)
        l.extend(process_file(p))

    return l


def process_file(p):
    f = open(p)


    seasons = []
    competition = None
    order = 0

    for line in f:
        line = line.strip()

        if line.startswith('Competition:'):
            competition = line.split('Competition:')[1]
            order = 0

        else:
            if line:
                seasons.append({
                        'competition': competition,
                        'season': line,
                        'order': order,
                        })
            order += 1

    return seasons
            
            

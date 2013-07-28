# For parsing ratings from Philip Beineke.

import csv

ratings_path = '/home/chris/www/soccerdata/data/analysis/ratings1.0.csv'


def get_ratings():
    f = open(ratings_path)
    r = csv.reader(f, delimiter=',', quotechar='"')
    ratings = [x for x in r][1:]
    
    l = []
    for e in ratings:
        l.append({
                'slug': e[2],
                'rating': e[4],
                'system': 'beineke/edgemon +-',
                })
        
    return l


if __name__ == "__main__":
    print(get_ratings())

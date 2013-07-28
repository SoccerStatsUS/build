import os
import yaml

DIR = '/home/chris/www/soccerdata/data/'

if not os.path.exists(DIR):
    DIR = "/Users/chrisedgemon/www/soccerdata/data/"




def load_teams():
    p = os.path.join(DIR, 'teams.yaml')
    return yaml.load(open(p))

if __name__ == "__main__":
    print(load_teams())

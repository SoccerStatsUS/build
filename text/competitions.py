
import os

# FIXME
COMPETITIONS = '/home/chris/www/soccerdata/data/competitions'

def load_competitions():

    def helper(line):
        fields = [e.strip() for e in line.split(';')]
        name, abbreviation, code, international, ctype, level, scope, area = fields

        ib =  (international.strip() == 'international')

        if level == '':
            level = None
        else:
            level = int(level)

        return {
            'name': name,
            'abbreviation': abbreviation,
            'code': code,
            'international': ib,
            'ctype': ctype,
            'level': level,
            'scope': scope,
            'area': area
            }
    

    p = os.path.join(COMPETITIONS)
    f = open(p)
    return [helper(line.strip()) for line in f if line.strip() and not line.startswith('*')]


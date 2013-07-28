# Process Ltrack files from Scott Leach.

import datetime
import os

from soccerdata.data.alias import get_team
from smid.text.standings import process_excel_standings


DIR = '/home/chris/www/soccerdata/data/ltrack'


def format_name(s):
    # Reverse a name from Donovan, Landon to Landon Donovan.
    fields = [e.strip() for e in s.split(",", 1)]

    if len(fields) == 1:
        ns = fields[0]
    elif len(fields) == 2:
        ns = "%s %s" % (fields[1], fields[0])
    return ns


def make_team_to_competition_dict():
    # Create a dict mapping a team name and season to a competition.

    l = []
    for e in 'mls', 'apsl', 'ussf2', 'nasl2':
        l.extend(process_excel_standings('domestic/country/usa/%s' % e))

    for e in '12', 'pdl', 'premier', 'pro', 'select', 'usisl', 'usl_pro':
        l.extend(process_excel_standings('domestic/country/usa/usl/%s' % e))

    

    d = {}
    for e in l:
        key = (get_team(e['team']), e['season'])
        if key not in d:
            d[key] = [e['competition']]

            
    return d


TEAM_COMPETITION_DICT = make_team_to_competition_dict()


def teams_for_season(season):
    return [e[0][0] for e in TEAM_COMPETITION_DICT.items() if e[0][1] == season]


def determine_competition(comp, team, season):

    mapping = {
        'CCC': 'CONCACAF Champions\' Cup',
        'IAC': 'Interamerican Cup',
        'GC': 'CONCACAF Giants Cup',
        'FDLY': 'Friendly',
        'MerC': 'Merconorte Cup',
        'CCWC': 'CONCACAF Cup Winners Cup',
        'LMC': 'La Manga Cup',

        'RC': 'Recopa CONCACAF',
        'PCK': 'Peace Cup',
        'CQ': 'Caribbean Qualification',
        #'CQ': 'Concacaf Champions\' Cup',
        'PPC': 'Pan-Pacific Championship',
        'INDC': 'Independence Cup',
        }

    if comp in mapping:
        return mapping[comp]
    

    if comp == 'LGE':
        try:
            competitions = TEAM_COMPETITION_DICT[(team, season)]
        except:
            import pdb; pdb.set_trace()

        if len(competitions) > 1:
            import pdb; pdb.set_trace()
        else:
            return competitions[0]

    import pdb; pdb.set_trace()
    x = 5



def process_lineups_file(fn):
    text = open(fn).read().replace('\r', '').split('\n')
    header = text[0]
    data = text[1:]

    l = []
    
    for line in data:
        s = line.strip()
        if s:
            fields = line.split('\t')

            comp, date_string, home_team, away_team, team, name, rating, on, off, yc1, yc2, rc, yc, time, substituted, time_on, time_off, yc_time = fields

            month, day, year = [int(e) for e in date_string.split("/")]
            d = datetime.datetime(year, month, day)
            season = str(d.year)

            t = get_team(team)

            competition = determine_competition(comp, t, season)


            n = format_name(name)


            l.append({
                    'name': n,
                    'on': int(on),
                    'off': int(off),
                    'team': t,
                    'date': d,
                    'season': season,
                    'competition': competition,
                    })


    return [e for e in l if e['competition'] != 'Major League Soccer']

        

def process_games_file(fn):
    """
    Process a games file.
    """
    text = open(fn).read().replace('\r', '').split('\n')
    header = text[0]
    data = text[1:]

    l = []
    
    for line in data:
        s = line.strip()
        if s:
            fields = line.split('\t')
            
            # 14 fields always
            try:
                date_string, home_team, away_team, home_score, away_score, attendance, competition_type, comp, comments, referee, awarded, _, _, _ = fields
            except:
                import pdb; pdb.set_trace()

            month, day, year = [int(e) for e in date_string.split("/")]
            d = datetime.datetime(year, month, day)

            season = str(d.year)

            team1 = get_team(home_team)
            team2 = get_team(away_team)

            competition = determine_competition(comp, team1, season)

            if attendance.strip():
                attendance = int(attendance.replace(',', ''))
            else:
                attendance = None

            if attendance in (0, 1, 10):
                attendance = None
                

            l.append({
                    'team1': team1,
                    'team2': team2,
                    'team1_score': int(home_score),
                    'team2_score': int(away_score),
                    'home_team': team1,
                    'competition': competition,
                    'season': season,
                    'date': d,
                    'attendance': attendance,
                    'referee': format_name(referee),
                    'sources': ['Scott Leach'],
                    })

    return [e for e in l if e['competition'] != 'Major League Soccer']


def process_goals_file(fn):
    """
    Process a goal file.
    """

    text = open(fn).read().replace('\r', '').split('\n')
    header = text[0]
    data = text[1:]

    l = []

    for line in data:
        s = line.strip()
        if s:
            fields = line.split('\t')

            # 11 fields always
            player, team, _, _, date_string, minute, _, comp, assist1, assist2, _ = fields

            month, day, year = [int(e) for e in date_string.split("/")]

            d = datetime.datetime(year, month, day)
            season = str(d.year)

            if assist1 and assist2:
                assists = [format_name(assist1), format_name(assist2)]
            elif assist1:
                assists = [format_name(assist1)]
            else:
                assists = []

            team = get_team(team)

            competition = determine_competition(comp, team, season)

            l.append({
                    'goal': format_name(player),
                    'minute': int(minute),
                    'team': team,
                    'type': 'normal',
                    'date': d,
                    'assists': assists,
                    'season': season,
                    'competition': competition,
                    })

    return [e for e in l if e['competition'] != 'Major League Soccer']

                    


def process_goals():
    """
    Process all goal data from Leach.
    """
    l = []
    directory = os.path.join(DIR, 'goals')
    for fn in os.listdir(directory):
        p = os.path.join(directory, fn)
        data = process_goals_file(p)
        l.extend(data)
    return l
        



def process_games():
    """
    Process all game data from Leach.
    """
    l = []
    directory = os.path.join(DIR, 'games')
    for fn in os.listdir(directory):
        p = os.path.join(directory, fn)
        data = process_games_file(p)
        l.extend(data)
    return l
     


def process_lineups():
    """
    Process all game data from Leach.
    """
    l = []
    directory = os.path.join(DIR, 'squads')
    for fn in os.listdir(directory):

        p = os.path.join(directory, fn)
        data = process_lineups_file(p)
        l.extend(data)
    return l
        

if __name__ == "__main__":
    print(process_lineups())
    #print(process_games())
    #print(process_goals())
    
    

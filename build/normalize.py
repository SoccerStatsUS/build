import datetime
from settings import SOURCES

from smid.alias import get_team, get_name, get_season, get_competition, get_place, get_stadium, get_city, get_round
from smid.mongo import generic_load, soccer_db, insert_rows, insert_row, soccer_db

from separate import separate_team, separate_name


def make_location_normalizer():
    # What is the proper way to handle locations?
    # Locations are primarily used by game and bio data.
    # Apply place alias.
    # Check if the location is a team (games only, team alias)
    # Check if the location is a stadium (stadium alias)
    # Check if the location is a city (city alias)
    # Check if the location is a state
    # Check if the location is a country
    # Throw an error.
    # Return a dict with appropriate values.
    """
    Detect stadium and split off from place name
    Split off a stadium from a place name, if possible.
    Apply stadium location information if a stadium is found.

    Examples:
    'Pizza Hut Park, Dallas, TX' -> ('Pizza Hut Park', 'Dallas, TX')
    'Pizza Hut Park, Dallas, Texas' -> ('Pizza Hut Park', 'Dallas, TX')
    'Richardson, Texas' -> (None, 'Richardson, Texas')
    """

    stadium_names = set()
    stadium_map = {}

    # Map stadium names to stadium objects; add to set.
    # Need to handle multiple stadiums with same name.
    for stadium in soccer_db.stadiums.find():
        name = stadium['name']
        stadium_names.add(name)
        stadium_map[name] = stadium
    
    def getter(s):

        #if s == 'Estadio Ricardo Saprissa, San Jose, Costa Rica':
        #    import pdb; pdb.set_trace()


        # No commas in stadium names
        # Take something like Home Depot Center, Carson, CA -> 
        # ('Home Depot Center', 'Carson, CA')
        if ',' in s:
            potential_stadium, location_string = s.split(',', 1)
        else:
            potential_stadium, location_string = s, ''

        potential_stadium = get_stadium(potential_stadium)
        location_string = get_city(location_string)

        if potential_stadium in stadium_names:
            sx = stadium_map[potential_stadium]
            name, city = sx['name'], sx['location']

            # Do soft location check here.
            if location_string and (city.strip() != location_string.strip()):
                pass
                """
                try:
                    print("mismatch:\n%s\n%s" % (location_string, city))
                except:
                    print("BIGFAIL %s" % str(location_string))
                    """
        
        else:
            name, city = None, get_city(s)

        return name, city
        
    return getter

location_normalizer = make_location_normalizer()



def calculate_lineup_result(d):
    if d['goals_for'] is None or d['goals_against'] is None:
        return None

    if d['goals_for'] == d['goals_against']:
        return 't'

    if d['goals_for'] > d['goals_against']:
        return 'w'

    else:
        return 'l'
    

def calculate_game_results(d):
    team1_score = d['team1_score']
    team2_score = d['team2_score']
    team1_result = d.get('team1_result')
    team2_result = d.get('team2_result')

    if team1_result and team2_result:
        return team1_result, team2_result

    if team1_score == team2_score == None:
        return '', ''

    if type(team1_score) == int and type(team2_score) == int:
        if team1_score == team2_score:
            return 't', 't'

        elif team1_score > team2_score:
            return 'w', 'l'

        else:
            return 'l', 'w'

    else:
        if team1_result == 'w':
            return 'w', 'l'

        if team1_result == 'l':
            return 'l', 'w'

        if team2_result == 'w':
            return 'l', 'w'

        if team2_result == 'l':
            return 'w', 'l'

    import pdb; pdb.set_trace()
    x = 5


def normalize_season(e):
    #e['competition'] = get_competition(e['competition'])

    e['name'] = get_season(e['name'])
    #e['name']

    return e

def normalize_game_stat(e):
    e['team'] = get_team(e['team'])
    e['team'] = separate_team(e['team'], e)
    e['player'] = get_name(e['player'])
    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])
    
    #if 'Noone' in e['player']:
    #    import pdb; pdb.set_trace()

    return e


# Change all of these to use only a single game.

def normalize_game(e):

    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])

    if e['season'] is None:
        e['season'] = 'Unknown'

    e['round'] = get_round(e.get('round', ''))
    if e.get('group'):
        if e['group'].startswith('Group'):
            e['group'] = e['group'].replace('Group', '').strip()


    e['team1'] = get_team(e['team1'])
    e['team2'] = get_team(e['team2'])

    e['team1'] = separate_team(e['team1'], e)
    e['team2'] = separate_team(e['team2'], e)

    # Make sure we always know the order of teams.
    if e['team1'] > e['team2']:
        e['team1'], e['team2'] = e['team2'], e['team1']
        e['team1_score'], e['team2_score'] = e['team2_score'], e['team1_score']

        if 'team1_result' in e:
            e['team1_result'], e['team2_result'] = e['team2_result'], e['team1_result']


    if e.get('home_team'):
        e['home_team'] = get_team(e['home_team'])
        e['home_team'] = separate_team(e['home_team'], e)


    # This is the wrong behavior...huh?
    if e.get('minutes') == None:
        e['minutes'] = 90

    if e['minutes'] == 'asdet':
        e['minutes'] = 120

    # Assign appropriate results based on score and result data.
    e['team1_result'], e['team2_result'] = calculate_game_results(e)

    #if e['team1'] == 'Chicago Croatian SC':
    #    import pdb; pdb.set_trace()

    # Transforming place names should happen before anything else.
    # Place transfomrations are the most conservative.
    if 'location' in e:
        if e['location']:
            e['location'] = get_place(e['location'])
            # Get stadium data if possible.

            e['stadium'], e['location'] = location_normalizer(e['location'])

    #if not e.get('stadium') and e['competition'] == 'Major League Soccer':
    #    import pdb; pdb.set_trace()


    if 'shootout_winner' not in e:
        e['shootout_winner'] = None
    else:
        if e['shootout_winner']:
            e['shootout_winner'] = get_team(e['shootout_winner'])


    if e.get('referee'):
        e['referee'] = get_name(e['referee'])
    else:
        e['referee'] = None

    if 'linesmen' in e:
        linesmen = e.pop('linesmen')

        if len(linesmen) == 0:
            pass
        elif len(linesmen) == 1:
            e['linesman1'] = get_name(linesmen[0])
        elif len(linesmen) == 2:
            e['linesman1'] = get_name(linesmen[0])
            e['linesman2'] = get_name(linesmen[1])
        elif len(linesmen) >= 3:
            e['linesman1'] = get_name(linesmen[0])
            e['linesman2'] = get_name(linesmen[1])
            e['linesman3'] = get_name(linesmen[2])
        else:
            import pdb; pdb.set_trace()
            x = 5


    if e.get('video'):
        url = e['video']

        if 'youtube.com/' in url:
            if 'watch' in url:
                code = url.split("v=")[1]
                nurl = "http://www.youtube.com/embed/%s" % code
                e['video'] = nurl

    return e


def normalize_pick(e):
    e['text'] = get_name(e['text'])
    e['team'] = get_team(e['team'])
    if e['former_team'] is not None:
        e['former_team'] = get_team(e['former_team'])
    return e


def normalize_salary(e):
    e['name'] = get_name(e['name'])
    return e


def normalize_position(e):
    e['person'] = get_name(e['person'])
    e['team'] = get_team(e['team'])
    return e

def normalize_stadiummap(e):
    e['stadium'] = get_stadium(e['stadium'])
    e['team'] = get_team(e['team'])
    return e


def normalize_team(e):

    e['name'] = get_team(e['name'])
    if e['city']:
        e['city'] = get_city(e['city'])

    return e


def normalize_stadium(e):
    e['name'] = get_stadium(e['name'])
    e['location'] = get_city(e['location'])

    e['year_opened'] = e['year_closed'] = None
  
    if type(e['opened']) == int:
        e['year_opened'] = e.pop('opened')
        e['opened'] = None

    elif type(e['opened']) == datetime.datetime:
        e['year_opened'] = e['opened'].year

    if type(e['closed']) == int:
        e['year_closed'] = e.pop('closed')
        e['closed'] = None

    elif type(e['closed']) == datetime.datetime:
        e['year_closed'] = e['closed'].year

    return e


def normalize_goal(e):
    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])

    e['team'] = get_team(e['team'])
    e['goal'] = get_name(e['goal'])
    
    if 'opponent' in e:
        e['opponent'] = get_team(e['opponent'])

    e['team'] = separate_team(e['team'], e)
    e['goal'] = separate_name(e['goal'], e)


    if e['goal'] == 'Own Goal':
        e['own_goal'] = True
        e['goal'] = None
        if e.get('assists'):
            e['own_goal_player'] = get_name(e['assists'][0])
            e['assists'] = []
            

    e['assists'] = [get_name(n) for n in e.get('assists', [])]

    if e['assists']:
        if e['assists'][0] == 'penalty kick':
            e['assists'] = []
            e['penalty'] = True

        elif e['assists'][0] == 'free kick':
            e['assists'] = []

        elif e['assists'][0] in ('unassisted', 'ua'):
            e['assists'] = []

    return e




def normalize_foul(e):
    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])

    e['team'] = get_team(e['team'])
    e['name'] = get_name(e['name'])
    return e

def normalize_stat(e):
    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])

    e['team'] = get_team(e['team'])


    try:
        e['name'] = get_name(e['name'])
    except:
        import pdb; pdb.set_trace()

    e['team'] = separate_team(e['team'], e)
    e['name'] = separate_name(e['name'], e)


    for k in (
        'games_started', 
        'games_played', 
        'goals',
        'assists',
        'minutes', 
        'shots', 
        'shots_on_goal',
        'fouls_committed', 
        'fouls_suffered', 
        'yellow_cards', 
        'red_cards'
        ):
        v = e.get(k) # stats should just pass back strings/None?
        if v is None or v in ('', '-', '?', ' '):
            e[k] = None
        else:
            try:
                e[k] = int(e[k])
            except:
                print("Failed integer coercion on %s" % e)
                import pdb; pdb.set_trace()
                e[k] = 0

    for k in 'goals', 'assists':
        if e.get(k) == '':
            e[k] = 0

    return e


def normalize_lineup(e):
    # Should handle 'end' code in lineup?

    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])

    e['team'] = get_team(e['team'])
    e['name'] = get_name(e['name'])

    e['team'] = separate_team(e['team'], e)
    e['name'] = separate_name(e['name'], e)

    if type(e['on']) == str and e['on'].endswith('\''):
        e['on'] = e['on'][:-1]

    if type(e['off']) == str and e['off'].endswith('\''):
        e['off'] = e['off'][:-1]

    return e


def normalize_standing(e):
    # What is the format for a standing?

    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])
    
    try:
        e['team'] = get_team(e['team'])
    except:
        import pdb; pdb.set_trace()

    e['team'] = separate_team(e['team'], e)

    if 'games' not in e:
        import pdb; pdb.set_trace()

    for key in ['shootout_wins', 'shootout_losses', 'ties']:
        if key not in e:
            e[key] = None

    return e


def normalize_roster(e):
    # Need to expand this.
    e['competition'] = get_competition(e['competition'])
    e['season'] = get_season(e['season'])

    e['name'] = get_name(e['name'])
    e['team'] = get_team(e['team'])
    return e


def normalize_award(e):
    e['competition'] = get_competition(e['competition'])

    if 'season' in e:
        e['season'] = get_season(e['season'])

    if e['model'] == 'Team':
        e['recipient'] = get_team(e['recipient'])
    else:
        e['recipient'] = get_name(e['recipient'])

    return e


def normalize_bio(e):
    try:
        e['name'] = get_name(e['name'])
    except:
        import pdb; pdb.set_trace()

    if e.get('birthdate') and type(e['birthdate']) == int:
        e['birthdate'] = None

    if e.get('deathdate') and type(e['deathdate']) == int:
        e['deathdate'] = None

    if e.get('birthplace'):
        e['birthplace'] = get_city(get_place(e['birthplace']))

    if e.get('deathplace'):
        e['deathplace'] = get_city(get_place(e['deathplace']))


    return e
    
    
def normalize():
    """
    Normalize different data types for collections.
    The goal here is to ensure that team, player, competition, and place names are consistent.
    That is, DaMarcus Beasley, Damarcus Beasley, and DeMarcus Beasley should all point to the same person.
    To do this, we aggressively standardize all names.
    Sometimes, this will result in different items being merged into one (e.g. Eddie Johnson and Edward Johnson)
    These will then be split up with denormalize.py.
    """

    def normalize_single_coll(coll, func):
        l = [func(e) for e in coll.find()]
        coll.drop()
        insert_rows(coll, l)

    def normalize_multiple_colls(data_type, func):
        for source in SOURCES:
            coll = soccer_db["%s_%s" % (source, data_type)]
            normalize_single_coll(coll, func)
            

    normalize_single_coll(soccer_db.seasons, normalize_season)
    normalize_single_coll(soccer_db.positions, normalize_position)

    normalize_single_coll(soccer_db.stadium_maps, normalize_stadiummap)

    normalize_single_coll(soccer_db.picks, normalize_pick)
    normalize_single_coll(soccer_db.salaries, normalize_salary)
    normalize_single_coll(soccer_db.stadiums, normalize_stadium)

    normalize_single_coll(soccer_db.teams, normalize_team)


    # Not normalizing fouls, rosters...
    # Bios only as a group.
    normalize_multiple_colls('bios', normalize_bio)
    normalize_multiple_colls('games', normalize_game)
    normalize_multiple_colls('goals', normalize_goal)
    normalize_multiple_colls('lineups', normalize_lineup)
    normalize_multiple_colls('stats', normalize_stat)
    normalize_multiple_colls('gstats', normalize_game_stat)
    normalize_multiple_colls('standings', normalize_standing)
    normalize_multiple_colls('rosters', normalize_roster)
    normalize_multiple_colls('awards', normalize_award)


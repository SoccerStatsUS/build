from collections import defaultdict
import datetime
import os

from smid.alias import get_team
from smid.mongo import soccer_db, insert_rows, generic_load

def denormalize():
    """
    Reverse the normalization process.
    This consists of a couple of different processes.
    First, we want to have correct, time-sensitive names for teams, competitions, and stadiums.
    So Sporting Kansas City should be Kansas City Wiz for 1996, Kansas City Wizards for 1997-2009, and 
    Sporting Kansas City for 2010-
    Furthermore, we will need to split some players and teams who share the same name.
    e.g. Eddie Johnson should be split into Eddie Johnson (1984) and Eddie Johnson (1988) (correct birthdates?)
    This is done by explicitly coding enough identity information to distinguish players.
    (Eddie Johnson (1984) played for FC Dallas, Sporting Kansas City, and Seattle Sounders)

    Additionally, this is where we apply stadium information to games. If we know the home team but not the location,
    we set the location to the team's stadium for that date if possible.
    """

    
    team_name_ungetter = make_team_name_ungetter()
    stadium_getter = make_stadium_getter()
    team_city_map = dict([(get_team(e['name']), e.get('city')) for e in soccer_db.teams.find()])

    print("Generating cities.")
    generate_cities()

    #print("Denormalizing games")
    l = []
    for e in soccer_db.games.find():
        e['team1_original_name'] = team_name_ungetter(e['team1'], e['date'])
        e['team2_original_name'] = team_name_ungetter(e['team2'], e['date'])

        # I suspect that this is happening far too late in the process.
        # When do stadium / city pairs get generated?
        home_team = e.get('home_team')
        if home_team and not e.get('stadium'):
            stadium = stadium_getter(home_team, e['date'])

            #if e['team1'] == 'Chicago Croatian SC':
            #    import pdb; pdb.set_trace()

            # stadium_getter returns home_team as a fallback; don't set that.
            if stadium and stadium != home_team:
                e['stadium'] = stadium
                e['location_inferred'] = True

            else:
                city = team_city_map.get(home_team)
                if city:
                    e['city'] = city
                    e['location_inferred'] = True

        elif home_team is None:
            # Fix location/city inconsistencies.
            team1_city = team_city_map.get(e['team1'])
            team2_city = team_city_map.get(e['team2'])
            if team1_city and team2_city:
                if team1_city != team2_city:
                    if team1_city == e['location']:
                        e['home_team'] = e['team1']

                    if team2_city == e['location']:
                        e['home_team'] = e['team2']

        l.append(e)

    soccer_db.games.drop()
    insert_rows(soccer_db.games, l)

    #print("Denormalizing competitions")
    #l = []

    #print("Denormalizing goals")
    l = []
    for goal in soccer_db.goals.find():
        if goal['date']:
            goal['team_original_name'] = team_name_ungetter(goal['team'], goal['date'])

        l.append(goal)

    soccer_db.goals.drop()
    insert_rows(soccer_db.goals, l)


    #print("Denormalizing stats")
    #l = []
    #for stat in soccer_db.stats.find():
    #    l.append(stat)

    #soccer_db.stats.drop()
    #insert_rows(soccer_db.stats, l)
            
    #print("Denormalizing lineups")
    lineups = []
    for lineup in soccer_db.lineups.find():

        #if lineup['date'] == datetime.datetime(2012, 8, 7) and lineup['team'] == 'Chivas USA Reserves' and 'Jorge' in lineup['name']:
        #    import pdb; pdb.set_trace()

        lineup['team_original_name'] = team_name_ungetter(lineup['team'], lineup['date'])
        lineups.append(lineup)

    soccer_db.lineups.drop()
    insert_rows(soccer_db.lineups, lineups)

    hall_of_famers = set([e['recipient'] for e in soccer_db.awards.find({'award': 'US Soccer Hall of Fame'})])

    l = []
    for e in soccer_db.bios.find():
        e['hall_of_fame'] = e['name'] in hall_of_famers
        l.append(e)
    
    soccer_db.bios.drop()
    insert_rows(soccer_db.bios, l)

    #print("Denormalizing standings")
    #standings = []

    #for s in soccer_db.standings.find():
    #    standings.append(s)

    #soccer_db.standings.drop()
    #insert_rows(soccer_db.standings, standings)


def make_stadium_getter():
    """
    Given a team name, eg FC Dallas and a date, return the appropriate stadium.
    """
    
    from soccerdata.text import stadiummap

    d = defaultdict(list)
    for x in stadiummap.load():
        key = x['team']
        value = (x['stadium'], x['start'], x['end'])
        d[key].append(value)


    def getter(team, team_date):
        
        if team_date is None:
            return team
        
        if team not in d:
            return team
        else:
            times_list = d[team]

            for u in times_list:
                try:
                    t, start, end = u
                except:
                    import pdb; pdb.set_trace()
                if start <= team_date <= end:
                    return t

        # fallback.
        return team

    return getter



def make_reverse_stadium_getter():
    """
    Given a stadium name, eg FC Dallas Stadium and a date, return the appropriate team.
    """
    # Unfinished since this seems ill-conceived.
    # Should return a list? This can be a little ambiguous.
    
    from soccerdata.text import stadiummap

    d = defaultdict(list)
    for x in stadiummap.load():
        key = x['stadium']
        value = (x['team'], x['start'], x['end'])
        d[key].append(value)


    def getter(stadium, team_date):
        
        if team_date is None:
            return stadium
        
        if team not in d:
            return team
        else:
            times_list = d[team]

            for u in times_list:
                try:
                    t, start, end = u
                except:
                    import pdb; pdb.set_trace()
                if start <= team_date <= end:
                    return t

        # fallback.
        return team

    return getter





def make_team_name_ungetter():
    """
    Given a canonical name, eg FC Dallas, return the time-specific name, e.g. Dallas Burn.
    """
    from soccerdata.text import namemap

    d = defaultdict(list)
    for x in namemap.load():
        key = x['from_name']
        value = (x['to_name'], x['start'], x['end'])
        d[key].append(value)


    def getter(name, name_date):

        if name_date is None:
            return name
        
        if name not in d:
            return name



        # Load the mapping of dates to team names
        # and iterate through it
        # e.g. [('Dallas Burn', 1/1/1996, 12/31/2001), ...]
        times_list = d[name]
        for u in times_list:
            try:
                t, start, end = u
            except:
                import pdb; pdb.set_trace()
            if start <= name_date <= end:
                return t

        # fallback.
        return name


    return getter
        

def make_competition_name_ungetter():
    """
    Given a canonical name, eg US Open Cup, return the time-specific name, e.g. National Challenge Cup
    """
    from soccerdata.text import competitionnamemap

    d = defaultdict(list)
    for x in namemap.load():
        key = x['from_name']
        value = (x['to_name'], x['seasons'])
        d[key].append(value)


    def getter(name, name_season):

        if name_date is None:
            return name
        
        if name not in d:
            return name

        # Load the mapping of dates to team names
        # and iterate through it
        # e.g. [('Dallas Burn', 1/1/1996, 12/31/2001), ...]        

        to, seasons = d[name]
        if name_season in seasons:
            return to


        return name

    return getter
        
        
def generate_cities():

    cities = set()


    for e in soccer_db.teams.find():
        if 'city' in e:
            cities.add(e['city'])

    for e in soccer_db.bios.find():
        cities.add(e.get('birthplace'))
        cities.add(e.get('deathplace'))



    for e in soccer_db.games.find():
        if 'location' in e:
            cities.add(e['location'])



    for e in soccer_db.stadiums.find():
        cities.add(e['location'])

    if None in cities:
        cities.remove(None)


    city_dicts = [{'name': city} for city in sorted(cities)]
    
    generic_load(soccer_db.cities, lambda: city_dicts)


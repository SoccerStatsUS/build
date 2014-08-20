from collections import defaultdict
import datetime
import os

from build.alias import get_team
from build.mongo import soccer_db, insert_rows, generic_load

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
    
    denormalize_games()
    denormalize_goals()
    denormalize_lineups()
    denormalize_game_stats()
    denormalize_stats()

    
def denormalize_games():

    l = []
    for e in soccer_db.games.find():
        e['team1_original_name'] = team_name_ungetter(e['team1'], e['date'])
        e['team2_original_name'] = team_name_ungetter(e['team2'], e['date'])
        l.append(e)

    soccer_db.games.drop()
    insert_rows(soccer_db.games, l)

    #print("Denormalizing competitions")
    #l = []


def denormalize_goals():

    l = []
    for goal in soccer_db.goals.find():
        if goal['date']:
            goal['team_original_name'] = team_name_ungetter(goal['team'], goal['date'])

        l.append(goal)

    soccer_db.goals.drop()
    insert_rows(soccer_db.goals, l)


def denormalize_stats():

    pass

    #print("Denormalizing stats")
    #l = []
    #for stat in soccer_db.stats.find():
    #    l.append(stat)

    #soccer_db.stats.drop()
    #insert_rows(soccer_db.stats, l)


def denormalize_lineups():
            
    lineups = []
    for lineup in soccer_db.lineups.find():

        #if lineup['date'] == datetime.datetime(2012, 8, 7) and lineup['team'] == 'Chivas USA Reserves' and 'Jorge' in lineup['name']:
        #    import pdb; pdb.set_trace()

        lineup['team_original_name'] = team_name_ungetter(lineup['team'], lineup['date'])
        lineups.append(lineup)


    soccer_db.lineups.drop()
    insert_rows(soccer_db.lineups, lineups)


def denormalize_game_stats():


    game_stats = []
    for gs in soccer_db.game_stats.find():

        gs['team_original_name'] = team_name_ungetter(gs['team'], gs['date'])
        game_stats.append(gs)

    soccer_db.game_stats.drop()
    insert_rows(soccer_db.game_stats, game_stats)


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


def make_reverse_stadium_getter():
    """
    Given a stadium name, eg FC Dallas Stadium and a date, return the appropriate team.
    """
    # Unfinished since this seems ill-conceived.
    # Should return a list? This can be a little ambiguous.
    
    from metadata.parse import stadiummap

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
    from metadata.parse import namemap

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
    from metadata.parse import competitionnamemap

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


team_name_ungetter = make_team_name_ungetter()

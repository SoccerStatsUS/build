from collections import defaultdict

from build.mongo import generic_load, soccer_db, insert_rows, insert_row
from build.alias import get_team

from settings import SOURCES

# This is for fixing errors in data that we can't address otherwise.
# Currently, remove duplicate players from soccernet game reports
# e.g. http://soccernet.espn.go.com/match?id=259398&cc=5901

# Correct team names for U-20, U-17 World Cup
# e.g. United States -> United States U-17



def transform():

    # Change this to add stuff to ends?

    # Transform team names for a given competition based on the applied formatting string.
    # e.g. United States -> United States U-17.
    transform_team_names_for_competition('fifa', 'FIFA U-17 World Cup', '%s U-17')
    transform_team_names_for_competition('fifa', 'FIFA U-20 World Cup', '%s U-20')
    transform_team_names_for_competition('fifa', 'Olympic Games', '%s Olympic')

    transform_team_names_for_competition('world_i', 'FIFA U-17 World Cup', '%s U-17')
    transform_team_names_for_competition('world_i', 'FIFA U-20 World Cup', '%s U-20')
    transform_team_names_for_competition('world_i', 'Olympic Games', '%s Olympic')

    transform_team_names_for_competition('concacaf_i', 'CONCACAF U-17 Championship', '%s U-17')
    transform_team_names_for_competition('concacaf_i', 'CONCACAF U-20 Championship', '%s U-20')
    transform_team_names_for_competition('concacaf_i', 'Olympic Games qualification (CONCACAF)', '%s Olympic')
    transform_team_names_for_competition('concacaf_i', 'Olympic Games qualification', '%s Olympic')


    #transform_team_names_for_competition('mls', 'MLS Reserve League', '%s Reserve')




def transform_team_names_for_competition(coll_group, competition, string_format):
    """
    For a given and collection, competition, transform team names based on the give formatting string.
    """

    games = []
    coll = soccer_db["%s_games" % coll_group]
    for e in coll.find():
        if e['competition'] == competition:
            e['team1'] = string_format % e['team1']
            e['team2'] = string_format % e['team2']

        games.append(e)

    coll.drop()
    insert_rows(coll, games)

    goals = []
    coll = soccer_db["%s_goals" % coll_group]
    for e in coll.find():
        if e['competition'] == competition:
            e['team'] = string_format % e['team']

        goals.append(e)

    coll.drop()
    insert_rows(coll, goals)

    lineups = []
    coll = soccer_db["%s_lineups" % coll_group]
    for e in coll.find():
        if e['competition'] == competition:
            e['team'] = string_format % e['team']

        lineups.append(e)

    coll.drop()
    insert_rows(coll, lineups)

    stats = []
    coll = soccer_db['%s_stats' % coll_group]
    for e in coll.find():
        if e['competition'] == competition:
            e['team'] = string_format % e['team']

        stats.append(e)

    coll.drop()
    insert_rows(coll, stats)











def make_player_name_guesser():
    # Uses all-time rosters to guess player names for teams.
    # All-time rosters are generated by the generate all-time rosters function?
    
    d = defaultdict(set)
    for e in soccer_db.rosters.find({'end': None, 'start': None}):
        d[e['team']].add(e['name'])

    def getter(name, team):
        candidates = d[team]              
        return get_name_from_fragment(name, candidates)

    return getter


def sanitize_lineups():
    """
    Some sort of sanity check. Probably shouldn't be here anyway.
    """

    l = []

    for s in SOURCES:
        game_set = set()

        coll = soccer_db["%s_standings" %s]

        for e in coll.find():
            t = (e['name'], e['team'], e['date'])
            if t in game_set:
                pass
            else:
                game_set.add(t)
                l.append(e)



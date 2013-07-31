from smid.mongo import generic_load, soccer_db, insert_rows, insert_row
from smid.settings import SOURCES

from collections import defaultdict
import datetime
import random




# Merge should be used for avoiding duplicate elements.

def merge():
    merge_standings()
    merge_awards()
    merge_all_stats()
    merge_all_games()

    merge_goals()
    merge_lineups()
    merge_game_stats()
    merge_fouls()

    merge_bios()

    merge_teams()

    merge_all_rosters()
        


def standard_merge(coll):
    from settings import SOURCES

    soccer_db[coll].drop()
    for e in SOURCES:
        insert_rows(soccer_db[coll], soccer_db['%s_%s' % (e, coll)].find())


def merge_teams():
    #soccer_db.teams.drop()
    #insert_rows(soccer_db.teams, soccer_db.chris_teams.find())
    #insert_rows(soccer_db.teams, soccer_db.wiki_teams.find())
    pass



def merge_standings():
    standard_merge('standings')


def merge_awards():
    standard_merge('awards')

    return
    soccer_db.awards.drop()
    insert_rows(soccer_db.awards, soccer_db.asl_awards.find())
    insert_rows(soccer_db.awards, soccer_db.nasl_awards.find())
    insert_rows(soccer_db.awards, soccer_db.apsl_awards.find())
    insert_rows(soccer_db.awards, soccer_db.mls_awards.find())
    insert_rows(soccer_db.awards, soccer_db.ncaa_awards.find())
    insert_rows(soccer_db.awards, soccer_db.usl_awards.find())
    insert_rows(soccer_db.awards, soccer_db.asl_awards.find())
    insert_rows(soccer_db.awards, soccer_db.usa_awards.find())

    
    

def merge_goals():

    dd = {}

    def update_goal(d):
        if '_id' in d:
            d.pop("_id")
        
        # Issues here: a player scores two goals in the same minute.
        # A player scores in a game, we don't have a minute, but we have separate sources referring.
        # Add a source key here.

        if d['minute']:
            try:
                key = (d['date'], d['goal'], d['minute'])
            except:
                import pdb; pdb.set_trace()
        else: 
            # For the case where a player has scored multiple goals, but we don't have a minute for any of them.
            # random.random() -> None.
            key = (d['date'], d['goal'], random.random())

        # source_id not implemented, but should be something simple (timestamp, counter)
        # to distinguish different internal 'sources' - different files or scrapes, basically.
        if key in dd: # and orig.get('source_id') != d.get('source_id'): 
            orig = dd[key]

            for k, v in d.items():
                if not orig.get(k) and v:
                    orig[k] = v

        # Otherwise, add the game.
        else:
            dd[key] = d

        
    for e in SOURCES:
        c = '%s_goals' % e
        coll = soccer_db[c]
        for e in coll.find():
            update_goal(e)
            
    soccer_db.goals.drop()
    insert_rows(soccer_db.goals, dd.values())





def merge_game_stats():

    dd = {}

    def update_game_stat(d):
        if '_id' in d:
            d.pop("_id")
        
        key = tuple([d[k] for k in ['player', 'team', 'date', 'competition', 'season']])

        if key in dd:
            orig = dd[key]

            for k, v in d.items():
                if not orig.get(k) and v:
                    orig[k] = v

        else:
            dd[key] = d

        
    for e in SOURCES:
        c = '%s_gstats' % e
        coll = soccer_db[c]
        for e in coll.find():
            update_game_stat(e)
            
    soccer_db.gstats.drop()
    insert_rows(soccer_db.gstats, dd.values())





def merge_fouls():

    dd = {}

    def update_foul(d):
        if '_id' in d:
            d.pop("_id")
        
        key = (d['date'], d['name'])

        if key not in dd: 
            dd[key] = d
        else:
            orig = dd[key]
            for k, v in d.items():
                if not orig.get(k) and v:
                    orig[k] = v
        
    for e in SOURCES:
        c = '%s_fouls' % e
        coll = soccer_db[c]
        for e in coll.find():
            update_foul(e)
            
    soccer_db.fouls.drop()
    insert_rows(soccer_db.fouls, dd.values())


def merge_lineups():

    dd = {}

    def update_lineup(d):
        d.pop("_id")

        # add source_id here also.
        key = (d['name'], d['date'], d['team'])

        if key in dd: 
            orig = dd[key]
            for k, v in d.items():
                if not orig.get(k) and v:
                    orig[k] = v

        # Otherwise, add the game.
        else:
            dd[key] = d

        
    for e in SOURCES:
        c = '%s_lineups' % e
        coll = soccer_db[c]
        for e in coll.find():
            update_lineup(e)
            
    soccer_db.lineups.drop()
    insert_rows(soccer_db.lineups, dd.values())



def merge_all_games():            
    games_coll_names = ['%s_games' % coll for coll in SOURCES]
    games_lists = [soccer_db[k].find() for k in games_coll_names]

    games = merge_games(games_lists)
    soccer_db.games.drop()
    insert_rows(soccer_db.games, games)



def merge_all_rosters():

    roster_coll_names = ['%s_rosters' % coll for coll in SOURCES]
    roster_lists = [soccer_db[k].find() for k in roster_coll_names]

    rosters = merge_rosters(roster_lists)
    soccer_db.rosters.drop()
    insert_rows(soccer_db.rosters, rosters)


def merge_rosters(roster_lists):

    def update_roster(d):
        # Need to consider how rosters interact with seasons, start/end dates.
        # Currently going to just ignore start/end dates for all rosters.


        if '_id' in d:
            d.pop('_id')

        key = (d['team'], d['season'], d['name'])

        if key not in roster_dict:
            roster_dict[key] = d

        
    roster_dict = {}

    for roster_list in roster_lists:
        for e in roster_list:
            update_roster(e)

    return roster_dict.values()


def merge_games(games_lists):
    """
    Merge games to prevent overlaps, then
    insert into the games db.
    """

    def update_game(d):

        if '_id' in d:
            d.pop("_id")

        

        teams = tuple(sorted([d['team1'], d['team2']]))

        # add source_id here to handle no date overlaps.
        key = (teams, d['date'], d['season'])


        #if sorted([d['team1'], d['team2']]) == ['Los Angeles Blues', 'Phoenix FC']:
        #    import pdb; pdb.set_trace()

        # Add the game if we don't have a match.
        if key not in game_dict:
            game_dict[key] = d

        # If there is already a game, update empty fields.
        else:
            orig = game_dict[key]

            # Overreaction to a bug that was seriously mangling scores when multiple games records were present.
            # (Was replacing scores of 0 with the larger score for both games.)
            t1, t2, t1s, t2s, t1r, t2r = [d.pop(e) for e in ('team1', 'team2', 'team1_score', 'team2_score', 'team1_result', 'team2_result')]
            if t1 == orig['team1'] and t2 == orig['team2']:
                pass
            elif t1 == orig['team2'] and t2 == orig['team1'] and d['date'] is not None: # make allowances for multiple unknown dates...
                t1, t1s, t1r, t2, t2s, t2r = t2, t2s, t2r, t1, t1s, t1r
                try:
                    assert t1s == orig['team1_score']
                    assert t2s == orig['team2_score']
                    assert t1r == orig['team1_result']
                    assert t1r == orig['team1_result']
                except:
                    print("Game information mismatch.")
                    #print(orig)
                    #print(d)

                    #import pdb; pdb.set_trace()
            else:
                if d['date'] is not None:
                    print("Game information mismatch.")
                    print(orig)
                    print(d)
                
            for k, v in d.items():
                if not orig.get(k) and v:
                    orig[k] = v

            orig['sources'] = orig.get('sources', []) + d.get('sources', [])

        game_dict[key]['merges'] = game_dict[key].get('merges', 0) + 1

    game_dict = {}

    for games_list in games_lists:
        for e in games_list:
            update_game(e)

    return game_dict.values()


def merge_bios():
    """
    Merge bios
    """

    bio_dict = {}


    def update_bio(d):
        # This will overmerge. e.g.
        # { 'name': 'John Smith', 'birthdate': datetime.datetime(1900, 1, 1) }
        # { 'name': 'John Smith', 'birthdate': datetime.datetime(1980, 6, 15), 'birthplace': 'Atlanta, Georgia' } 
        # -> { 'name': 'John Smith', 'birthdate': datetime.datetime(1900, 1, 1), birthplace': 'Atlannta, Georgia' }
        # Probably want to under-merge, then apply split logic.
        
        n = d['name']
        
        if n in bio_dict:
            orig = bio_dict[n]
            for k, v in d.items():
                if not orig.get(k) and v:
                    orig[k] = v
        else:
            bio_dict[n] = d

      
    for e in SOURCES:
        c = '%s_bios' % e
        coll = soccer_db[c]
        for e in coll.find():
            update_bio(e)

    soccer_db.bios.drop()
    insert_rows(soccer_db.bios, bio_dict.values())



def merge_all_stats():            
    stats_lists = [soccer_db[k].find() for k in ['%s_stats' % coll for coll in SOURCES]]
    stats = merge_stats(stats_lists)

    soccer_db.stats.drop()
    insert_rows(soccer_db.stats, stats)

    
def merge_stats(stats_lists):
    """
    Merge stats.
    """


    def update_stat(d):
        if 'team' not in d:
            import pdb; pdb.set_trace()
        t = (d['name'], d['team'], d['competition'], d['season'])
        if t in stat_dict:
            orig = stat_dict[t]
            for k, v in d.items():
                if not orig.get(k) and v:
                    orig[k] = v
        else:
            stat_dict[t] = d

    stat_dict = {}
    for stats_list in stats_lists:
        for e in stats_list:
            update_stat(e)

    return stat_dict.values()


if __name__ == "__main__":
    merge()

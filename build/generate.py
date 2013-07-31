from collections import defaultdict

from smid.mongo import soccer_db, insert_rows, generic_load
from standings import get_standings


# I think I should just generate standings directly from soccer_db.games.
# And then check those against downloaded standings.


make_stat_tuple = lambda name, d: (name, d['team'], d['season'], d['competition'])



def generate():
    generate_competition_standings()
    generate_game_stats()
    generate_competition_stats() # Use game stats to make competition stats.



def generate_game_stats():
    """
    Generate player statistics for individual games.
    Like the stuff you see on uslsoccer.com.
    """
    # Start scraping actual game stats from mlssoccer.com, uslsoccer.com, etc.

    stats = defaultdict(lambda: defaultdict(int))

    for g in soccer_db.goals.find():
        if g['goal']:
            key = tuple([g[k] for k in ['goal', 'team', 'date', 'competition', 'season']])
            stats[key]['goals'] += 1
            stats[key]['games_played'] = 1
            for assist in g['assists']:
                k = tuple([assist] + [g[k] for k in ['team', 'date', 'competition', 'season']])
                stats[k]['assists'] += 1

    #for f in soccer_db.fouls.find():
    #    key = tuple([f[k] for k in ['name', 'team', 'date', 'competition', 'season']])
    #    stats[key]['red_cards'] += 1

    for l in soccer_db.lineups.find():
        key = tuple([l[k] for k in ['name', 'team', 'date', 'competition', 'season']])
        #stats[key].update({ 'on': l['on'],
        #                    'off': l['off'],
        #                    })
        stats[key]['games_played'] = 1
        if l['on'] == 0:
            stats[key]['games_started'] = 1

        if type(l['on']) == int and type(l['off']) == int:
            stats[key]['minutes'] += l['off'] - l['on']

    l = []
    for key, v in stats.items():
        d = dict(zip(['player', 'team', 'date', 'competition', 'season'], key))
        v.update(d)
        v['goals'] = v['goals'] or 0
        l.append(v)
        

    #soccer_db.gstats.drop()
    generic_load(soccer_db.gstats, lambda: l)


def generate_competition_stats():

    def competition_generate(competition):
        x = generate_stats(soccer_db.goals.find({'competition': competition}), soccer_db.lineups.find({"competition": competition}))
        generic_load(soccer_db.stats, lambda: x.values())

    l = [
        'FIFA Club World Cup',
        'FIFA World Cup',
        'FIFA U-20 World Cup',
        'FIFA U-17 World Cup',
        'FIFA Confederations Cup',
        'FIFA World Cup qualification (CONCACAF)',
        'FIFA World Cup qualification (CONMEBOL)',

        'Intercontinental Cup',
        'Interamerican Cup',
        'Recopa Sudamericana',
        'SURUGA Bank Championship',
        'La Copita del Mundo',

        'World Cup Qualifying',
        'Olympic Games',
        'International Friendly',
        'Gold Cup',    
        'CONCACAF Championship',
        'Copa Centroamericana',
        'Caribbean Cup',
        'Copa America',
        'Copa Merconorte',
        'Copa Mercosur',
        'CONCACAF Champions League',
        'CONCACAF Cup Winners Cup',
        'CONCACAF Giants Cup',
        #'CONCACAF Champions\' Cup',
        'North American SuperLiga',
        'Copa Interclubes UNCAF',
        'CFU Club Championship',
        'Copa Libertadores',
        'Copa Sudamericana',
        'Copa CONMEBOL',
        'Copa Masters CONMEBOL',
        'MLS Cup Playoffs',
        'MLS Reserve League',
        'AFA Cup',
        'U.S. Open Cup',
        'Canadian Championship',
        'American League of Professional Football',
        'Eastern Soccer League (1928-1929)',
        'International Soccer League',
        'USSF Division 2 Professional League',

        'Liga MX',
        'Argentine Primera División',

        'Hyundai A-League',

        'Liga MX Liguilla',
        'Campeón de Campeones',
        'Campeonato Brasileiro Série A',
        'Categoría Primera A',
        'Ecuadorian Serie A',
        'Chinese Super League',
        'American Soccer League (1934-1983)',
        'Mundialito',
        'Women\'s Professional Soccer',
        'Women\'s United Soccer Association',
        'Liga Nacional de Guatemala',
        'Liga Nacional de Honduras',
        'Liga Panameña de Fútbol',
        'Primera División de Costa Rica',
        'Salvadoran Primera División',
        #'North American Soccer League',
        ]

    for e in l:
        competition_generate(e)




def generate_competition_standings():
    """Generate rolling standings for a given competition."""
    # Don't generate based on collection (definitely will overcount games.

    def sg2(competition):
        stg = generate_standings(competition)
        generic_load(soccer_db.standings, lambda: stg)

    l = [
        'FIFA Club World Cup',
        'Intercontinental Cup',
        'Interamerican Cup',
        'Recopa Sudamericana',
        'SURUGA Bank Championship',
        'La Copita del Mundo',    
        'Copa Libertadores',
        'Copa Sudamericana',
        'Copa CONMEBOL',
        'Copa Masters CONMEBOL',
        'CONCACAF Champions League',
        'Copa Interclubes UNCAF',
        'CFU Club Championship',    
        'CONCACAF Cup Winners Cup',
        'CONCACAF Giants Cup',
        'North American Superliga',
        'Women\'s Professional Soccer',
        'National Women\'s Soccer League',
        'Women\'s Premier Soccer League',
        'Women\'s United Soccer Association',
        'International Soccer League',
        'Eastern Soccer League (1928-1929)',
        'Major League Soccer',
        'North American Soccer League',
        'National Professional Soccer League',
        'United Soccer Association',
        'American Soccer League (1921-1933)',
        'MLS Reserve League',
        'MLS Cup Playoffs',
        'U.S. Open Cup',
        'Hyundai A-League',
        'Canadian Championship',
        'Liga MX',
        ]

    for e in l:
        sg2(e)



class Standing(object):
    def __init__(self, game, team, standing=None):
        self.team = team
        self.date = game['date']
        self.competition = game['competition']
        self.season = game['season']

        if standing:
            self.wins = standing.wins
            self.ties = standing.ties
            self.losses = standing.losses
            self.goals_for = standing.goals_for
            self.goals_against = standing.goals_against
        else:
            self.wins = self.ties = self.losses = self.goals_for = self.goals_against = 0

        # Not really handling these anywhere yet.
        self.shootout_wins = self.shootout_losses = 0

        ht, at, h, a = [game[k] for k in ['team1', 'team2', 'team1_score', 'team2_score']]

        if team == ht:
            gf, ga = h, a
        else:
            ga, gf = h, a

        self.goals_for += gf or 0
        self.goals_against += ga or 0

        if h == None or a == None:
            return

        if h == a:
            self.ties += 1
        elif ht == team and h > a:
            self.wins += 1
        elif at == team and a > h:
            self.wins += 1
        else:
            self.losses += 1


    def to_dict(self):
        return {
            'team': self.team,
            'date': self.date,
            'competition': self.competition,
            'season': self.season,
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'shootout_wins': self.shootout_wins,
            'shootout_losses': self.shootout_losses,
            'games': self.wins + self.losses + self.ties,
            'goals_for': self.goals_for,
            'goals_against': self.goals_against,
            'final': False,
            }
                
            

def generate_standings(competition):
    """
    Given a competition, produce team standings for that competition.
    """

    standing_dict = defaultdict(list)

    # This exists so we can find standings with arbitrary datetimes.
    # Seems like this whole thing might be better structured as a dict of lists?

    def generate_team_standing(game, team):

        key = (team, competition, game['season'])

        if key in standing_dict:
            standing = standing_dict[key][-1]
            new_standing = Standing(game, team, standing)
        else:
            new_standing = Standing(game, team)

        standing_dict[key].append(new_standing)


    for game in soccer_db.games.find({'competition': competition}).sort('date', 1):

        generate_team_standing(game, game['team1'])
        generate_team_standing(game, game['team2'])


    standings = []
    for lst in standing_dict.values():
        standings.extend([e.to_dict() for e in lst])




    return standings



def generate_stats(goals=[], lineups=[]):
    """
    Generate a stat dict from goals, lineups
    """
    # This duplicates game_stats functionality. Use the game_stats
    # to generate the stats.
    

    sd = {}

    def add_item(t, key, amount=1):
        """
        Add goal, lineup, etc to the stat dict.
        """

        # Generate empty stat objects.
        if t not in sd:
            name, team, season, competition = t
            if not name:
                #"Name not in tuple %s" % str(t)
                return

            sd[t] = {
                'name': name,
                'team': team,
                'season': season,
                'competition': competition,
                'goals': 0,
                'assists': 0,
                'games_played': 0,
                'games_started': 0,
                'minutes': 0,
                }

        #if t[0] == 'Omar Bravo' and t[1] == 'UANL':
        #    print(sd[t])


        # Increment the appropriate key.
        sd[t][key] += amount


    for goal in goals:
        t = make_stat_tuple(goal['goal'], goal)
        add_item(t, 'goals')

        for assist in goal['assists']:
            t = make_stat_tuple(assist, goal)
            add_item(t, 'assists')

    # This is where things are breaking for Omar Bravo.
    for lineup in lineups:
        t = make_stat_tuple(lineup['name'], lineup)

        # Empty lineup 
        if lineup['on'] == 0 and lineup['off'] == 0:
            pass
        else:
            if lineup['on'] == 0:
                add_item(t, 'games_started')
            add_item(t, 'games_played')

            if lineup['off'] is not None and lineup['on'] is not None:
                try:
                    minutes = lineup['off'] - lineup['on']
                    add_item(t, 'minutes', minutes)
                except TypeError:
                    print(lineup)
            else:
                pass
                #print("Missing minute data for appearance.")
        

    return sd

    

             
if __name__ == "__main__":
    generate()


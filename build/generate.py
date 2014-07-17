from collections import defaultdict

from smid.mongo import soccer_db, insert_rows, generic_load
from standings import get_standings

# I think I should just generate standings directly from soccer_db.games.
# And then check those against downloaded standings.


make_stat_tuple = lambda name, d: (name, d['team'], d['season'], d['competition'])


def stadiums_to_teams():
    from soccerdata.text import stadiummap
    from smid.alias import get_stadium

    d = defaultdict(set)

    for e in stadiummap.load():
        key = get_stadium(e['stadium'])
        value = e['team']
        d[key].add(value)

    return d
        


def make_stadium_getter():
    """
    Given a team name, eg FC Dallas and a date, return the appropriate stadium.
    """
    # This is also done in sdev...
    
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


def generate():
    generate_game_data()
    generate_competition_standings()
    generate_game_stats()
    generate_competition_stats() # Use game stats to make competition stats.
    generate_cities()



def generate_game_data():
    """
    Infer 
    - home team using location
    - location using home team
    """
    # By this point, location should be gone, replaced by stadium/city/state/country

    stadium_getter = make_stadium_getter()
    team_city_map = dict([(e['name'], e.get('city')) for e in soccer_db.teams.find()])

    stadium_mapper = stadiums_to_teams()

    l = []

    for e in soccer_db.games.find():

        home_team = e.get('home_team')
        if home_team and not e.get('stadium'):
            stadium = stadium_getter(home_team, e['date'])

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
            # Get home team based on team info.
            # Fix location/city inconsistencies.

            # If we know about a stadium, try to use the stadium.
            if 'stadium' in e and e['stadium'] in stadium_mapper:                
                try:
                    teams = stadium_mapper[e['stadium']]
                except:
                    import pdb; pdb.set_trace()

                if e['team1'] in teams and e['team2'] not in teams:
                    e['home_team'] = e['team1']
                elif e['team2']:
                    e['home_team'] = e['team2']

            else:

                team1_city = team_city_map.get(e['team1'])
                team2_city = team_city_map.get(e['team2'])
                if team1_city and team2_city:
                    if team1_city != team2_city and e.get('location'):
                        if team1_city == e['location']:
                            e['home_team'] = e['team1']

                        if team2_city == e['location']:
                            e['home_team'] = e['team2']

        l.append(e)

    soccer_db.games.drop()
    insert_rows(soccer_db.games, l)




def generate_game_stats():
    """
    Generate player statistics for individual games.
    Like the stuff you see on uslsoccer.com.
    """
    # Start scraping actual game stats from mlssoccer.com, uslsoccer.com, etc.

    make_key = lambda d: tuple([d[key] for key in ['player', 'team', 'date', 'competition', 'season']])

    stats = defaultdict(lambda: defaultdict(int))

    for g in soccer_db.goals.find():
        if g['goal']:
            if 'Own Goal' in g['assists']:
                # need to add opponent in normalize.
                if 'opponent' in g: 
                    key = tuple([g[k] for k in ['goal', 'opponent', 'date', 'competition', 'season']])
                    stats[key]['own_goals'] += 1
                    #stats[key]['games_played'] = 1 #don't add games played on goals; not useful info.

                    k2 = tuple(['Own Goal'] + [g[k] for k in ['opponent', 'date', 'competition', 'season']])
                    stats[k2]['goals'] += 1

            else:
                key = tuple([g[k] for k in ['goal', 'team', 'date', 'competition', 'season']])
                stats[key]['goals'] += 1
                #stats[key]['games_played'] = 1 #don't add games played on goals; not useful info.
                for assist in g['assists']:
                    k = tuple([assist] + [g[k] for k in ['team', 'date', 'competition', 'season']])
                    stats[k]['assists'] += 1

    #for f in soccer_db.fouls.find():
    #    key = tuple([f[k] for k in ['name', 'team', 'date', 'competition', 'season']])
    #    stats[key]['red_cards'] += 1

    for l in soccer_db.lineups.find():


        # Player didn't play - different from 
        #if l['on'] == 0 and l['off'] == 0:
        if l.get('unused') == True:
            continue

        key = tuple([l[k] for k in ['name', 'team', 'date', 'competition', 'season']])

        stats[key]['games_played'] = 1

        if l['on'] == 0:
            stats[key]['games_started'] = 1

        if type(l['on']) == int and type(l['off']) == int:
            stats[key]['minutes'] += l['off'] - l['on']
            stats[key]['on'] = l['on']
            stats[key]['off'] = l['off']

            #if l['on'] == 90 and l['off'] == 90:
            #    import pdb; pdb.set_trace()

        # Presumably a starter where we don't know when he came off.
        elif type(l['on']) == int:
            stats[key]['on'] = l['on']
            stats[key]['off'] = None 
            stats[key]['minutes'] = 90 # Know this is wrong, but will be closer than nothing

        # Presumably a substitute where we don't know when he came on.
        elif type(l['off']) == int:
            stats[key]['on'] = None
            stats[key]['off'] = 90 # Change this to total game minutes
            stats[key]['minutes'] = 0 # Know this is wrong, but will be closer than nothing

        # Hunting these...
        else:
            # Colin Jose NASL lineups, eg
            # All we know is who played, not starters/subs
            #import pdb; pdb.set_trace()
            pass

        stats[key]['order'] = l.get('order')

    l = []
    for key, v in stats.items():
        d = dict(zip(['player', 'team', 'date', 'competition', 'season'], key))
        v.update(d)
        v['goals'] = v['goals'] or 0
        l.append(v)
        

    extant = set([make_key(e) for e in soccer_db.gstats.find()])
    lx = [e for e in l if make_key(e) not in extant]

    #soccer_db.gstats.drop()
    generic_load(soccer_db.gstats, lambda: lx)



def generate_competition_stats():

    def competition_generate(competition):
        x = generate_stats(soccer_db.gstats.find({'competition': competition}))
        #import pdb; pdb.set_trace()
        generic_load(soccer_db.stats, lambda: x.values())
        #import pdb; pdb.set_trace()
        y = 5

    # Move this out into a global variable.
    l = [

        # Women
        'Women\'s Professional Soccer',
        'Women\'s United Soccer Association',
        'Damallsvenskan',

        # Misc

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

        # US Minor

        'American Professional Soccer League', 
        'USSF Division 2 Professional League',
        'North American Soccer League (2011-)',


        # CONCACAF
        'Liga MX',
        'Liga Nacional de Guatemala',
        'Liga Nacional de Honduras',
        'Liga Panameña de Fútbol',
        'Primera División de Costa Rica',
        'Salvadoran Primera División',

        # CONMEBOL
        'Argentine Primera División',
        'Brasileirão',

        'Ecuadorian Serie A',
        'Categoría Primera A',
        'Uruguayan Primera División',
        'Paraguayan Primera División',
        'Peruvian Primera División',
        'Chilean Primera División',
        'Liga de Fútbol Profesional Boliviano',

        'Campeonato Metropolitano (Argentina)',

        'Campeonato Paulista',
        'Rio de Janeiro Championship ',
        'Campeonato Mineiro',

        # UEFA 

        'UEFA Champions League',

        'Serie A',
        'La Liga',
        'Premier League',
        '1. Bundesliga',
        'Ligue 1',

        'Superligaen',
        'Tippeligaen',
        'Allsvenskan',

        'Super Lig',
        'Belgian Pro League',
        'Eredivisie',
        'Primeira Liga',

        'Scottish Premier League',
        'Ekstraklasa',
        'Austrian Bundesliga',
        'Swiss Super League',

        'Russian Premier League',
        'Ukrainian Premier League',
        'Gambrinus Liga',
        'Nemzeti Bajnokság I',

        # Poland, Czech, Scotland, Switzerland, Austria, ...
        # Hungary, Ukraine, Serbia, Romania, Greece, Russia

        # ASIA
        'Hyundai A-League',
        'Chinese Super League',
        'K League',
        'J. League',


        # other

        'Liga MX Liguilla',
        'Campeón de Campeones',

        'American Soccer League (1933-1983)',
        'Mundialito',



        # Overlap?
        #'USL Second Division',
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

        'UEFA Champions League',
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
        'Premier League',
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
        self.shootout_wins = self.shootout_losses = None

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



def generate_stats(gstats=[]):
    sd = {}

    for gstat in gstats:
        try:
            t = make_stat_tuple(gstat['player'], gstat)
        except:
            import pdb; pdb.set_trace()
        
        if t not in sd:
            sd[t] = {
                'name': gstat['player'],
                'team': gstat['team'],
                'competition': gstat['competition'],
                'season': gstat['season'],
                'goals': gstat.get('goals'),
                'own_goals': gstat.get('own_goals'),
                'assists': gstat.get('assists'),
                'games_played': gstat.get('games_played'),
                'games_started': gstat.get('games_started'),
                'minutes': gstat.get('minutes'),
                }

        else:
            d = sd[t]
            for key in 'goals', 'own_goals', 'assists', 'games_played', 'games_started', 'minutes':
                if gstat.get(key) is not None:
                    d[key] = (d.get(key) or 0) + gstat[key]

    return sd



def generate_stats_old(goals=[], lineups=[]):
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
                return # No name on stat.

            sd[t] = {
                'name': name,
                'team': team,
                'season': season,
                'competition': competition,
                'goals': 0,
                'assists': None,
                'games_played': None,
                'games_started': None,
                'minutes': None,
                }

        # Increment the appropriate key.
        sd[t][key] = (sd[t].get(key) or 0) + amount


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


def generate_cities():
    print("Generating cities.")

    cities = set()

    for e in soccer_db.teams.find():
        if 'city' in e:
            cities.add(e['city'])


    for e in soccer_db.bios.find():
        cities.add(e.get('birthplace'))
        cities.add(e.get('deathplace'))


    # Probably can speed this up substantially
    for e in soccer_db.games.find():
        if 'location' in e:
            cities.add(e['location'])

    for e in soccer_db.stadiums.find():
        cities.add(e['location'])

    if None in cities:
        cities.remove(None)

    city_dicts = [{'name': city} for city in sorted(cities)]
    
    generic_load(soccer_db.cities, lambda: city_dicts)

    #return city_dicts

    

             
if __name__ == "__main__":
    generate()



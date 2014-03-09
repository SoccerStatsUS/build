# Can no longer build on server. Too much data, takes too long.
# Move this all over to Amazon. Taking too long to load here.
# Consider trimming down dramatically.
# Data quality is too low.

import functools
import os

from smid.alias.people import check_for_name_loops
from smid.alias.teams import check_for_team_loops, get_team
from smid.mongo import generic_load, soccer_db

from smid.settings import ROOT_DIR

from foulds.cache import data_cache, set_cache

GAMES_DIR = os.path.join(ROOT_DIR, "soccerdata/data/games")
STANDINGS_DIR = os.path.join(ROOT_DIR, "soccerdata/data/standings")


UEFA_DIR = os.path.join(ROOT_DIR, 'uefa-data')
NCAA_DIR = os.path.join(ROOT_DIR, 'ncaa-data')
NWSL_DIR = os.path.join(ROOT_DIR, 'nwsl-data')


def clear_all():
    """
    Clear all relevant mongo tables.
    """
    from smid.settings import STAT_TABLES, SOURCES, SINGLE_SOURCES
    for e in STAT_TABLES:
        soccer_db['%s' % e].drop()

    for s in SOURCES:
        for e in STAT_TABLES: 
            soccer_db['%s_%s' % (s, e)].drop()

    for e in SINGLE_SOURCES:
        soccer_db[e].drop()


def load_games_standard(coll, fn, games_only=False, root=GAMES_DIR):
    """
    Load standard data from a standard games file.
    """
    from donelli.parse import games

    print(fn)

    p = os.path.join(root, fn)
    games, goals, fouls, lineups, rosters = games.process_file(p)

    generic_load(soccer_db['%s_games' % coll], lambda: games, delete=False)

    if not games_only:
        generic_load(soccer_db['%s_lineups' % coll], lambda: lineups, delete=False)
        generic_load(soccer_db['%s_fouls' % coll], lambda: fouls, delete=False)
        generic_load(soccer_db['%s_goals' % coll], lambda: goals, delete=False)
        generic_load(soccer_db['%s_rosters' % coll], lambda: rosters, delete=False)


def load_standings_standard(coll, filename, delimiter=';', root=STANDINGS_DIR):
    """
    Load standard standings.
    """

    from donelli.parse import standings
    print(filename)

    path = os.path.join(root, filename)
    generic_load(soccer_db['%s_standings' % coll], lambda: standings.process_standings_file(path, delimiter))


def load():
    """
    Load everything.
    
    # House-cleaning
    Make sure that aliases don't have any cycles.
    Clear mongo database.

    # load background data
    - sources
    - competitions
    - places
    - teams
    - name maps (team,date->name)
    - stadium maps (team,date->stadium)
    - competition maps (competition,date->stadium)
    -? organizations

    # load personal info
    - biographical data
    - salaries
    - job information
    - drafts
    -? stats

    # load game data
    - currently loading games, standings, stats mixed.
    """

    check_for_name_loops()
    check_for_team_loops()
    clear_all()


    load_sources()
    load_place_data()

    load_competitions()

    load_transactions()

    load_teams()

    load_name_maps()
    load_stadium_maps()
    load_competition_maps()

    # short circuit bios
    #load_games(); return 

    load_bios()
    load_extra()

    load_games()


def load_transactions():

    from soccerdata.text import drafts

    generic_load(soccer_db.drafts, drafts.load_drafts)
    generic_load(soccer_db.picks, drafts.load_picks)

    load_jobs()


def load_extra():
    load_salaries()
    load_news()



def load_games():  
    load_domestic()


    load_international()

    load_women()
    load_other()




def load_international():

    load_world_international()

    load_uefa_international()
    load_conmebol_international()
    load_concacaf_international()
    load_oceania_international()

    load_asia_international()
    load_africa_international()



def load_domestic():
    load_nasl() 

    load_mls() 
    load_mexico()
    load_asl2()           
    load_us_minor()
    load_nafbl()
    load_canada()
    load_usa_cups()

    load_conmebol_leagues()


    load_asl()  


    load_conmebol()
    load_world()
    load_alpf()
    load_uncaf()
    load_concacaf()
    load_cfu()

    load_uefa()
    load_asia()
    load_uefa_leagues()
    #load_mediotiempo()    
    load_australia()    

    load_africa()

    # modern (mostly)
    load_oceania()

    # historical



def load_other():    
    load_ltrack()
    load_fifa()
    #load_ncaa()
    load_indoor()
    load_city()
    load_modern_friendlies()
    load_early_friendlies()

    load_ny()



def load_mediotiempo():
    from foulds.sites import mediotiempo

    games = mediotiempo.scrape_games(range(2000, 49000)) 

    generic_load(soccer_db['mediotiempo_games'], lambda: [e for e in games if e not in [{}, None]])
    #generic_load(soccer_db['mls2_goals'], lambda: [e for e in goals if e not in [{}, None]])
    #generic_load(soccer_db['mls2_lineups'], lambda: [e for e in lineups if e not in [{}, None]])



def load_excel_standings(coll, fn):
    """
    Load standard excel-formatted standings.
    """
    from donelli.parse import standings

    generic_load(soccer_db['%s_standings' % coll], lambda: standings.process_excel_standings(fn))


def load_sd_excel_standings(coll, fn):
    from donelli.parse import standings
    p = os.path.join(ROOT_DIR, 'soccerdata/data/standings/', fn)
    generic_load(soccer_db['%s_standings' % coll], lambda: standings.process_excel_standings(p))

            
def load_name_maps():
    from soccerdata.text import namemap
    generic_load(soccer_db.name_maps, namemap.load)


def load_competition_maps():
    from soccerdata.text import competitionnamemap
    generic_load(soccer_db.competition_maps, competitionnamemap.load)    


def load_stadium_maps():
    from soccerdata.text import stadiummap
    generic_load(soccer_db.stadium_maps, stadiummap.load)


def load_sources():
    from soccerdata.text import sources
    generic_load(soccer_db.sources, sources.load)


def load_news():
    from oneonta import feeds
    generic_load(soccer_db.news, feeds.parse_feeds)


def load_bios():

    from soccerdata.text import bios
    from foulds.sites import mlsnet, mlssoccer

    print("Loading ASL Bios")
    generic_load(soccer_db.asl_bios, bios.process_asl_bios)

    #print("Loading MLSsoccer.com player bios.")
    generic_load(soccer_db.mls_bios, mlssoccer.scrape_all_bios)

    #generic_load(soccer_db.mls_bios, mlsnet.scrape_2005_bios)
    generic_load(soccer_db.mls_bios, mlsnet.scrape_2001_bios)

    generic_load(soccer_db.fifa_bios, bios.process_world_cup_bios)
    generic_load(soccer_db.nasl_bios, bios.process_misl_bios)
    generic_load(soccer_db.nasl_bios, bios.process_nasl_bios)
    generic_load(soccer_db.usa_bios, bios.process_usa_bios)
    generic_load(soccer_db.mls_bios, bios.process_mls_bios)
    generic_load(soccer_db.mls_reserve_bios, bios.process_mls_reserve_bios)
    generic_load(soccer_db.asl_bios, bios.process_asl_bios2)
    generic_load(soccer_db.asl2_bios, bios.process_asl2_bios)
    generic_load(soccer_db.us_d2_bios, bios.process_ussf2_bios)
    generic_load(soccer_db.us_d2_bios, bios.process_nasl2_bios)
    generic_load(soccer_db.us_d2bios, bios.process_apsl_bios)

    generic_load(soccer_db.us_d2_bios, bios.process_usl1_bios)
    generic_load(soccer_db.us_d3_bios, bios.process_usl2_bios)

    generic_load(soccer_db.us_d4_bios, bios.process_pdl_bios)
    generic_load(soccer_db.us_d4_bios, bios.load_other_bios) 
    

def load_place_data():
    """
    Load place data.
    """
    from soccerdata.text import places
    generic_load(soccer_db.countries, places.load_countries)
    generic_load(soccer_db.states, places.load_states)
    generic_load(soccer_db.state_populations, places.load_state_populations)
    generic_load(soccer_db.stadiums, places.load_stadiums)


def load_usa_cups():

    from soccerdata.text import awards

    generic_load(soccer_db.us_cups_awards, awards.process_american_cup_awards)
    generic_load(soccer_db.us_cups_awards, awards.process_us_open_cup_awards, delete=False)
    generic_load(soccer_db.us_cups_awards, awards.process_lewis_cup_awards, delete=False)

    load_games_standard('us_cups', 'domestic/country/usa/cups/afa')
    load_games_standard('us_cups', 'domestic/country/usa/cups/afa2')
    load_games_standard('us_cups', 'domestic/country/usa/cups/lewis')
    load_games_standard('us_cups', 'domestic/country/usa/cups/duffy')
    load_games_standard('us_cups', 'domestic/country/usa/cups/aafa')

    for e in range(191, 202):
        load_games_standard('us_cups', 'domestic/country/usa/cups/open/%s0' % e)#, games_only=True)


def load_canada():
    from soccerdata.text import awards, partial

    load_standings_standard('canada', 'domestic/country/canada/csl1')
    load_standings_standard('canada', 'domestic/country/canada/cnsl')
    load_sd_excel_standings('canada', 'domestic/country/canada/csl')
    
    load_games_standard('canada', 'domestic/country/canada/cups/championship')
    load_games_standard('canada', 'domestic/country/canada/cups/early')

    load_games_standard('canada', 'domestic/country/canada/friendly/1')
    load_games_standard('canada', 'domestic/country/canada/friendly/friendly2')
    load_games_standard('canada', 'domestic/country/canada/friendly/toronto')
    load_games_standard('canada', 'domestic/country/canada/friendly/vancouver')

    generic_load(soccer_db.canada_stats, partial.process_csl_partial)

    generic_load(soccer_db.canada_awards, awards.process_csl_awards)
    generic_load(soccer_db.canada_awards, awards.process_canada_awards)


def load_uncaf():
    from soccerdata.text import awards

    generic_load(soccer_db.uncaf_awards, awards.process_uncaf_awards)
    generic_load(soccer_db.uncaf_awards, awards.process_guatemala_awards)
    generic_load(soccer_db.uncaf_awards, awards.process_honduras_awards)
    generic_load(soccer_db.uncaf_awards, awards.process_costa_rica_awards)
    generic_load(soccer_db.uncaf_awards, awards.process_elsalvador_awards)
    generic_load(soccer_db.uncaf_awards, awards.process_panama_awards)
    generic_load(soccer_db.uncaf_awards, awards.process_nicaragua_awards)

    load_standings_standard('uncaf', 'domestic/country/guatemala3')
    load_standings_standard('uncaf', 'domestic/country/elsalvador2')
    load_standings_standard('uncaf', 'domestic/country/honduras')
    load_standings_standard('uncaf', 'domestic/country/costarica2')
    load_standings_standard('uncaf', 'domestic/country/costarica3')
    load_standings_standard('uncaf', 'domestic/country/panama')
    load_standings_standard('uncaf', 'domestic/country/nicaragua')
    #load_standings_standard('uncaf', 'domestic/country/belize')
    
    for e in range(1996, 2013):
        load_games_standard('uncaf', 'domestic/country/guatemala/league/%s' % e)

    for e in range(1999, 2013):
        load_games_standard('uncaf', 'domestic/country/el_salvador/%s' % e)

    load_games_standard('uncaf', 'domestic/country/el_salvador/torneo')

    for e in range(2000, 2013):
        load_games_standard('uncaf', 'domestic/country/honduras/%s' % e)

    for e in range(2003, 2013):
        load_games_standard('uncaf', 'domestic/country/costa_rica/league/%s' % e)

    for e in range(2000, 2013):
        load_games_standard('uncaf', 'domestic/country/panama/%s' % e)


    load_games_standard('uncaf', 'domestic/confederation/concacaf/uncaf/fraternidad')
    load_games_standard('uncaf', 'domestic/confederation/concacaf/uncaf/torneograndes')
    load_games_standard('uncaf', 'domestic/confederation/concacaf/uncaf/interclube')



def load_uefa():
    for e in range(1955, 1992):
        load_games_standard('uefa', 'domestic/confederation/uefa/champions/%s' % e)

    load_games_standard('uefa', 'domestic/confederation/uefa/super')



def load_uefa_leagues():
    from soccerdata.text import awards

    generic_load(soccer_db.uefa_awards, awards.process_uefa_awards)
    generic_load(soccer_db.uefa_awards, awards.process_england_awards)

    load_uefa_major()
    load_uefa_mid()
    load_scandinavia()

    load_uefa_minor()



def load_africa():
    from soccerdata.text import awards

    #load_standings_standard('uefa', 'domestic/country/tunisia')
    #load_standings_standard('uefa', 'domestic/country/egypt')
    #load_standings_standard('uefa', 'domestic/country/algeria')
    #load_standings_standard('uefa', 'domestic/country/morocco')
    #load_standings_standard('uefa', 'domestic/country/south_africa')
    #load_standings_standard('uefa', 'domestic/country/nigeria')
    #load_standings_standard('uefa', 'domestic/country/cameroon')
    #load_standings_standard('uefa', 'domestic/country/ghana')
    #load_standings_standard('uefa', 'domestic/country/sudan')
    #load_standings_standard('uefa', 'domestic/country/congo_dr')
    #load_standings_standard('uefa', 'domestic/country/angola')
    #load_standings_standard('uefa', 'domestic/country/cote_divoire')
    #load_standings_standard('uefa', 'domestic/country/libya')
    #load_standings_standard('uefa', 'domestic/country/zimbabwe')

    for year in range(2013, 2013):
        load_games_standard('uefa', 'domestic/country/tunisia/men/%s' % year)

    for year in range(2013, 2013):
        load_games_standard('uefa', 'domestic/country/egypt/men/%s' % year)

    for year in range(2013, 2013):
        load_games_standard('uefa', 'domestic/country/algeria/men/%s' % year)

    for year in range(2013, 2013):
        load_games_standard('uefa', 'domestic/country/south_africa/men/%s' % year)



def load_premier_league():
    from foulds.sites import premierleague
    generic_load(soccer_db.epl_games, premierleague.scrape_calendars)


def load_uefa_major():

    #load_premier_league()

    load_standings_standard('uefa', 'domestic/country/italy')
    load_standings_standard('uefa', 'domestic/country/spain')
    load_standings_standard('uefa', 'domestic/country/france')
    load_standings_standard('uefa', 'domestic/country/germany')
    load_standings_standard('uefa', 'domestic/country/england')
    
    # england
    for year in range(1992, 2009):
        load_games_standard('uefa', 'games/%s' % year, root=UEFA_DIR)

    for year in range(1999, 2013):
        load_games_standard('uefa', 'domestic/country/germany/men/%s' % year)

    for year in range(1998, 2012):
        load_games_standard('uefa', 'domestic/country/france/%s' % year)

    for year in range(1997, 2013):
        load_games_standard('uefa', 'domestic/country/spain/%s' % year)

    for year in range(1996, 2013):
        load_games_standard('uefa', 'domestic/country/italy/%s' % year)

    return
    load_games_standard('mexico', 'domestic/country/spain/friendly/madrid')



def load_uefa_mid():

    load_standings_standard('uefa', 'domestic/country/netherlands')
    load_standings_standard('uefa', 'domestic/country/belgium')
    load_standings_standard('uefa', 'domestic/country/turkey')
    load_standings_standard('uefa', 'domestic/country/russia')
    load_standings_standard('uefa', 'domestic/country/ukraine')
    load_standings_standard('uefa', 'domestic/country/portugal')


    for year in range(1996, 2011):
        load_games_standard('uefa', 'domestic/country/netherlands/%s' % year)

    for year in range(1997, 2010):
        load_games_standard('uefa', 'domestic/country/turkey/%s' % year)

    for year in range(1998, 2011):
        load_games_standard('uefa', 'domestic/country/portugal/%s' % year)

    for year in range(1997, 2010):
        load_games_standard('uefa', 'domestic/country/belgium/%s' % year)

    for year in range(2003, 2012):
        load_games_standard('uefa', 'domestic/country/russia/%s' % year)


    for year in range(2006, 2012):
        load_games_standard('uefa', 'domestic/country/ukraine/%s' % year)


def load_scandinavia():

    load_standings_standard('uefa', 'domestic/country/denmark')
    load_standings_standard('uefa', 'domestic/country/sweden')
    load_standings_standard('uefa', 'domestic/country/norway')
    #load_standings_standard('uefa', 'domestic/country/finland')
    #load_standings_standard('uefa', 'domestic/country/iceland')

    for year in range(1997, 2012):
        load_games_standard('uefa', 'domestic/country/denmark/%s' % year)

    for year in range(1999, 2012):
        load_games_standard('uefa', 'domestic/country/norway/%s' % year)

    for year in range(2001, 2012):
        load_games_standard('uefa', 'domestic/country/sweden/%s' % year)

    for year in range(2012, 2012):
        load_games_standard('uefa', 'domestic/country/finland/%s' % year)

    for year in range(2012, 2012):
        load_games_standard('uefa', 'domestic/country/iceland/%s' % year)


def load_uefa_minor():

    load_standings_standard('uefa', 'domestic/country/switzerland')
    load_standings_standard('uefa', 'domestic/country/scotland2')
    load_standings_standard('uefa', 'domestic/country/austria2')
    load_standings_standard('uefa', 'domestic/country/poland')
    


    #load_standings_standard('uefa', 'domestic/country/czech')
    load_standings_standard('uefa', 'domestic/country/romania')
    #load_standings_standard('uefa', 'domestic/country/serbia')
    #load_standings_standard('uefa', 'domestic/country/croatia')

    #load_standings_standard('uefa', 'domestic/country/bosnia')
    #load_standings_standard('uefa', 'domestic/country/slovakia')
    #load_standings_standard('uefa', 'domestic/country/slovenia')

    #load_standings_standard('uefa', 'domestic/country/greece')
    #load_standings_standard('uefa', 'domestic/country/cyprus')

    #load_standings_standard('uefa', 'domestic/country/hungary2')
    #load_standings_standard('uefa', 'domestic/country/bulgaria')
    #load_standings_standard('uefa', 'domestic/country/ireland')
    #load_standings_standard('uefa', 'domestic/country/wales')

    for year in range(1996, 2010):
        load_games_standard('uefa', 'domestic/country/poland/%s' % year)

    for year in range(1998, 2013):
        load_games_standard('uefa', 'domestic/country/scotland/%s' % year)

    for year in range(1997, 2010):
        load_games_standard('uefa', 'domestic/country/switzerland/%s' % year)

    for year in range(1998, 2011):
        load_games_standard('uefa', 'domestic/country/austria/%s' % year)

    return

    for year in range(1997, 2012):
        load_games_standard('uefa', 'domestic/country/romania/%s' % year)

    for year in range(1997, 2013):
        load_games_standard('uefa', 'domestic/country/czech/%s' % year)

    return

    for year in range(2008, 2011):
        load_games_standard('uefa', 'domestic/country/serbia/%s' % year)

    for year in range(2012, 2013):
        load_games_standard('uefa', 'domestic/country/croatia/%s' % year)


    return

    for year in range(2013, 2013):
        load_games_standard('uefa', 'domestic/country/bosnia/%s' % year)

    for year in range(2012, 2013):
        load_games_standard('uefa', 'domestic/country/slovenia/%s' % year)

    for year in range(2012, 2013):
        load_games_standard('uefa', 'domestic/country/slovakia/%s' % year)

    return

    for year in range(2005, 2012):
        load_games_standard('uefa', 'domestic/country/greece/%s' % year)

    for year in range(2012, 2013):
        load_games_standard('uefa', 'domestic/country/cyprus/%s' % year)

    return

    for year in range(1998, 2013):
        load_games_standard('uefa', 'domestic/country/hungary/%s' % year)

    for year in range(2010, 2014):
        load_games_standard('uefa', 'domestic/country/ireland/%s' % year)

    for year in range(2012, 2012):
        load_games_standard('uefa', 'domestic/country/bulgaria/%s' % year)


def load_conmebol_leagues():
    load_conmebol_minor()
    load_brazil()
    load_argentina()

def load_conmebol_minor():
    from soccerdata.text import awards

    generic_load(soccer_db.conmebol_awards, awards.process_conmebol_league_awards)

    load_standings_standard('conmebol', 'domestic/country/uruguay2')
    load_standings_standard('conmebol', 'domestic/country/chile2')

    load_standings_standard('conmebol', 'domestic/country/colombia3')

    load_standings_standard('conmebol', 'domestic/country/ecuador')

    load_standings_standard('conmebol', 'domestic/country/peru')
    load_standings_standard('conmebol', 'domestic/country/paraguay')
    load_standings_standard('conmebol', 'domestic/country/bolivia')

    #load_standings_standard('conmebol', 'domestic/country/venezuela')
    #load_standings_standard('conmebol', 'domestic/country/colombia2')
    #load_standings_standard('conmebol', 'domestic/country/colombia')
    #load_standings_standard('conmebol', 'domestic/country/chile')
    #load_standings_standard('conmebol', 'domestic/country/uruguay')


    for year in range(1996, 2012):
        load_games_standard('conmebol', 'domestic/country/uruguay/%s' % year)

    for year in range(1996, 2014):
        load_games_standard('conmebol', 'domestic/country/chile/%s' % year)

    for year in range(1997, 2011):
        load_games_standard('conmebol', 'domestic/country/colombia/%s' % year)

    for year in range(1996, 2014):
        load_games_standard('conmebol', 'domestic/country/ecuador/%s' % year)

    for year in range(1996, 2012):
        load_games_standard('conmebol', 'domestic/country/peru/%s' % year)

    for year in range(1996, 2013):
        load_games_standard('conmebol', 'domestic/country/bolivia/%s' % year)

    for year in range(1997, 2013):
        load_games_standard('conmebol', 'domestic/country/paraguay/%s' % year)

    for year in range(2012, 2012):
        load_games_standard('conmebol', 'domestic/country/venezuela/%s' % year)


def load_argentina():
    from soccerdata.text import awards

    generic_load(soccer_db.conmebol_awards, awards.process_argentina_awards)
    #load_standings_standard('conmebol', 'domestic/country/argentina2')
    load_standings_standard('conmebol', 'domestic/country/argentina')

    for year in range(1967, 1985):
        load_games_standard('conmebol', 'domestic/country/argentina/city/%s' % year)

    for year in range(1932, 2011):
        load_games_standard('conmebol', 'domestic/country/argentina/leagues/%s' % year)


def load_brazil():
    from soccerdata.text import awards

    load_standings_standard('conmebol', 'domestic/country/brazil')

    generic_load(soccer_db.conmebol_awards, awards.process_brazil_awards)

    for e in range(1971, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/brasileiro/%s' % e)


    # state leagues.

    for year in range(1905, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/paulista/%s' % year)

    for year in range(1946, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/carioca/%s' % year)

    for year in range(1915, 1917):
        load_games_standard('brazil', 'domestic/country/brazil/minas_gerais/%s' % year)

    for year in range(2006, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/minas_gerais/%s' % year)

    #for year in range(2011, 2013):
    #    load_games_standard('brazil', 'domestic/country/brazil/gaucho/%s' % year)

    return

    for year in range(2011, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/bahia/%s' % year)

    for year in range(2013, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/pernambuco/%s' % year)

    for year in range(2013, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/parana/%s' % year)

    return

    for year in range(2013, 2013):
        load_games_standard('brazil', 'domestic/country/brazil/santacatarina/%s' % year)


    load_games_standard('brazil', 'domestic/country/brazil/friendly/botafogo')


def load_brazil_international():

    for e in ['1906', '1914', '1923', '1934', '1939']:
        load_games_standard('brazil', 'international/country/brazil/%s' % e)



def load_women():
    from soccerdata.text import awards, stats

    generic_load(soccer_db.women_awards, awards.process_women_awards)

    WOMEN_ROOT = os.path.join(NWSL_DIR, 'data/games')

    load_games_standard('women', 'wusa', root=WOMEN_ROOT)
    load_games_standard('women', 'nwsl', root=WOMEN_ROOT)
    load_games_standard('women', 'wps', root=WOMEN_ROOT)
    load_games_standard('women', 'wpsl_elite', root=WOMEN_ROOT)

    generic_load(soccer_db.women_stats, stats.process_nwsl_stats)
    
    for e in ['wusa', 'wps', 'wpsl_elite', 'nwsl']:
        r = os.path.join(ROOT_DIR, 'nwsl-data/data/standings')
        load_standings_standard('women', e, root=r)

    generic_load(soccer_db.women_rosters, lambda: flatten_lineups(soccer_db.women_lineups.find({'competition': 'Women\'s United Soccer Association'})))

    #for e in range(2007, 2013):
    #    load_games_standard('women', 'domestic/country/usa/leagues/women/wpsl/%s' % e)



def load_mlssoccer_season(url, competition):
    from foulds.sites.mlssoccer import scrape_competition

    games, goals, lineups = scrape_competition(url, competition)

    generic_load(soccer_db['mls2_games'], lambda: [e for e in games if e not in [{}, None]])
    generic_load(soccer_db['mls2_goals'], lambda: [e for e in goals if e not in [{}, None]])
    generic_load(soccer_db['mls2_lineups'], lambda: [e for e in lineups if e not in [{}, None]])


def load_mls():
    from soccerdata.text import awards, stats

    generic_load(soccer_db.mls_awards, awards.process_mls_awards)

    load_standings_standard('mls', 'domestic/country/usa/mls')

    # Add rsssf games.
    for e in range(2001, 2001):
        r = os.path.join(ROOT_DIR, 'usd1/data/games/league/rsssf/%s' % e)
        load_games_standard('mls3', str(e), root=r)


    print("Loading MLS reserves data.")
    for e in [2005, 2006, 2007, 2008, 2011, 2012, 2013]:
        load_games_standard('mls', 'domestic/country/usa/leagues/reserve/mls/%s' % e)


    for e in ['1996.2010', '2011', '2012', '2013']:
        r = os.path.join(ROOT_DIR, 'usd1/data/games/league/simple/mls')
        load_games_standard('mls', str(e), root=r)


    load_games_standard('mls', os.path.join(ROOT_DIR, 'usd1/data/games/playoffs/mls'))

    # Not loading 1996-2011 stats?
    generic_load(soccer_db.mls_stats, stats.process_mls_2012_stats)
    generic_load(soccer_db.mls_stats, stats.process_mls_2013_stats)

    load_mls_lineup_db()

    u = 'http://www.mlssoccer.com/schedule?month=all&year=%s&club=all&competition_type=%s&broadcast_type=all&op=Search&form_id=mls_schedule_form'

    #for year in (2011, 2012, 2013):
    for year in (2013,):
        load_mlssoccer_season(u % (year, 46), 'Major League Soccer')
        load_mlssoccer_season(u % (year, 45), 'MLS Cup Playoffs')
        load_mlssoccer_season(u % (year, 44), 'MLS Cup Playoffs')

    generic_load(soccer_db.mls_rosters, lambda: flatten_stats(soccer_db.mls_stats.find()))


def load_nafbl():
    from soccerdata.text import awards

    # Also loading ALPF and SNESL
    generic_load(soccer_db.asl_awards, awards.process_nafbl_awards, delete=False)
    generic_load(soccer_db.asl_awards, awards.process_snesl_awards, delete=False)

    #load_sd_excel_standings('nafbl', 'domestic/country/usa/early')

    load_games_standard('nafbl', 'domestic/country/usa/leagues/regional/nafbl1')
    load_games_standard('nafbl', 'domestic/country/usa/leagues/regional/nafbl2')
    load_games_standard('nafbl', 'domestic/country/usa/leagues/regional/snesl')
    load_games_standard('nafbl', 'domestic/country/usa/leagues/regional/nasfl')
    load_games_standard('nafbl', 'domestic/country/usa/leagues/misc/isl') # ISL 1925?



def load_city():
    from soccerdata.text import awards

    #load_games_standard('city', 'city')
    load_sd_excel_standings('city', 'domestic/city/slsl')
    load_sd_excel_standings('city', 'domestic/city/cosmo')
    #generic_load(soccer_db.city_awards, awards.process_chicago_awards, delete=False)


def load_ny():
    from soccerdata.text import awards

    load_games_standard('state', 'domestic/country/usa/leagues/regional/metropolitan')
    load_games_standard('state', 'domestic/country/usa/friendly/1900_ny')
    generic_load(soccer_db.state_awards, awards.process_ny_awards, delete=False)


def load_early_friendlies():

    for e in range(1865, 1891, 5):
        load_games_standard('us_friendly', 'domestic/country/usa/friendly/%s' % e)

    for e in range(1900, 1951, 10):
        load_games_standard('us_friendly', 'domestic/country/usa/friendly/%s' % e)


def load_modern_friendlies():

    load_games_standard('us_friendly', 'international/misc/bicentennial')

    load_games_standard('us_friendly', 'domestic/country/usa/friendly/carolina')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/dynamo')

    load_games_standard('us_friendly', 'domestic/country/usa/friendly/1960')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/1967')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/1970')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/1980')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/tours/1970')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/tours/1980')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/1990')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/2000')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/2010')

    # All-Star game.
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/mls_all_star')

    # Premium tournaments (superclubs)
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/wfc')
    load_games_standard('us_friendly', 'domestic/country/usa/friendly/icc')


def load_competitions():
    from soccerdata.text import competitions, seasons
    print("Loading competitions.")
    generic_load(soccer_db.competitions, competitions.load_competitions)
    generic_load(soccer_db.seasons, seasons.load_seasons)


def load_teams():
    from soccerdata.text import teams
    print("Loading teams.")
    generic_load(soccer_db.teams, teams.load)


def load_salaries():
    from soccerdata.text import salaries

    generic_load(soccer_db.salaries, salaries.load_salaries)


def load_jobs():
    from soccerdata.text import positions, p2
    print("Loading positions.")

    jobs = os.path.join(ROOT_DIR, 'soccerdata/data/jobs/')
    

    f1 = lambda: p2.process_file(os.path.join(jobs, 'world/england'), 'Head Coach')
    f2 = lambda: p2.process_file(os.path.join(jobs, 'usa/d1/mls/head'), 'Head Coach', delimiter=';')

    #generic_load(soccer_db.positions, positions.process_positions)
    generic_load(soccer_db.positions, f1)
    generic_load(soccer_db.positions, f2)


def load_copa_america():
    from soccerdata.text import rosters
    from soccerdata.text.cmp import copaamerica

    coll = 'conmebol_i'
    games, goals, fouls, lineups = copaamerica.process_copa_files()

    generic_load(soccer_db['%s_games' % coll], lambda: games, delete=False)
    generic_load(soccer_db['%s_lineups' % coll], lambda: lineups, delete=False)
    generic_load(soccer_db['%s_fouls' % coll], lambda: fouls, delete=False)
    generic_load(soccer_db['%s_goals' % coll], lambda: goals, delete=False)

    generic_load(soccer_db.conmebol_i_rosters, lambda: rosters.process_rosters('international/copa_america'))
    load_games_standard('conmebol_i', 'international/confederation/conmebol/copa_america/stadia')

    
def load_asl():
    from usd1.parse import asl
    from soccerdata.text import awards

    generic_load(soccer_db.asl_awards, awards.process_asl_awards, delete=False)
    generic_load(soccer_db.asl_awards, awards.process_esl_awards, delete=False)

    DIR = os.path.join(ROOT_DIR, 'usd1/data')

    #load_excel_standings('asl', os.path.join(DIR, 'standings/asl')) # delete?
    load_standings_standard('asl', 'standings/asl2', root=DIR)

    # Colin Jose data
    generic_load(soccer_db.asl_goals, asl.process_asl_goals)
    generic_load(soccer_db.asl_stats, asl.process_stats)
    generic_load(soccer_db.asl_games, asl.process_asl_games)

    load_games_standard('asl', os.path.join(DIR, 'games/league/simple/asl'))
    load_games_standard('asl', os.path.join(DIR, 'games/league/simple/esl'))

    generic_load(soccer_db.asl_rosters, lambda: flatten_stats(soccer_db.asl_stats.find()))


def load_alpf():
    load_games_standard('alpf', os.path.join(ROOT_DIR, 'usd1/data/games/league/simple/alpf'))
    load_standings_standard('alpf', 'alpf', root=os.path.join(ROOT_DIR, 'usd1/data/standings'))


def load_asl2():
    from soccerdata.text import awards, partial, rosters

    generic_load(soccer_db.asl2_awards, awards.process_asl2_awards, delete=False)
    generic_load(soccer_db.asl2_stats, partial.process_asl2_partial)

    generic_load(soccer_db.conmebol_i_rosters, lambda: rosters.process_rosters2('domestic/asl2'))

    load_sd_excel_standings('asl2', 'domestic/country/usa/asl2')
    load_games_standard('asl2', 'domestic/country/usa/leagues/d2/asl2')


def load_nasl():
    """
    Load stats from the old nasl and misl.
    """

    from soccerdata.text import awards, rosters, stats
    generic_load(soccer_db.nasl_awards, awards.process_nasl_awards)
    generic_load(soccer_db.nasl_awards, awards.process_usa_awards)
    generic_load(soccer_db.nasl_awards, awards.process_npsl_awards)
    generic_load(soccer_db.nasl_rosters, lambda: rosters.process_rosters2(os.path.join(ROOT_DIR, 'usd1/data/rosters/nasl')))
    generic_load(soccer_db.nasl_stats, stats.process_nasl_stats)


    from usd1.parse import nasl

    DIR = os.path.join(ROOT_DIR, 'usd1/data/')
    GDIR = os.path.join(DIR, 'games')

    print("Loading NASL data.")
    load_excel_standings('nasl', os.path.join(DIR, 'standings/nasl'))
    load_excel_standings('nasl', os.path.join(DIR, 'standings/nasl0'))

    load_games_standard('nasl', 'playoffs/nasl', root=GDIR)

    generic_load(soccer_db.nasl_games, nasl.process_npsl_games)
    generic_load(soccer_db.nasl_goals, nasl.process_npsl_goals)
    load_games_standard('nasl', 'league/simple/usa', root=GDIR)

    # Need to work some integrity issues on games.
    generic_load(soccer_db.nasl_games, nasl.process_nasl_games)
    generic_load(soccer_db.nasl_goals, nasl.process_nasl_goals)
    generic_load(soccer_db.nasl_lineups, nasl.process_nasl_lineups)


def load_apsl():
    """
    Load stats and games from the APSL and WSA.
    """
    from soccerdata.text import awards, partial
    from soccerdata.text.cmp import apsl

    print("loading apsl stats")
    apsl_stats = apsl.process_apsl_stats()

    # lambdas...
    generic_load(soccer_db.us_d2_stats, apsl_stats)
    generic_load(soccer_db.us_d2_rosters, flatten_stats(apsl_stats))

    print("loading apsl partial stats")
    generic_load(soccer_db.us_d2_stats, partial.process_apsl_partial)

    generic_load(soccer_db.us_d2_awards, awards.process_apsl_awards)

    load_sd_excel_standings('us_d2', 'domestic/country/usa/apsl')



    # Test these
    #load_standings_standard('us_d2', 'domestic/country/usa/wsa')
    #load_standings_standard('us_d2', 'domestic/country/usa/lssa')

    
    #print("loading apsl scores")
    #generic_load(soccer_db.us_d2_games, apsl.process_apsl_scores)
    #load_games_standard('us_d2', 'domestic/country/usa/leagues/wsa3')

    load_games_standard('us_d2', 'domestic/country/usa/leagues/d2/apsl')
    load_games_standard('us_d2', 'domestic/country/usa/leagues/d3/wsa4')

    load_games_standard('us_d2', 'domestic/country/usa/playoffs/apsl')
    load_games_standard('us_d2', 'domestic/country/usa/playoffs/wsa')
    load_games_standard('us_d2', 'domestic/country/usa/cups/apsl_professional')


def load_indoor():
    """
    Load stats and games from the MISL, standings from MISL, APSL and WSA.
    """
    from soccerdata.text import stats

    load_sd_excel_standings('indoor', 'indoor/all')
    load_sd_excel_standings('indoor', 'indoor/misl')

    #print("Loading MISL stats.")
    #generic_load(soccer_db.indoor_stats, stats.process_misl_stats)



def load_mls_lineup_db():
    from usd1.parse import lineupdb
    # MLS lineup data 1996-2010 from http://usasoccer.blogspot.com/

    print("Loading scaryice score data.")
    generic_load(soccer_db.mls_games, lineupdb.load_all_games_scaryice)

    print("Loading scaryice goal data.")
    generic_load(soccer_db.mls_goals, lineupdb.load_all_goals_scaryice)
    
    print( "Loading scaryice lineup data.")
    generic_load(soccer_db.mls_lineups, lineupdb.load_all_lineups_scaryice)


def load_pdl():
    from soccerdata.text.cmp import pdl
    from soccerdata.text import awards, stats

    load_sd_excel_standings('us_d4', 'domestic/country/usa/usl/pdl')
    generic_load(soccer_db.us_d4_awards, awards.process_pdl_awards)
    generic_load(soccer_db.us_d4_stats, stats.process_pdl_stats)
    generic_load(soccer_db.us_d4_games, pdl.load_pdl_games)

    load_standings_standard('us_d2', 'domestic/country/usa/usl/pdl_2012')
    load_standings_standard('us_d2', 'domestic/country/usa/usl/pdl_2013')


def load_us_minor():
    """
    Load usl stats and nasl stats.
    """

    from foulds.sites import nasl, uslsoccer
    from soccerdata.text import awards, stats
    from soccerdata.text.cmp import nasl2


    load_apsl()
    load_pdl()

    generic_load(soccer_db.us_d2_stats, nasl2.process_stats)

    generic_load(soccer_db.us_d2_awards, awards.process_usl_awards)
    generic_load(soccer_db.us_d2_awards, awards.process_ussf2_awards)
    generic_load(soccer_db.us_d2_awards, awards.process_nasl2_awards)

    #generic_load(soccer_db['us_lower_games'], uslsoccer.scrape_2013_games) 
    #generic_load(soccer_db['us_lower_goals'], uslsoccer.scrape_2013_goals)
    #generic_load(soccer_db['us_lower_gstats'], uslsoccer.scrape_2013_game_stats) # Fix stat generation

    #generic_load(soccer_db['us_lower_games'], nasl.scrape_all_games)
    #generic_load(soccer_db['us_lower_goals'], nasl.scrape_all_goals)
    #generic_load(soccer_db['us_lower_gstats'], nasl.scrape_all_game_stats)
             
    # Division 2
    generic_load(soccer_db.us_d2_stats, stats.process_usl1_stats)
    generic_load(soccer_db.us_d2_stats, stats.process_usl2_stats)

    load_sd_excel_standings('us_d2', 'domestic/country/usa/usl/12') # split

    load_standings_standard('us_d2', 'domestic/country/usa/usl/usl0')
    load_standings_standard('us_d2', 'domestic/country/usa/ussf2')
    load_standings_standard('us_d2', 'domestic/country/usa/nasl2')

    load_games_standard('us_d2', 'domestic/country/usa/leagues/d2/usl1')
    load_games_standard('us_d2', 'domestic/country/usa/leagues/d2/ussfd2')
    load_games_standard('us_d2', 'domestic/country/usa/leagues/d2/nasl/2011')
    load_games_standard('us_d2', 'domestic/country/usa/leagues/d2/nasl/2012')
    load_games_standard('us_d2', 'domestic/country/usa/leagues/d2/nasl/2013')

    load_games_standard('us_d2', 'domestic/country/usa/playoffs/usl1')
    load_games_standard('us_d2', 'domestic/country/usa/playoffs/nasl2')

    # Division 3
    load_sd_excel_standings('us_d3', 'domestic/country/usa/usl/pro') # 2 or 3?
    load_sd_excel_standings('us_d3', 'domestic/country/usa/usl/premier')

    load_sd_excel_standings('us_d3', 'domestic/country/usa/usl/usisl')

    load_standings_standard('us_d3', 'domestic/country/usa/usl/usl_pro')
    load_standings_standard('us_d3', 'domestic/country/usa/usl/select') # 2 or 3?

    for e in range(2003, 2014):
        load_games_standard('us_d3', 'domestic/country/usa/leagues/d3/%s' % e)
    load_games_standard('us_d3', 'domestic/country/usa/playoffs/usl2')



def load_asia():

    #load_standings_standard('china', 'domestic/country/iran')
    #load_standings_standard('china', 'domestic/country/iraq')
    #load_standings_standard('china', 'domestic/country/saudi_arabia')
    #load_standings_standard('china', 'domestic/country/qatar')
    #load_standings_standard('china', 'domestic/country/uae')
    #load_standings_standard('china', 'domestic/country/uzbekistan')

    #load_standings_standard('china', 'domestic/country/india')

    for e in range(2009, 2013):
        load_games_standard('japan', 'domestic/country/iran/%s' % e)

    for e in range(2012, 2013):
        load_games_standard('japan', 'domestic/country/iran/%s' % e)

    load_east_asia()

def load_east_asia():
    from soccerdata.text import awards

    load_standings_standard('china', 'domestic/country/china')
    load_standings_standard('japan', 'domestic/country/japan')
    load_standings_standard('korea', 'domestic/country/korea')

    #load_standings_standard('korea', 'domestic/country/thailand')
    #load_standings_standard('korea', 'domestic/country/vietnam')
    #load_standings_standard('korea', 'domestic/country/indonesia')

    generic_load(soccer_db.china_awards, awards.process_china_awards)
    generic_load(soccer_db.japan_awards, awards.process_japan_awards)
    generic_load(soccer_db.korea_awards, awards.process_korea_awards)

    for e in range(2004, 2013):
        load_games_standard('china', 'domestic/country/china/league/%s' % e)

    for e in range(1997, 2011):
        load_games_standard('japan', 'domestic/country/japan/%s' % e)

    for e in range(1983, 2011):
        load_games_standard('korea', 'domestic/country/korea/%s' % e)


def load_australia():
    from soccerdata.text import awards

    generic_load(soccer_db.australia_awards, awards.process_australia_awards)

    load_standings_standard('australia', 'domestic/country/australia')

    for season in range(2005, 2013):
        load_games_standard('australia', 'domestic/country/australia/league/%s' % season)

    load_games_standard('australia', 'domestic/country/australia/playoffs')

    return
    from foulds.sites.australia import scrape_aleague

    games, goals, lineups = scrape_aleague()
    generic_load(soccer_db['australia_games'], lambda: [e for e in games if e not in [{}, None]])
    generic_load(soccer_db['australia_goals'], lambda: [e for e in goals if e not in [{}, None]])
    generic_load(soccer_db['australia_lineups'], lambda: [e for e in lineups if e not in [{}, None]])



def load_mexico():
    from soccerdata.text import awards

    generic_load(soccer_db.mexico_awards, awards.process_mexico_awards)

    load_standings_standard('mexico', 'domestic/country/mexico/1', ';')
    load_standings_standard('mexico', 'domestic/country/mexico/short', ';')
    #load_standings_standard('mexico', 'domestic/country/mexico/primera_fuerza')

    for e in range(1970, 2013):
        load_games_standard('mexico', 'domestic/country/mexico/league/%s' % e)

    for e in range(2012, 2013):
        load_games_standard('mexico', 'domestic/country/mexico/ascenso/%s' % e)

    for e in range(1970, 2020, 10):
        load_games_standard('mexico', 'domestic/country/mexico/playoffs/%s' % e)

        
    return

    # league
    load_games_standard('mexico', 'domestic/country/mexico/league/1943')
    load_games_standard('mexico', 'domestic/country/mexico/league/1963')
    load_games_standard('mexico', 'domestic/country/mexico/league/1964')
    load_games_standard('mexico', 'domestic/country/mexico/league/1967')
    load_games_standard('mexico', 'domestic/country/mexico/league/1970mexico')


    # Cups
    load_games_standard('mexico', 'domestic/country/mexico/interliga')
    load_games_standard('mexico', 'domestic/country/mexico/pre_libertadores')
    load_games_standard('mexico', 'domestic/country/mexico/super')

    # Friendlies.
    load_games_standard('mexico', 'domestic/country/mexico/friendly/adolfo_lopez_mateos')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/agosto')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/chiapas')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/corona')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/gol')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/guadalajara')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/guadalajara2')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/guadalajara3')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/hidalgo')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/leon')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/mesoamericana')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/mexico_city')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/mexico_city2')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/milenio')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/monterrey')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/nike')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/pentagonal2')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/puebla')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/quadrangular')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/queretaro')

    load_games_standard('mexico', 'domestic/country/mexico/friendly/tijuana')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/toluca')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/torreon')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/tour')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/universidades')
    load_games_standard('mexico', 'domestic/country/mexico/friendly/veracruz')


def load_oceania():
    load_games_standard('oceania', 'domestic/confederation/ofc/wantok')


def load_oceania_international():

    for e in range(1986, 2018, 4):
        load_games_standard('oceania_i', 'international/confederation/ofc/wcq/%s' % e)

    load_games_standard('oceania_i', 'international/confederation/ofc/melanesia')
    load_games_standard('oceania_i', 'international/confederation/ofc/polynesia')
    load_games_standard('oceania_i', 'international/confederation/ofc/nations')


def load_uefa_international():
    load_games_standard('uefa_i', 'international/country/france')
    #load_games_standard('uefa_i', 'international/country/slovenia')

    #load_games_standard('uefa_i', 'international/country/netherlands')
    #load_games_standard('uefa_i', 'international/country/belgium')
    #load_games_standard('uefa_i', 'international/country/austria')
    #load_games_standard('uefa_i', 'international/country/hungary')

    return

    load_games_standard('uefa_i', 'international/country/germany')
    load_games_standard('uefa_i', 'international/country/spain')
    load_games_standard('uefa_i', 'international/country/italy')
    load_games_standard('uefa_i', 'international/country/sweden')
    load_games_standard('uefa_i', 'international/country/norway')
    load_games_standard('uefa_i', 'international/country/denmark')
    load_games_standard('uefa_i', 'international/country/portugal')



def load_asia_international():
    return
    load_games_standard('afc_i', 'international/country/south_korea')
    load_games_standard('afc_i', 'international/country/north_korea')

    for e in range(195, 201):
        load_games_standard('afc_i', 'international/country/japan/%s0' % e)


def load_africa_international():
    return
    load_games_standard('caf_i', 'international/country/nigeria')
    load_games_standard('caf_i', 'international/country/cameroon')
    load_games_standard('caf_i', 'international/country/ghana')


def load_mixed_confederation():

    load_games_standard('world', 'domestic/confederation/mixed/panpacific')
    load_games_standard('world', 'domestic/confederation/mixed/interamerican')
    load_games_standard('world', 'domestic/confederation/mixed/suruga')

    for e in [1960, 1970, 1980, 1990, 2000]:
        load_games_standard('world', 'domestic/confederation/mixed/intercontinental/%s' % e)



def load_conmebol():
    from soccerdata.text import awards

    generic_load(soccer_db.conmebol_awards, awards.process_conmebol_awards)

    for e in range(1960, 2014):
        load_games_standard('conmebol', 'domestic/confederation/conmebol/libertadores/%s' % e)

    load_games_standard('conmebol', 'domestic/confederation/conmebol/recopa_sudamericana')
    load_games_standard('conmebol', 'domestic/confederation/conmebol/sacc')

    load_games_standard('conmebol', 'domestic/confederation/conmebol/merconorte')
    load_games_standard('conmebol', 'domestic/confederation/conmebol/mercosur')
    load_games_standard('conmebol', 'domestic/confederation/conmebol/mercosul')

    for e in range(1992, 2000):
        load_games_standard('conmebol', 'domestic/confederation/conmebol/conmebol/%s' % e)

    for e in range(2002, 2013):
        load_games_standard('conmebol', 'domestic/confederation/conmebol/sudamericana/%s' % e)

    #load_games_standard('conmebol', 'domestic/confederation/conmebol/aldao')
    #load_games_standard('conmebol', 'domestic/confederation/conmebol/copa_ibarguren')

    #load_games_standard('conmebol', 'domestic/confederation/conmebol/copa_tie')
    #load_games_standard('conmebol', 'domestic/confederation/conmebol/masters')





def load_conmebol_international():
    from soccerdata.text import awards
    generic_load(soccer_db.conmebol_i_awards, awards.process_conmebol_international_awards)

    for year in range(1958, 2015, 4):
        load_games_standard('conmebol_i', 'international/confederation/conmebol/wcq/%s' % year)

    load_copa_america()

    load_games_standard('conmebol_i', 'international/confederation/conmebol/early_south_america')
    load_games_standard('conmebol_i', 'international/confederation/conmebol/copa_premio_honor')
    load_games_standard('conmebol_i', 'international/confederation/conmebol/copa_del_atlantico')
    load_games_standard('conmebol_i', 'international/confederation/conmebol/copa_newton')
    load_games_standard('conmebol_i', 'international/confederation/conmebol/copa_lipton')
    load_games_standard('conmebol_i', 'international/confederation/conmebol/copa_mayo')

    load_games_standard('conmebol_i', 'international/country/argentina')
    load_games_standard('conmebol_i', 'international/country/bolivia')
    #load_games_standard('conmebol_i', 'international/country/brazil')
    load_brazil_international()
    load_games_standard('conmebol_i', 'international/country/chile')
    load_games_standard('conmebol_i', 'international/country/colombia')
    load_games_standard('conmebol_i', 'international/country/ecuador')
    load_games_standard('conmebol_i', 'international/country/paraguay')
    load_games_standard('conmebol_i', 'international/country/peru')
    load_games_standard('conmebol_i', 'international/country/uruguay'),
    load_games_standard('conmebol_i', 'international/country/venezuela')


def load_cfu():
    from soccerdata.text import awards
    generic_load(soccer_db.cfu_awards, awards.process_cfu_awards)

    load_games_standard('cfu', 'domestic/confederation/concacaf/cfu/1990')
    load_games_standard('cfu', 'domestic/confederation/concacaf/cfu/2000')
    load_games_standard('cfu', 'domestic/confederation/concacaf/cfu/2010')

    # league results
    load_standings_standard('cfu', 'domestic/country/bermuda')
    load_standings_standard('cfu', 'domestic/country/trinidad')
    load_standings_standard('cfu', 'domestic/country/curacao')
    load_standings_standard('cfu', 'domestic/country/martinique')
    load_standings_standard('cfu', 'domestic/country/jamaica')

    for year in range(2010, 2012):
        load_games_standard('concacaf', 'domestic/country/jamaica/league/%s' % year)

    #for year in range(2010, 2012):
    #    load_games_standard('concacaf', 'domestic/country/trinidad/league/%s' % year)

    for year in range(2012, 2012):
        load_games_standard('concacaf', 'domestic/country/cuba/%s' % year)

    for year in range(2012, 2012):
        load_games_standard('concacaf', 'domestic/country/haiti/%s' % year)



def load_uncaf_international():
    from soccerdata.text import awards

    #generic_load(soccer_db.concacaf_i_awards, awards.process_uncaf_international_awards)

    load_games_standard('concacaf_i', 'international/confederation/concacaf/uncaf')

    load_games_standard('concacaf_i', 'international/country/belize')
    load_games_standard('concacaf_i', 'international/country/costa_rica')
    load_games_standard('concacaf_i', 'international/country/el_salvador')
    load_games_standard('concacaf_i', 'international/country/guatemala')
    load_games_standard('concacaf_i', 'international/country/honduras')
    load_games_standard('concacaf_i', 'international/country/nicaragua')
    load_games_standard('concacaf_i', 'international/country/panama')


def load_world_international():
    from soccerdata.text import awards, rosters

    generic_load(soccer_db.world_i_awards, awards.process_world_cup_awards)
    generic_load(soccer_db.world_i_awards, awards.process_olympics_awards)

    #generic_load(soccer_db.world_i_rosters, lambda: rosters.process_rosters('international/olympics'))
    #generic_load(soccer_db.world_i_rosters, lambda: rosters.process_rosters2(os.path.join('soccerdata/data/rosters/international/confederations')))

    confed = [1992, 1995, 1997, 1999, 2001, 2003, 2005, 2009, 2013]

    for e in confed:
        load_games_standard('world_i', 'international/world/confederations/%s' % e)

    for e in [1930, 1934] + list(range(1950, 2015, 4)):
        load_games_standard('world_i', 'international/world/world_cup/%s' % e)

    #load_games_standard('world_i', 'international/world/u17')

    load_games_standard('world_i', 'international/world/artemio_franchi')
    load_games_standard('world_i', 'international/world/interallied')
    load_games_standard('world_i', 'international/world/mundialito')

    olympics = [1900, 1904, 1908, 1912, 1920, 1924, 1928, 1936] + list(range(1948, 2000, 4))
    # list(range(1948, 2013, 4))

    # Merge olympic data.
    for e in olympics:
        load_games_standard('world_i', 'international/world/olympics/%s' % e, games_only=True)

    for e in range(1977, 2014, 2):
        load_games_standard('world_i', 'international/world/u20/%s' % e)



def load_world():
    from soccerdata.text import awards, rosters
    generic_load(soccer_db.world_awards, awards.process_world_awards)
    generic_load(soccer_db.world_awards, awards.process_isl_awards) # ISL et al.

    load_mixed_confederation()

    # Club World Cup
    for e in [2000, 2001] + list(range(2005, 2014)):
        load_games_standard('world', 'domestic/world/club_world_cup/%s' % e)

                      
    # International friendly club tournaments - ISL, Parmalat Cup, Copa Rio, etc.
    # Also existed in Brazil / Argentina / Colombia?
    generic_load(soccer_db.world_rosters, lambda: rosters.process_rosters2(os.path.join(ROOT_DIR, 'soccerdata/data/rosters/domestic/club_world_cup')))
    generic_load(soccer_db.world_rosters, lambda: rosters.process_rosters2(os.path.join(ROOT_DIR, 'soccerdata/data/rosters/domestic/isl')))
    generic_load(soccer_db.world_rosters, lambda: rosters.process_rosters2(os.path.join(ROOT_DIR, 'soccerdata/data/rosters/domestic/copita')))
    
    #load_sd_excel_standings('world', 'domestic/country/usa/isl')
    load_games_standard('world', 'domestic/country/usa/leagues/isl2')

    load_games_standard('world', 'domestic/country/mexico/friendly/palmares')

    load_games_standard('world', 'domestic/world/parmalat')
    load_games_standard('world', 'domestic/world/copa_rio')
    load_games_standard('world', 'domestic/confederation/conmebol/pequena')
    load_games_standard('world', 'international/misc/fifa_world_stars_games')


def load_caribbean_international():
    from soccerdata.text import awards

    generic_load(soccer_db.concacaf_i_awards, awards.process_caribbean_awards)

    load_games_standard('uncaf', 'international/confederation/concacaf/caribbean/cfu')
    load_games_standard('uncaf', 'international/confederation/concacaf/caribbean/1980')
    load_games_standard('uncaf', 'international/confederation/concacaf/caribbean/1990')
    load_games_standard('uncaf', 'international/confederation/concacaf/caribbean/2001')

    load_games_standard('concacaf_i', 'international/country/anguilla')
    load_games_standard('concacaf_i', 'international/country/antigua')
    load_games_standard('concacaf_i', 'international/country/aruba')
    load_games_standard('concacaf_i', 'international/country/bahamas')
    load_games_standard('concacaf_i', 'international/country/barbados')
    load_games_standard('concacaf_i', 'international/country/bermuda')    
    load_games_standard('concacaf_i', 'international/country/bvi')
    load_games_standard('concacaf_i', 'international/country/cayman')
    load_games_standard('concacaf_i', 'international/country/cuba')
    load_games_standard('concacaf_i', 'international/country/dominica')
    load_games_standard('concacaf_i', 'international/country/dr')
    load_games_standard('concacaf_i', 'international/country/french_guyana')
    load_games_standard('concacaf_i', 'international/country/grenada')
    load_games_standard('concacaf_i', 'international/country/guadeloupe')
    load_games_standard('concacaf_i', 'international/country/guyana')
    load_games_standard('concacaf_i', 'international/country/haiti')
    load_games_standard('concacaf_i', 'international/country/jamaica')
    load_games_standard('concacaf_i', 'international/country/martinique')
    load_games_standard('concacaf_i', 'international/country/montserrat')
    load_games_standard('concacaf_i', 'international/country/puerto_rico')
    load_games_standard('concacaf_i', 'international/country/nevis')
    load_games_standard('concacaf_i', 'international/country/st_lucia')
    load_games_standard('concacaf_i', 'international/country/saint_martin')
    load_games_standard('concacaf_i', 'international/country/st_vincent')
    load_games_standard('concacaf_i', 'international/country/sint_maarten')
    load_games_standard('concacaf_i', 'international/country/suriname')
    load_games_standard('concacaf_i', 'international/country/trinidad_tobago')
    load_games_standard('concacaf_i', 'international/country/turks_caicos')
    load_games_standard('concacaf_i', 'international/country/usvi')

    #load_games_standard('concacaf_i', 'international/country/saint_croix')
    #load_games_standard('concacaf_i', 'international/country/saint_thomas')    
    #load_games_standard('concacaf_i', 'international/country/tortola')
    #load_games_standard('concacaf_i', 'international/country/virgin_gorda')


def load_usmnt():
    from soccerdata.text import awards

    generic_load(soccer_db.usa_awards, awards.load_hall_of_fame)

                      
    root = os.path.join(ROOT_DIR, 'usmnt-data')

    for e in range(1910, 2020, 10):
        load_games_standard('usa', 'games/years/%s' % e, root=root)

    load_games_standard('usa', 'games/fifa/world_cup', root=root)
    load_games_standard('usa', 'games/friendly/us_cup', root=root)
    load_games_standard('usa', 'games/friendly/friendly', root=root)

    
def load_concacaf_international():
    from soccerdata.text import awards
    generic_load(soccer_db.concacaf_i_awards, awards.process_concacaf_international_awards)

    # World Cup qualifying
    for year in range(1994, 2015, 4):
        load_games_standard('concacaf_i', 'international/confederation/concacaf/wcq/%s' % year)
    load_games_standard('concacaf_i', 'international/confederation/concacaf/wcq/world_cup_qualifying')

    # Olympic qualifying
    for year in range(2000, 2014, 4):
        load_games_standard('concacaf_i', 'international/confederation/concacaf/olympic/%s' % year)

    # U-20 World Cup qualifying
    for year in [2009, 2011, 2013]:
        load_games_standard('concacaf_i', 'international/confederation/concacaf/u20/%s' % year)

    # U-17 World Cup qualifying (incomplete)
    for year in [2009, 2011, 2013]:
        load_games_standard('concacaf_i', 'international/confederation/concacaf/u17/%s' % year)

    # Gold Cup and predecessors
    load_games_standard('concacaf_i', 'international/confederation/concacaf/gold/championship')
    load_games_standard('concacaf_i', 'international/confederation/concacaf/gold/cccf')

    for e in [1991, 1993, 1996, 1998, 2000, 2002, 2003, 2005, 2007, 2009, 2011, 2013]:
        load_games_standard('concacaf_i', 'international/confederation/concacaf/gold/%s' % e)

    # Miscellaneous
    load_games_standard('concacaf_i', 'international/confederation/concacaf/cacg')
    load_games_standard('concacaf_i', 'international/confederation/concacaf/martinez')
    load_games_standard('concacaf_i', 'international/confederation/concacaf/independence')
    load_games_standard('cloncacaf_i', 'international/confederation/concacaf/friendly')

    #load_panamerican()
    #generic_load(soccer_db.concacaf_i_awards, awards.process_panamerican_awards)

    #for e in [1951, 1955, 1959, 1963, 1967, 1971, 1975, 1979, 1983, 1987, 
    #          1991, 1995, 1999, 2003, 2007]:
    #    load_games_standard('concacaf_i', 'international/world/panamerican/%s' % e)


    # Results by team
    load_uncaf_international()
    load_caribbean_international()
    load_usmnt()
    load_games_standard('canada', 'international/country/canada/1900')
    load_games_standard('canada', 'international/country/canada/2000')
    load_games_standard('mexico', 'international/country/mexico/alltime')


def load_concacaf():
    from soccerdata.text import awards
    generic_load(soccer_db.concacaf_awards, awards.process_concacaf_awards)

    load_games_standard('concacaf', 'domestic/confederation/concacaf/giantscup')
    load_games_standard('concacaf', 'domestic/confederation/concacaf/recopa')
    load_games_standard('concacaf', 'domestic/confederation/concacaf/superliga')

    for e in range(2008, 2014):
        load_games_standard('concacaf', 'domestic/confederation/concacaf/champions/league/%s' % e)

    for e in [1960, 1970, 1980, 1990, 2000]:
        load_games_standard('concacaf', 'domestic/confederation/concacaf/champions/%s' % e)


def load_ncaa():
    from soccerdata.text import awards, stats
    generic_load(soccer_db.ncaa_awards, awards.process_ncaa_awards)
    load_games_standard('ncaa', 'domestic/country/usa/college')

    generic_load(soccer_db.ncaa_stats, stats.process_ncaa_stats)

    for year in range(1959, 1963):
        load_games_standard('ncaa', 'games/championship/%s' % year, root=NCAA_DIR)

    for year in range(2011, 2014):
        load_games_standard('ncaa', 'games/championship/%s' % year, root=NCAA_DIR)



def load_fifa():

    from foulds.sites import fifa

    generic_load(soccer_db.fifa_games, fifa.scrape_all_world_cup_games)
    generic_load(soccer_db.fifa_goals, fifa.scrape_all_world_cup_goals)
    generic_load(soccer_db.fifa_lineups, fifa.scrape_all_world_cup_lineups)

    load_fifa_competition('FIFA U-20 World Cup')
    load_fifa_competition('FIFA U-17 World Cup')
    load_fifa_competition('FIFA Confederations Cup')
    load_fifa_competition('Olympic Games')

    #load_fifa_competition('FIFA Club World Cup')
    

def load_fifa_competition(competition):
    from foulds.sites import fifa
    games, goals, lineups = fifa.scrape_everything(competition)
    generic_load(soccer_db.fifa_games, lambda: games)
    generic_load(soccer_db.fifa_goals, lambda: goals)
    generic_load(soccer_db.fifa_lineups, lambda: lineups)



# Grouped.

def make_team_to_competition_dict():
    from donelli.parse.standings import process_excel_standings, process_standings_file

    # Create a dict mapping a team name and season to a competition.

    SDIR = os.path.join(ROOT_DIR, 'soccerdata/data/standings/domestic/country/usa/')
    
    l = process_standings_file(os.path.join(SDIR, 'mls'))

    l.extend(process_excel_standings(os.path.join(SDIR, 'apsl')))

    for e in '12', 'pdl', 'premier', 'pro',  'usisl':
        l.extend(process_excel_standings(os.path.join(SDIR, 'usl', e)))

    for e in 'ussf2', 'nasl2', 'usl/select', 'usl/usl_pro':
        p = os.path.join(SDIR, e)
        l.extend(process_standings_file(p, ';'))

    d = {}
    for e in l:
        key = (get_team(e['team']), e['season'])
        if key not in d:
            d[key] = [e['competition']]

    return d



# Only used by ltrack.
def determine_competition(comp, team, season, competition_map):
    from smid.alias.teams import get_team

    # Pull this out.
    mapping = {
        'CCC': 'CONCACAF Champions\' Cup',
        'CCL': 'CONCACAF Champions League',

        'CCup': 'Canadian Championship',
        'CanC': 'Canadian Championship',

        'SL': 'North American SuperLiga',
        'CFU': 'CFU Club Championship',

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
        'USOC': 'US Open Cup',
        'ASG': 'Friendly',
        'PDL': 'USL Premier Developmental League',
        'DC': 'Dallas Cup',

        'LT': 'Friendly', # Lisbon Tournament
        'WC': 'FIFA World Cup',

        'MkC': 'Friendly', # Milk Cup
        'Milk': 'Friendly', # Milk Cup

        'GCup': 'Gold Cup',

        'VDMT': 'Friendly', #'Val-de-Marne Tournament',

        'APT': 'Friendly', # Asia-Pacific Tour
        'NIF': 'Friendly', #'Nike International',

        'NLG': 'Friendly', # Non-League
        'SCC': 'Friendly', #'Sister Cities Cup'

        'MMF': 'FIFA U-17 World Cup', # not sure... 'Mondial Minimes Fra'
        'WC17': 'FIFA U-17 World Cup', 

        'ResL': 'MLS Reserve League',
        'CU17': 'FIFA U-17 World Cup',
        'CU20': 'FIFA U-20 World Cup',

        'WFC': 'Friendly', # World Football Challenge',
        'RGP': 'Friendly', # Rio Grande Plate
        }

    if comp in mapping:
        return mapping[comp]

    # ILG -> Interleague

    elif comp in ('LGE', 'ILG', 'PLO', 'PLOF'):  
        try:
            competitions = competition_map[(get_team(team), season)]
        except:
            competitions = []
            #import pdb; pdb.set_trace()

        if len(competitions) == 0:
            return comp
        elif len(competitions) > 1:
            import pdb; pdb.set_trace()
        else:
            return competitions[0]

    else:
        import pdb; pdb.set_trace()
        return comp



def load_ltrack():

    import ltrack.parse

    p = os.path.join(ROOT_DIR, 'ltrack/data')

    # Might be able to do this better...might not.
    func = functools.partial(determine_competition,
                             competition_map=make_team_to_competition_dict())

    generic_load(soccer_db.ltrack_goals, lambda: ltrack.parse.process_goals(p, func))
    generic_load(soccer_db.ltrack_games, lambda: ltrack.parse.process_games(p, func))
    generic_load(soccer_db.ltrack_lineups, lambda: ltrack.parse.process_lineups(p, func))




def flatten_stats(stats):
    """
    Convert stats into rosters.
    """

    r = []
    for stat in stats:
        r.append({
                'name': stat['name'],
                'team': stat['team'],
                'season': stat['season'],
                'competition': stat['competition'],
                })
    return r
        


def flatten_lineups(lineups):
    """
    Convert lineups into rosters.
    """

    r = { tuple([l[k] for k in ['name', 'team', 'season', 'competition']]) for l in lineups }
    rx = [{'name': e[0], 'team': e[1], 'season': e[2], 'competition': e[3]} for e in r]
    return rx
        



if __name__ == "__main__":
    load()

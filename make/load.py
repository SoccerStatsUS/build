# Can no longer build on server. Too much data, takes too long.
# Move this all over to Amazon. Taking too long to load here.
# Consider trimming down dramatically.
# Data quality is too low.

import functools
import os

from metadata.alias.people import check_for_name_loops
from metadata.alias.teams import check_for_team_loops, get_team
from build.mongo import generic_load, soccer_db
from build.settings import ROOT_DIR

from parse.parse import stats, games, standings, transactions


SPALDING_DIR = os.path.join(ROOT_DIR, 'spalding_data')
FRIENDLY_DIR = os.path.join(ROOT_DIR, 'friendly_data')

USD1_DIR = os.path.join(ROOT_DIR, 'usd1_data')
INDOOR_DIR = os.path.join(ROOT_DIR, 'indoor_data')

US_MINOR_DIR = os.path.join(ROOT_DIR, 'us_minor_data')

UEFA_DIR = os.path.join(ROOT_DIR, 'uefa_data')
CONMEBOL_DIR = os.path.join(ROOT_DIR, 'conmebol_data')
CONCACAF_DIR = os.path.join(ROOT_DIR, 'concacaf_data')
AFC_DIR = os.path.join(ROOT_DIR, 'afc_data')
CAF_DIR = os.path.join(ROOT_DIR, 'caf_data')
WORLD_DIR = os.path.join(ROOT_DIR, 'world_data')

NCAA_DIR = os.path.join(ROOT_DIR, 'ncaa_data')
NWSL_DIR = os.path.join(ROOT_DIR, 'nwsl_data')
CUPS_DIR = os.path.join(ROOT_DIR, 'us_cup_data')
ISL_DIR = os.path.join(ROOT_DIR, 'isl_data')

TEAM_DIR = os.path.join(ROOT_DIR, 'team_data')

INTERNATIONAL_DIR = os.path.join(ROOT_DIR, 'international_data')

#STATS_DIR = os.path.join(ROOT_DIR, "soccerdata/data/stats")


def clear_all():
    """
    Clear all relevant mongo tables.
    """
    from build.settings import STAT_TABLES, SOURCES, SINGLE_SOURCES
    for e in STAT_TABLES:
        soccer_db['%s' % e].drop()

    for s in SOURCES:
        for e in STAT_TABLES: 
            soccer_db['%s_%s' % (s, e)].drop()

    for e in SINGLE_SOURCES:
        soccer_db[e].drop()


def load_transactions_standard(coll, fn, root):

    print(fn)
    tx = transactions.process_transactions(fn, root)

    generic_load(soccer_db['%s_transactions' % coll], lambda: tx, delete=False)




def load_games_standard(coll, fn, root, games_only=False):
    """
    Load standard data from a standard games file.
    """

    print(fn)

    p = os.path.join(root, fn)
    gms, goals, fouls, lineups, rosters = games.process_file(p)

    generic_load(soccer_db['%s_games' % coll], lambda: gms, delete=False)

    if not games_only:
        generic_load(soccer_db['%s_lineups' % coll], lambda: lineups, delete=False)
        generic_load(soccer_db['%s_fouls' % coll], lambda: fouls, delete=False)
        generic_load(soccer_db['%s_goals' % coll], lambda: goals, delete=False)
        generic_load(soccer_db['%s_rosters' % coll], lambda: rosters, delete=False)


def load_standings_standard(coll, filename, root, delimiter=';'):
    """Load standard standings."""

    print(filename)
    generic_load(soccer_db['%s_standings' % coll], lambda: standings.process_standings_file(os.path.join(root, filename), delimiter))


def load_stats_standard(coll, filename, root, delimiter=';'):
    """Load standard stats """
    print(filename)
    generic_load(soccer_db['%s_stats' % coll], lambda: stats.process_stats(os.path.join(root, filename), delimiter))


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

    load_metadata()

    #load_usmntstats()
    #load_soccerstatsus()

    load_garberbucks()

    #load_early()
    #load_socceroutsider()
    
    #load_advanced()



def load_garberbucks():
    load_mls()
    #load_us_cups()
    #load_concacaf()


def load_soccerstatsus():
    """
    Load all main data by subject
    domestic: FIFA Club World Cup, Champions League, MLS, US minor, etc.
    women: US, Sweden, England
    indoor: US indoor 1975-2014)
    amateur: NCAA, amateur cup (?)
    international: USMNT, FIFA international, countries
    friendly: US friendly data
    """

    #load_women()
    load_domestic()
    #load_indoor()
    #load_amateur()
    #load_outer()
    #load_international()
    #load_friendly()



def load_socceroutsider():
    load_us_minor()
    load_usd1()    

    load_world()


def load_usmntstats():
    load_usmnt()
    

def load_metadata():
    """
    Load soccer metadata
    """

    load_sources()
    load_place_data()
    load_competitions()
    load_teams()
    load_bios()

    load_name_maps()
    load_stadium_maps()
    load_competition_maps()


def load_advanced():


    # drafts
    #load_drafts()

    # jobs
    load_jobs()
    load_transactions()

    # money data
    load_salaries()

    # news feeds
    #load_news()


def load_early():
    #load_early_friendly()

    load_nafbl()
    load_spalding()
    load_us_cups()



def load_international():

    load_world_international()
    load_concacaf_international()
    load_uefa_international()
    load_conmebol_international()

    load_oceania_international()
    load_asia_international()
    load_africa_international()


def load_domestic():

    load_usd1()    
    return
    load_us_minor()
    load_world()
    load_us_cups()

    return

    load_concacaf()
    load_conmebol()
    load_uefa()

    load_caf()
    load_ofc()
    load_afc()


def load_usd1():
    load_mls()

    return
    load_alpf()
    load_asl()
    load_nasl()




def load_outer():
    load_ltrack()
    #load_fifa()
    pass
    #load_mediotiempo()    


def load_mediotiempo():
    #from foulds.sites import mediotiempo

    games = mediotiempo.scrape_games(range(2000, 49000)) 

    generic_load(soccer_db['mediotiempo_games'], lambda: [e for e in games if e not in [{}, None]])
    #generic_load(soccer_db['mls2_goals'], lambda: [e for e in goals if e not in [{}, None]])
    #generic_load(soccer_db['mls2_lineups'], lambda: [e for e in lineups if e not in [{}, None]])


def load_name_maps():
    """
    Map team names to appropriate aliases
    eg FC Dallas -> Dallas Burn for 1996-2004
    """
    from metadata.parse import namemap
    generic_load(soccer_db.name_maps, namemap.load)


def load_competition_maps():
    """
    Competition aliases.
    eg A-League / USL 1
    """
    from metadata.parse import competitionnamemap
    generic_load(soccer_db.competition_maps, competitionnamemap.load)    


def load_stadium_maps():
    """
    Team to stadium mappings
    eg FC Dallas -> Dragon Stadium, 2003, 2003
    """
    from metadata.parse import stadiummap
    generic_load(soccer_db.stadium_maps, stadiummap.load)


def load_sources():
    from metadata.parse import sources
    generic_load(soccer_db.sources, sources.load)


def load_news():
    from oneonta import feeds
    generic_load(soccer_db.news, feeds.parse_feeds)


def load_bios():
    print('loading bios')

    from metadata.parse import bios
    #from foulds.sites import mlsnet, mlssoccer

    generic_load(soccer_db.asl_bios, bios.process_asl_bios)

    #print("Loading MLSsoccer.com player bios.")
    #generic_load(soccer_db.mls_bios, mlssoccer.scrape_all_bios)

    #generic_load(soccer_db.mls_bios, mlsnet.scrape_2005_bios)
    #generic_load(soccer_db.mls_bios, mlsnet.scrape_2001_bios)

    generic_load(soccer_db.fifa_bios, bios.process_world_cup_bios)
    generic_load(soccer_db.nasl_bios, bios.process_misl_bios)
    generic_load(soccer_db.nasl_bios, bios.process_nasl_bios)
    generic_load(soccer_db.usa_bios, bios.process_usa_bios)
    generic_load(soccer_db.mls_bios, bios.process_mls_bios)
    generic_load(soccer_db.mls_reserve_bios, bios.process_mls_reserve_bios)
    generic_load(soccer_db.asl_bios, bios.process_asl_bios2)
    generic_load(soccer_db.asl2_bios, bios.process_asl2_bios)
    generic_load(soccer_db.us_minor_bios, bios.process_ussf2_bios)
    generic_load(soccer_db.us_minor_bios, bios.process_nasl2_bios)
    generic_load(soccer_db.us_minor_bios, bios.process_apsl_bios)

    generic_load(soccer_db.us_minor_bios, bios.process_usl1_bios)
    generic_load(soccer_db.us_minor_bios, bios.process_usl2_bios)

    generic_load(soccer_db.us_minor_bios, bios.process_pdl_bios)
    generic_load(soccer_db.us_minor_bios, bios.load_other_bios) 
    

def load_place_data():
    """
    Load place data.
    """
    from metadata.parse import places

    generic_load(soccer_db.countries, places.load_countries)
    generic_load(soccer_db.states, places.load_states)
    generic_load(soccer_db.state_populations, places.load_state_populations)
    generic_load(soccer_db.stadiums, places.load_stadiums)


def load_us_cups():

    from metadata.parse import awards
    from parse.parse import rosters

    # Open

    generic_load(soccer_db.us_cups_awards, awards.process_us_open_cup_awards, delete=False)


    for e in range(2011, 2015):
        load_games_standard('us_cups', 'games/open/%s' % e, root=CUPS_DIR)#, games_only=True)


    return

    for e in range(191, 202):
        load_games_standard('us_cups', 'games/open/%s0' % e, root=CUPS_DIR)#, games_only=True)


    # AFA

    generic_load(soccer_db.us_cups_awards, awards.process_american_cup_awards)
    generic_load(soccer_db.us_cups_rosters, lambda: rosters.process_rosters2(path=os.path.join(CUPS_DIR, "rosters/afa"))
)
    load_games_standard('us_cups', 'games/open/afa' , root=CUPS_DIR)
    load_games_standard('us_cups', 'games/open/afa2' , root=CUPS_DIR)


    # Other

    generic_load(soccer_db.us_cups_awards, awards.process_lewis_cup_awards, delete=False)

    load_games_standard('us_cups', 'games/league/lewis' , root=CUPS_DIR)
    load_games_standard('us_cups', 'games/league/duffy' , root=CUPS_DIR)
    load_games_standard('us_cups', 'games/amateur/aafa' , root=CUPS_DIR)


    #load_games_standard('us_cups', 'games/amateur', root=CUPS_DIR)


def load_canada():
    from metadata.parse import awards
    #, partial

    load_standings_standard('canada', 'standings/canada/csl1', root=CONCACAF_DIR)
    load_standings_standard('canada', 'standings/canada/cnsl', root=CONCACAF_DIR)
    load_standings_standard('canada', 'standings/canada/csl', root=CONCACAF_DIR)
    
    load_games_standard('canada', 'games/country/canada/cups/championship', root=CONCACAF_DIR)
    load_games_standard('canada', 'games/country/canada/cups/early', root=CONCACAF_DIR)

    load_games_standard('canada', 'games/country/canada/friendly/1', root=CONCACAF_DIR)
    load_games_standard('canada', 'games/country/canada/friendly/friendly2', root=CONCACAF_DIR)
    load_games_standard('canada', 'games/country/canada/friendly/toronto', root=CONCACAF_DIR)
    load_games_standard('canada', 'games/country/canada/friendly/vancouver', root=CONCACAF_DIR)

    #generic_load(soccer_db.canada_stats, partial.process_csl_partial)

    generic_load(soccer_db.canada_awards, awards.process_csl_awards)
    generic_load(soccer_db.canada_awards, awards.process_canada_awards)


def load_uncaf():
    from metadata.parse import awards

    generic_load(soccer_db.concacaf_awards, awards.process_uncaf_awards)

    generic_load(soccer_db.concacaf_awards, awards.process_guatemala_awards)
    generic_load(soccer_db.concacaf_awards, awards.process_honduras_awards)
    generic_load(soccer_db.concacaf_awards, awards.process_costa_rica_awards)
    generic_load(soccer_db.concacaf_awards, awards.process_elsalvador_awards)
    generic_load(soccer_db.concacaf_awards, awards.process_panama_awards)
    generic_load(soccer_db.concacaf_awards, awards.process_nicaragua_awards)

    load_standings_standard('concacaf', 'standings/guatemala/3', root=CONCACAF_DIR)
    load_standings_standard('concacaf', 'standings/elsalvador/2', root=CONCACAF_DIR)
    load_standings_standard('concacaf', 'standings/honduras', root=CONCACAF_DIR)
    load_standings_standard('concacaf', 'standings/costarica/2', root=CONCACAF_DIR)
    load_standings_standard('concacaf', 'standings/costarica/3', root=CONCACAF_DIR)
    load_standings_standard('concacaf', 'standings/panama', root=CONCACAF_DIR)
    load_standings_standard('concacaf', 'standings/nicaragua', root=CONCACAF_DIR)
    #load_standings_standard('concacaf', 'standings/belize', root=CONCACAF_DIR)
    
    for e in range(1996, 2014):
        load_games_standard('concacaf', 'games/country/guatemala/league/%s' % e, root=CONCACAF_DIR)

    for e in range(1999, 2014):
        load_games_standard('concacaf', 'games/country/el_salvador/%s' % e, root=CONCACAF_DIR)

    for e in range(1996, 2014):
        load_games_standard('concacaf', 'games/country/honduras/%s' % e, root=CONCACAF_DIR)

    for e in range(1997, 2014):
        load_games_standard('concacaf', 'games/country/costa_rica/league/d1/%s' % e, root=CONCACAF_DIR)

    for e in range(1998, 2014):
        load_games_standard('concacaf', 'games/country/panama/d1/%s' % e, root=CONCACAF_DIR)

    for e in range(2010, 2013):
        load_games_standard('concacaf', 'games/country/nicaragua/%s' % e, root=CONCACAF_DIR)

    #for e in range(2013, 2013):
    #    load_games_standard('concacaf', 'games/country/belize/%s' % e, root=CONCACAF_DIR)

    load_games_standard('concacaf', 'games/confederation/uncaf/fraternidad', root=CONCACAF_DIR)
    load_games_standard('concacaf', 'games/confederation/uncaf/torneograndes', root=CONCACAF_DIR)
    load_games_standard('concacaf', 'games/confederation/uncaf/interclube', root=CONCACAF_DIR)

    #load_games_standard('concacaf', 'games/el_salvador/torneo', root=CONCACAF_DIR)


def load_uefa():

    for e in range(1955, 1992):
        load_games_standard('uefa', 'games/confederation/champions/%s' % e, root=UEFA_DIR)

    load_games_standard('uefa', 'games/confederation/super', root=UEFA_DIR)

    load_uefa_leagues()




def load_uefa_leagues():
    from metadata.parse import awards

    generic_load(soccer_db.uefa_awards, awards.process_uefa_awards)
    generic_load(soccer_db.uefa_awards, awards.process_england_awards)

    load_uefa_major()
    load_uefa_mid()
    load_uefa_minor()

    load_uefa_friendly()



def load_caf():
    from metadata.parse import awards

    #generic_load(soccer_db.uefa_awards, awards.process_caf_awards)

    #load_standings_standard('uefa', 'standings/ghana', root=CAF_DIR)
    #load_standings_standard('uefa', 'standings/southafrica', root=CAF_DIR)

    #load_standings_standard('uefa', 'standings/nigeria', root=CAF_DIR)
    #load_standings_standard('uefa', 'standings/cameroon', root=CAF_DIR)

    #load_standings_standard('uefa', 'standings/sudan', root=CAF_DIR)
    #load_standings_standard('uefa', 'standings/congo_dr', root=CAF_DIR)

    #load_standings_standard('uefa', 'standings/cote_divoire', root=CAF_DIR)


    load_northern_africa()

    load_southern_africa()

    for year in range(2003, 2011):
        load_games_standard('uefa', 'games/nigeria/%s' % year, root=CAF_DIR)

    for year in range(2005, 2013):
        load_games_standard('uefa', 'games/ghana/%s' % year, root=CAF_DIR)

    for year in range(2009, 2014):
        load_games_standard('uefa', 'games/cameroon/%s' % year, root=CAF_DIR)

    return

    for year in range(2010, 2010):
        load_games_standard('uefa', 'games/dr_congo/%s' % year, root=CAF_DIR)

def load_northern_africa():

    #load_standings_standard('uefa', 'standings/tunisia', root=CAF_DIR)
    #load_standings_standard('uefa', 'standings/egypt', root=CAF_DIR)
    #load_standings_standard('uefa', 'standings/algeria', root=CAF_DIR)
    #load_standings_standard('uefa', 'standings/morocco', root=CAF_DIR)
    #load_standings_standard('uefa', 'standings/libya', root=CAF_DIR)

    for year in range(1994, 2014):
        load_games_standard('uefa', 'games/algeria/%s' % year, root=CAF_DIR)

    return

    for year in range(2006, 2014):
        load_games_standard('uefa', 'games/egypt/%s' % year, root=CAF_DIR)



    for year in range(2013, 2013):
        load_games_standard('uefa', 'games/tunisia/%s' % year, root=CAF_DIR)

    for year in range(2010, 2011):
        load_games_standard('uefa', 'games/morocco/%s' % year, root=CAF_DIR)

    for year in range(2011, 2011):
        load_games_standard('uefa', 'games/libya/%s' % year, root=CAF_DIR)



def load_southern_africa():

    #load_standings_standard('uefa', 'games/south_africa', root=CAF_DIR)
    #load_standings_standard('uefa', 'games/angola', root=CAF_DIR)
    #load_standings_standard('uefa', 'games/zimbabwe', root=CAF_DIR)
    #load_standings_standard('uefa', 'games/zambia', root=CAF_DIR)

    for year in range(2010, 2010):
        load_games_standard('uefa', 'games/angola/%s' % year, root=CAF_DIR)

    for year in range(2006, 2013):
        load_games_standard('uefa', 'games/southafrica/%s' % year, root=CAF_DIR)

    for year in range(2013, 2013):
        load_games_standard('uefa', 'games/zambia/%s' % year, root=CAF_DIR)

    for year in range(2010, 2010):
        load_games_standard('uefa', 'games/zambia/%s' % year, root=CAF_DIR)


def load_premier_league():
    from foulds.sites import premierleague
    generic_load(soccer_db.epl_games, premierleague.scrape_calendars)


def load_spalding():

    for year in ['1904','1906','1909','1911','1912','1913','1914','1916','1917','1918','1919','1921','1922', '1923']:
        load_standings_standard('uefa', 'standings/%s' % year, root=SPALDING_DIR)
        load_games_standard('uefa', 'games/%s' % year, root=SPALDING_DIR)


def load_uefa_major():

    #load_premier_league()

    load_standings_standard('uefa', 'standings/italy', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/spain', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/france', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/germany', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/england/epl', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/england/epl2', root=UEFA_DIR)
    
    # england
    for year in range(1992, 2014):
        load_games_standard('uefa', 'games/country/england/%s' % year, root=UEFA_DIR)

    for year in range(1996, 2014):
        load_games_standard('uefa', 'games/country/germany/men/%s' % year, root=UEFA_DIR)

    for year in range(1997, 2014):
        load_games_standard('uefa', 'games/country/spain/%s' % year, root=UEFA_DIR)

    for year in range(1996, 2014):
        load_games_standard('uefa', 'games/country/italy/%s' % year, root=UEFA_DIR)

    for year in range(1998, 2014):
        load_games_standard('uefa', 'games/country/france/%s' % year, root=UEFA_DIR)






def load_uefa_mid():

    load_standings_standard('uefa', 'standings/netherlands', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/belgium', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/turkey', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/russia', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/ukraine', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/portugal', root=UEFA_DIR)


    for year in range(1996, 2014):
        load_games_standard('uefa', 'games/country/netherlands/%s' % year, root=UEFA_DIR)

    for year in range(1997, 2014):
        load_games_standard('uefa', 'games/country/turkey/%s' % year, root=UEFA_DIR)

    for year in range(1998, 2014):
        load_games_standard('uefa', 'games/country/portugal/%s' % year, root=UEFA_DIR)

    for year in range(1997, 2014):
        load_games_standard('uefa', 'games/country/belgium/%s' % year, root=UEFA_DIR)

    for year in range(1999, 2014):
        load_games_standard('uefa', 'games/country/russia/%s' % year, root=UEFA_DIR)

    #for year in range(2000, 2014): # 1999
    #for year in range(1997, 2014):
    #    load_games_standard('uefa', 'games/country/ukraine/%s' % year, root=UEFA_DIR)

    for year in range(1990, 1990):
        load_games_standard('uefa', 'games/country/ussr/%s' % year, root=UEFA_DIR)



def load_scandinavia():

    load_standings_standard('uefa', 'standings/denmark', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/sweden', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/norway', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/finland', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/iceland', root=UEFA_DIR)

    for year in range(1997, 2014):
        load_games_standard('uefa', 'games/country/denmark/%s' % year, root=UEFA_DIR)

    for year in range(1999, 2014):
        load_games_standard('uefa', 'games/country/norway/%s' % year, root=UEFA_DIR)

    for year in range(1998, 2014):
        load_games_standard('uefa', 'games/country/sweden/%s' % year, root=UEFA_DIR)

    #for year in range(2012, 2012):
    #    load_games_standard('uefa', 'games/country/finland/%s' % year, root=UEFA_DIR)

    #for year in range(2012, 2012):
    #    load_games_standard('uefa', 'games/country/iceland/%s' % year, root=UEFA_DIR)


def load_uefa_minor():

    load_scandinavia()

    load_standings_standard('uefa', 'standings/switzerland', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/scotland2', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/austria2', root=UEFA_DIR)
    load_standings_standard('uefa', 'standings/poland', root=UEFA_DIR)    
    #load_standings_standard('uefa', 'standings/ireland', root=UEFA_DIR)

    #load_standings_standard('uefa', 'standings/czech', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/romania', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/serbia', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/croatia', root=UEFA_DIR)

    #load_standings_standard('uefa', 'standings/bosnia', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/slovakia', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/slovenia', root=UEFA_DIR)

    #load_standings_standard('uefa', 'standings/greece', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/cyprus', root=UEFA_DIR)

    #load_standings_standard('uefa', 'standings/hungary2', root=UEFA_DIR)
    #load_standings_standard('uefa', 'standings/bulgaria', root=UEFA_DIR)

    #load_standings_standard('uefa', 'standings/wales', root=UEFA_DIR)

    for year in range(1996, 2014):
        load_games_standard('uefa', 'games/country/poland/%s' % year, root=UEFA_DIR)

    for year in range(1996, 2014):
        load_games_standard('uefa', 'games/country/scotland/%s' % year, root=UEFA_DIR)

    for year in range(1996, 2014):
        load_games_standard('uefa', 'games/country/switzerland/%s' % year, root=UEFA_DIR)

    for year in range(1996, 2014):
        load_games_standard('uefa', 'games/country/austria/%s' % year, root=UEFA_DIR)

    for year in range(2000, 2014):
        load_games_standard('uefa', 'games/country/ireland/%s' % year, root=UEFA_DIR)

    for year in range(1997, 2012):
        load_games_standard('uefa', 'games/country/romania/%s' % year, root=UEFA_DIR)

    for year in range(1997, 2013):
        load_games_standard('uefa', 'games/country/czech/%s' % year, root=UEFA_DIR)

    for year in range(1998, 2013):
        load_games_standard('uefa', 'games/country/hungary/%s' % year, root=UEFA_DIR)

    for year in range(1995, 2013):
        load_games_standard('uefa', 'games/country/cyprus/%s' % year, root=UEFA_DIR)

    for year in range(2004, 2012):
        load_games_standard('uefa', 'games/country/greece/%s' % year, root=UEFA_DIR)

    for year in range(2008, 2011):
        load_games_standard('uefa', 'games/country/serbia/%s' % year, root=UEFA_DIR)

    for year in range(2008, 2013):
        load_games_standard('uefa', 'games/country/croatia/%s' % year, root=UEFA_DIR)

    for year in range(2010, 2013):
        load_games_standard('uefa', 'games/country/bosnia/%s' % year, root=UEFA_DIR)

    for year in range(2011, 2013):
        load_games_standard('uefa', 'games/country/slovenia/%s' % year, root=UEFA_DIR)

    return

    for year in range(2012, 2013):
        load_games_standard('uefa', 'games/country/slovakia/%s' % year, root=UEFA_DIR)

    for year in range(2012, 2012):
        load_games_standard('uefa', 'games/country/bulgaria/%s' % year, root=UEFA_DIR)


def load_uefa_friendly():
    load_games_standard('uefa', 'games/spain/friendly/madrid')



def load_conmebol_leagues():

    load_conmebol_minor()
    load_brazil()
    load_argentina()


def load_conmebol_minor():

    from metadata.parse import awards

    generic_load(soccer_db.conmebol_awards, awards.process_conmebol_league_awards)

    load_standings_standard('conmebol', 'standings/uruguay2', root=CONMEBOL_DIR)
    load_standings_standard('conmebol', 'standings/chile2', root=CONMEBOL_DIR)
    load_standings_standard('conmebol', 'standings/colombia3', root=CONMEBOL_DIR)
    load_standings_standard('conmebol', 'standings/ecuador', root=CONMEBOL_DIR)
    load_standings_standard('conmebol', 'standings/peru', root=CONMEBOL_DIR)
    load_standings_standard('conmebol', 'standings/paraguay', root=CONMEBOL_DIR)
    load_standings_standard('conmebol', 'standings/bolivia', root=CONMEBOL_DIR)
    #load_standings_standard('conmebol', 'standings/venezuela', root=CONMEBOL_DIR)

    # Historic standings

    #load_standings_standard('conmebol', 'standings/colombia2', root=CONMEBOL_DIR)
    #load_standings_standard('conmebol', 'standings/colombia', root=CONMEBOL_DIR)
    #load_standings_standard('conmebol', 'standings/chile', root=CONMEBOL_DIR)
    #load_standings_standard('conmebol', 'standings/uruguay', root=CONMEBOL_DIR)


    for year in range(1996, 2014):
        load_games_standard('conmebol', 'games/country/uruguay/%s' % year, root=CONMEBOL_DIR)

    for year in range(1996, 2014):
        load_games_standard('conmebol', 'games/country/chile/%s' % year, root=CONMEBOL_DIR)

    for year in range(1997, 2014):
        load_games_standard('conmebol', 'games/country/colombia/%s' % year, root=CONMEBOL_DIR)

    for year in range(1996, 2014):
        load_games_standard('conmebol', 'games/country/ecuador/%s' % year, root=CONMEBOL_DIR)

    for year in range(1996, 2014):
        load_games_standard('conmebol', 'games/country/bolivia/%s' % year, root=CONMEBOL_DIR)

    for year in range(1996, 2014):
        load_games_standard('conmebol', 'games/country/peru/%s' % year, root=CONMEBOL_DIR)

    for year in range(1997, 2014):
        load_games_standard('conmebol', 'games/country/paraguay/%s' % year, root=CONMEBOL_DIR)

    for year in range(2012, 2014):
        load_games_standard('conmebol', 'games/country/venezuela/%s' % year, root=CONMEBOL_DIR)


def load_argentina():
    from metadata.parse import awards

    generic_load(soccer_db.conmebol_awards, awards.process_argentina_awards)
    
    load_standings_standard('conmebol', 'standings/argentina', root=CONMEBOL_DIR)

    # historic
    #load_standings_standard('conmebol', 'standings/argentina2', root=CONMEBOL_DIR)

    for year in range(1967, 1985):
        load_games_standard('conmebol', 'games/country/argentina/city/%s' % year, root=CONMEBOL_DIR)

    #for year in range(1932, 2014):
    for year in range(2010, 2014):
        load_games_standard('conmebol', 'games/country/argentina/leagues/%s' % year, root=CONMEBOL_DIR)


def load_brazil():
    from metadata.parse import awards

    load_standings_standard('conmebol', 'standings/brazil', root=CONMEBOL_DIR)

    generic_load(soccer_db.conmebol_awards, awards.process_brazil_awards)

    #for e in range(1971, 2014):
    for e in range(1971, 2014):
        load_games_standard('brazil', 'games/country/brazil/brasileiro/%s' % e, root=CONMEBOL_DIR)

    # state leagues.

    for year in range(1905, 2013):
        load_games_standard('brazil', 'games/country/brazil/paulista/%s' % year, root=CONMEBOL_DIR)

    for year in range(1946, 2013):
        load_games_standard('brazil', 'games/country/brazil/carioca/%s' % year, root=CONMEBOL_DIR)

    #for year in range(1915, 1917):
    #    load_games_standard('brazil', 'games/country/brazil/minas_gerais/%s' % year, root=CONMEBOL_DIR)

    for year in range(2006, 2013):
        load_games_standard('brazil', 'games/country/brazil/minas_gerais/%s' % year, root=CONMEBOL_DIR)

    #for year in range(2011, 2013):
    #    load_games_standard('brazil', 'games/country/brazil/gaucho/%s' % year, root=CONMEBOL_DIR)

    for year in range(2011, 2013):
        load_games_standard('brazil', 'games/country/brazil/bahia/%s' % year, root=CONMEBOL_DIR)

    for year in range(2013, 2013):
        load_games_standard('brazil', 'games/country/brazil/pernambuco/%s' % year, root=CONMEBOL_DIR)

    for year in range(2013, 2013):
        load_games_standard('brazil', 'games/country/brazil/parana/%s' % year, root=CONMEBOL_DIR)

    for year in range(2013, 2013):
        load_games_standard('brazil', 'games/country/brazil/santacatarina/%s' % year, root=CONMEBOL_DIR)


    #load_games_standard('brazil', 'country/games/brazil/friendly/botafogo', root=CONMEBOL_DIR)


def load_brazil_international():

    for e in ['1906', '1914', '1923', '1934', '1939']:
        load_games_standard('brazil', 'games/country/brazil/%s' % e, root=INTERNATIONAL_DIR)



def load_women():
    load_women_international()
    load_women_domestic()


def load_women_international():
    pass


def load_women_domestic():
    from metadata.parse import awards

    generic_load(soccer_db.women_awards, awards.process_women_awards)

    load_games_standard('women', 'games/usa/wusa/wusa', root=NWSL_DIR)
    load_games_standard('women', 'games/usa/wps/wps', root=NWSL_DIR)
    load_games_standard('women', 'games/usa/nwsl/2013', root=NWSL_DIR)
    load_games_standard('women', 'games/usa/nwsl/2014', root=NWSL_DIR)

    load_games_standard('women', 'games/usa/wpsl/elite', root=NWSL_DIR)

    #for e in range(2007, 2013):
    #    load_games_standard('women', 'domestic/country/usa/leagues/women/wpsl/%s' % e)

    nwsl_stats = stats.process_stats("nwsl/2013", root=os.path.join(NWSL_DIR, 'stats'), delimiter=';')
    generic_load(soccer_db.women_stats, nwsl_stats)

    for e in ['wusa', 'wps', 'wpsl_elite', 'nwsl', 'wsl']:
        load_standings_standard('women', 'standings/usa/%s' % e, root=NWSL_DIR)

    return

    load_standings_standard('standings/sweden', e, root=NWSL_DIR)
    load_standings_standard('standings/france', e, root=NWSL_DIR)

    generic_load(soccer_db.women_rosters, lambda: flatten_lineups(soccer_db.women_lineups.find({'competition': 'Women\'s United Soccer Association'})))
    generic_load(soccer_db.women_rosters, lambda: flatten_lineups(soccer_db.women_lineups.find({'competition': 'National Women\'s Soccer League'})))


    for e in range(2012, 2013):
        load_games_standard('women', 'games/argentina/%s' % e, root=NWSL_DIR)

    for e in range(2008, 2013):
        load_games_standard('women', 'games/australia/%s' % e, root=NWSL_DIR)

    # Europe


    for e in range(2000, 2005):
        load_games_standard('women', 'games/england/1/%s' % e, root=NWSL_DIR)

    for e in range(2000, 2011): # through 2010.
        load_games_standard('women', 'games/france/1/%s' % e, root=NWSL_DIR)

    for e in range(2000, 2011):
        load_games_standard('women', 'games/germany/%s' % e, root=NWSL_DIR)

    for e in range(2000, 2006):
        load_games_standard('women', 'games/sweden/1/%s' % e, root=NWSL_DIR)


def load_mlssoccer_season(url, competition):
    #from foulds.sites.mlssoccer import scrape_competition

    games, goals, lineups = scrape_competition(url, competition)

    generic_load(soccer_db['mls2_games'], lambda: [e for e in games if e not in [{}, None]])
    generic_load(soccer_db['mls2_goals'], lambda: [e for e in goals if e not in [{}, None]])
    generic_load(soccer_db['mls2_lineups'], lambda: [e for e in lineups if e not in [{}, None]])


def load_mls():
    from metadata.parse import awards

    from parse.parse import rosters

    generic_load(soccer_db.mls_awards, awards.process_mls_awards)

    generic_load(soccer_db.mls_rosters, lambda: flatten_stats(soccer_db.mls_stats.find()))

    for e in range(2014, 2017):
        generic_load(soccer_db.mls_rosters, lambda: rosters.process_rosters3('data/rosters/mls/' + str(e), root=USD1_DIR), delete=False)
        generic_load(soccer_db.mls_bios, lambda: rosters.process_rosters3('data/rosters/mls/' + str(e), root=USD1_DIR), delete=False)


    """
    generic_load(soccer_db.mls_rosters, lambda: rosters.process_rosters3('data/rosters/mls/2016b', root=USD1_DIR), delete=False)
    generic_load(soccer_db.mls_rosters, lambda: rosters.process_rosters3('data/rosters/mls/2015', root=USD1_DIR), delete=False)
    generic_load(soccer_db.mls_rosters, lambda: rosters.process_rosters3('data/rosters/mls/2014', root=USD1_DIR), delete=False)

    generic_load(soccer_db.mls_bios, lambda: rosters.process_rosters3('data/rosters/mls/2016b', root=USD1_DIR), delete=False)
    generic_load(soccer_db.mls_bios, lambda: rosters.process_rosters3('data/rosters/mls/2015', root=USD1_DIR), delete=False)
    generic_load(soccer_db.mls_bios, lambda: rosters.process_rosters3('data/rosters/mls/2014', root=USD1_DIR), delete=False)
    """

    for e in range(1996, 2017):
        load_transactions_standard('mls', 'data/transactions/mls/%s' % e, USD1_DIR)


    load_standings_standard('mls', 'data/standings/mls', root=USD1_DIR)

    for e in range(2012, 2017):
        generic_load(soccer_db.mls_stats, stats.process_stats("data/stats/mls/" + str(e), source='MLSSoccer.com', root=USD1_DIR))

    # Add rsssf games.
    #for e in range(2001, 2001):
    #    r = os.path.join(ROOT_DIR, 'usd1_data/data/games/mls/sources/rsssf/%s' % e)
    #    load_games_standard('mls3', str(e), root=r)

    for e in range(1996, 2017):
        load_games_standard('mls', 'data/games/mls/%s' % e, root=USD1_DIR)

    load_mls_lineup_db()

    print("Loading MLS reserves data.")
    for e in [2005, 2006, 2007, 2008, 2011, 2012, 2013, 2014]:
        load_games_standard('mls', 'data/games/mls/reserve/mls/%s' % e, root=USD1_DIR)

    #generic_load(soccer_db.asl_rosters, lambda: flatten_stats(soccer_db.asl_stats.find()))

    load_games_standard('mls', 'data/games/mls/playoffs', root=USD1_DIR)

    # 2012 is actually 1996-2012.


    #generic_load(soccer_db.mls_stats, stats.process_stats("data/stats/mls/2012", source='MLSSoccer.com', root=USD1_DIR))
    #generic_load(soccer_db.mls_stats, stats.process_stats("data/stats/mls/2013", source='MLSSoccer.com', root=USD1_DIR))


    """
    u = 'http://www.mlssoccer.com/schedule?month=all&year=%s&club=all&competition_type=%s&broadcast_type=all&op=Search&form_id=mls_schedule_form'

    for year in (2011, 2012, 2013):
        load_mlssoccer_season(u % (year, 46), 'Major League Soccer')
        load_mlssoccer_season(u % (year, 45), 'MLS Cup Playoffs')
        load_mlssoccer_season(u % (year, 44), 'MLS Cup Playoffs')
    """

    



def load_nafbl():
    from metadata.parse import awards

    # Also loading ALPF and SNESL
    generic_load(soccer_db.asl_awards, awards.process_nafbl_awards, delete=False)
    generic_load(soccer_db.asl_awards, awards.process_snesl_awards, delete=False)

    #load_standings_standard('us_minor', 'domestic/country/usa/nafbl')
    #load_standings_standard('us_minor', 'domestic/country/usa/snesl')
    #load_standings_standard('us_minor', 'domestic/country/usa/nasfl')

    load_games_standard('us_minor', 'games/regional/nafbl1', root=US_MINOR_DIR)
    load_games_standard('us_minor', 'games/regional/nafbl2', root=US_MINOR_DIR)
    load_games_standard('us_minor', 'games/regional/snesl', root=US_MINOR_DIR)
    load_games_standard('us_minor', 'games/regional/nasfl', root=US_MINOR_DIR)
    #load_games_standard('us_minor', 'games/misc/isl', root=US_MINOR_DIR)



def load_city():
    from metadata.parse import awards

    load_new_york()
    load_st_louis()

    #load_games_standard('city', 'city')
    #generic_load(soccer_db.city_awards, awards.process_chicago_awards, delete=False)


def load_new_york():
    from metadata.parse import awards

    #load_games_standard('state', 'domestic/country/usa/leagues/regional/metropolitan')
    #load_games_standard('state', 'domestic/country/usa/friendly/1900_ny')
    generic_load(soccer_db.state_awards, awards.process_ny_awards, delete=False)

    #load_sd_excel_standings('city', 'domestic/city/cosmo')

def load_st_louis():
    #load_sd_excel_standings('city', 'domestic/city/slsl')
    pass


def load_friendly():
    load_early_friendly()
    load_modern_friendly()

def load_early_friendly():

    for e in range(1865, 1891, 5):
        load_games_standard('us_friendly', 'games/friendly/%s' % e, root=FRIENDLY_DIR)

    for e in range(1900, 1951, 10):
        load_games_standard('us_friendly', 'games/friendly/%s' % e, root=FRIENDLY_DIR)


def load_modern_friendly():

    #load_games_standard('us_friendly', 'games/misc/bicentennial', root=INTERNATIONAL_DIR)

    load_games_standard('us_friendly', 'games/friendly/1960')
    load_games_standard('us_friendly', 'games/friendly/1967')
    load_games_standard('us_friendly', 'games/friendly/1970')
    load_games_standard('us_friendly', 'games/friendly/1980')
    load_games_standard('us_friendly', 'games/friendly/tours/1970')
    load_games_standard('us_friendly', 'games/friendly/tours/1980')
    load_games_standard('us_friendly', 'games/friendly/1990')
    load_games_standard('us_friendly', 'games/friendly/2000')
    load_games_standard('us_friendly', 'games/friendly/2010')

    # All-Star game.
    load_games_standard('us_friendly', 'games/friendly/mls_all_star')

    # Premium tournaments (superclubs)
    #load_games_standard('us_friendly', 'games/friendly/wfc')
    #load_games_standard('us_friendly', 'games/friendly/icc')

    for e in ['arizona', 'canada', 'carolina', 'coliseo', 'desert', 'disney', 'dynamo', 'europac', 'festival_of_americas', 'hawaii',
              'icc', 'los_angeles_nations', 'miami', 'mls_all_star', 'mls_combine', 'pegaso', 'super_cup', 'tecate', 'wfc',
              ]: #'los_angeles', 'miami_cup', 'women',
        load_games_standard('us_friendly', 'games/friendly/%s' % e)


def load_competitions():
    from metadata.parse import confederations, competitions, seasons
    print("Loading competitions.")

    soccer_db.confederations.drop()
    generic_load(soccer_db.confederations, confederations.load_confederations)

    generic_load(soccer_db.competitions, competitions.load_competitions)
    generic_load(soccer_db.seasons, seasons.load_seasons)

    soccer_db.competition_relations.drop()
    generic_load(soccer_db.competition_relations, competitions.load_competition_relations)


def load_teams():
    from metadata.parse import teams
    print("Loading teams.")
    generic_load(soccer_db.teams, teams.load)


def load_salaries():
    from soccerdata.text import salaries

    generic_load(soccer_db.salaries, salaries.load_salaries)


def load_drafts():
    from metadata.parse import drafts

    generic_load(soccer_db.drafts, drafts.load_drafts)
    generic_load(soccer_db.picks, drafts.load_picks)


def load_transactions():
    pass


def load_jobs():
    from soccerdata.text import positions, p2
    #print("Loading jobs.")

    jobs = os.path.join(ROOT_DIR, 'soccerdata/data/jobs/')

    # This is messed up. 
    # Terribly.
    # Need to address badly.

    # Or merge into transactions?
    

    #f1 = lambda: p2.process_file(os.path.join(jobs, 'world/england'), 'Head Coach')
    #f1 = lambda: p2.process_file(os.path.join(jobs, 'world/argentina'), 'Head Coach')

    #f2 = lambda: p2.process_file(os.path.join(jobs, 'usa/d1/mls/head'), 'Head Coach', delimiter=';')
    #f2 = lambda: p2.process_file(os.path.join(jobs, 'usa/d1/nasl/head'), 'Head Coach', delimiter=';')
    #f2 = lambda: p2.process_file(os.path.join(jobs, 'usa/d1/asl/head'), 'Head Coach', delimiter=';')

    #f2 = lambda: p2.process_file(os.path.join(jobs, 'usa/d2/nasl/head'), 'Head Coach', delimiter=';')
    #f2 = lambda: p2.process_file(os.path.join(jobs, 'usa/d2/ussfd2'), 'Head Coach', delimiter=';')
    #f2 = lambda: p2.process_file(os.path.join(jobs, 'usa/d3/uslpro'), 'Head Coach', delimiter=';')

    #generic_load(soccer_db.positions, positions.process_positions)
    #generic_load(soccer_db.positions, f1)
    #generic_load(soccer_db.positions, f2)


def load_copa_america():
    from parse.parse import rosters
    from metadata.parse.cmp import copaamerica

    coll = 'conmebol_i'
    games, goals, fouls, lineups = copaamerica.process_copa_files()

    generic_load(soccer_db['%s_games' % coll], lambda: games, delete=False)
    generic_load(soccer_db['%s_lineups' % coll], lambda: lineups, delete=False)
    generic_load(soccer_db['%s_fouls' % coll], lambda: fouls, delete=False)
    generic_load(soccer_db['%s_goals' % coll], lambda: goals, delete=False)

    generic_load(soccer_db.conmebol_i_rosters, lambda: rosters.process_rosters('rosters/copa_america', root=INTERNATIONAL_DIR))
    load_games_standard('conmebol_i', 'games/confederation/conmebol/copa_america/stadia',  root=INTERNATIONAL_DIR)

    
def load_asl():
    from usd1_data.parse import asl
    from metadata.parse import awards

    generic_load(soccer_db.asl_awards, awards.process_asl_awards, delete=False)
    generic_load(soccer_db.asl_awards, awards.process_esl_awards, delete=False)

    DIR = os.path.join(ROOT_DIR, 'usd1_data/data')

    load_standings_standard('asl', 'standings/asl', DIR)

    # Colin Jose data
    #generic_load(soccer_db.asl_goals, asl.process_asl_goals)
    #generic_load(soccer_db.asl_games, asl.process_asl_games)
    generic_load(soccer_db.asl_stats, asl.process_stats)

    for e in range(1921, 1932):
        load_games_standard('asl', 'data/games/asl/jose/%s' % e, USD1_DIR)

    for e in range(1921, 1934):
        load_games_standard('asl', 'data/games/asl/%s' % e, USD1_DIR)

    load_games_standard('asl', 'data/games/asl/esl', USD1_DIR)

    generic_load(soccer_db.asl_rosters, lambda: flatten_stats(soccer_db.asl_stats.find()))


def load_alpf():
    load_games_standard('alpf', 'data/games/alpf', USD1_DIR)
    load_standings_standard('alpf', 'data/standings/alpf', USD1_DIR)


def load_asl2():
    from metadata.parse import awards
    #from soccerdata.text import partial
    from parse.parse import rosters

    generic_load(soccer_db.us_minor_awards, awards.process_asl2_awards, delete=False)
    #generic_load(soccer_db.us_minor_stats, partial.process_asl2_partial)

    load_standings_standard('us_minor', 'standings/d2/asl2', US_MINOR_DIR)

    generic_load(soccer_db.us_minor_rosters, lambda: rosters.process_rosters2(path=os.path.join(US_MINOR_DIR, "rosters/asl2")))

    for e in range(1933, 1951):
        load_games_standard('us_minor', 'games/d2/asl2/allaway/%s' % e, root=US_MINOR_DIR)

    for e in range(1933, 1984):
        load_games_standard('us_minor', 'games/d2/asl2/sd/%s' % e, games_only=True, root=US_MINOR_DIR)



def load_nasl():
    """
    Load stats from the old nasl and misl.
    """

    from metadata.parse import awards
    from parse.parse import rosters
    from usd1_data.parse import nasl

    generic_load(soccer_db.nasl_awards, awards.process_nasl_awards)
    generic_load(soccer_db.nasl_awards, awards.process_usa_awards)
    generic_load(soccer_db.nasl_awards, awards.process_npsl_awards)
    generic_load(soccer_db.nasl_rosters, lambda: rosters.process_rosters2(os.path.join(ROOT_DIR, 'usd1_data/data/rosters/nasl')))

    generic_load(soccer_db.nasl_stats, stats.process_stats("data/stats/nasl", source='nasljerseys.com', root=USD1_DIR))


    print("Loading NASL data.")
    load_standings_standard('nasl', 'data/standings/nasl', USD1_DIR)
    load_standings_standard('nasl', 'data/standings/nasl0', USD1_DIR)

    load_games_standard('nasl', 'data/games/playoffs/nasl', USD1_DIR)

    generic_load(soccer_db.nasl_games, nasl.process_npsl_games)
    generic_load(soccer_db.nasl_goals, nasl.process_npsl_goals)
    load_games_standard('nasl', 'data/games/league/simple/usa', USD1_DIR)

    # Need to work some integrity issues on games.
    generic_load(soccer_db.nasl_games, nasl.process_nasl_games)
    generic_load(soccer_db.nasl_goals, nasl.process_nasl_goals)
    generic_load(soccer_db.nasl_lineups, nasl.process_nasl_lineups)




def load_indoor():
    """
    Load stats and games from the MISL, standings from MISL, APSL and WSA.
    """

    from metadata.parse import awards

    generic_load(soccer_db.indoor_awards, awards.process_indoor_awards)

    # standings

    load_standings_standard('indoor', 'data/standings/nasl', root=INDOOR_DIR)
    load_standings_standard('indoor', 'data/standings/misl', root=INDOOR_DIR)
    #load_standings_standard('indoor', 'data/standings/misl2', root=INDOOR_DIR)
    load_standings_standard('indoor', 'data/standings/aisa', root=INDOOR_DIR) # /npsl?
    load_standings_standard('indoor', 'data/standings/cisl', root=INDOOR_DIR)
    load_standings_standard('indoor', 'data/standings/eisl', root=INDOOR_DIR)
    load_standings_standard('indoor', 'data/standings/misl3', root=INDOOR_DIR)
    load_standings_standard('indoor', 'data/standings/usisl', root=INDOOR_DIR)
    #load_standings_standard('indoor', 'data/standings/usl', root=INDOOR_DIR)
    load_standings_standard('indoor', 'data/standings/pasl', root=INDOOR_DIR)

    # games


    for e in [1975, 1976, 1980, 1981]:
        load_games_standard('indoor', 'data/games/nasl/%s' % e, root=INDOOR_DIR)

    for e in range(1978, 1992):
        load_games_standard('indoor', 'data/games/misl/%s' % e, root=INDOOR_DIR)

    for e in range(2001, 2008):
        load_games_standard('indoor', 'data/games/misl2/%s' % e, root=INDOOR_DIR)

    for e in range(2009, 2013): # add 2008, 2013-2014.
        load_games_standard('indoor', 'data/games/misl3/%s' % e, root=INDOOR_DIR)

    for e in range(1993, 1998):
        load_games_standard('indoor', 'data/games/cisl/%s' % e, root=INDOOR_DIR)

    for e in range(1998, 2002):
        load_games_standard('indoor', 'data/games/wisl/%s' % e, root=INDOOR_DIR)

    load_games_standard('indoor', 'data/games/xsl/2008', root=INDOOR_DIR)


    # Team-specific

    #for e in range(1984, 2002):
    #    load_games_standard('indoor', 'sidekicks/data/games/%s' % e, root=TEAM_DIR)


    #for e in range(2013, 2013):
    #    load_games_standard('indoor', 'games/pasl/%s' % e, root=INDOOR_DIR)

    # stats

    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/nasl/nasl", root=INDOOR_DIR))
    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/misl/misl", root=INDOOR_DIR))
    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/misl2", root=INDOOR_DIR))
    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/misl3", root=INDOOR_DIR))
    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/cisl", root=INDOOR_DIR))
    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/aisa", root=INDOOR_DIR))
    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/wisl", root=INDOOR_DIR))
    generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/npsl", root=INDOOR_DIR))
    #generic_load(soccer_db.indoor_stats, stats.process_stats("data/stats/pasl", source='nasljerseys.com', root=INDOOR_DIR))



def load_mls_lineup_db():
    from usd1_data.parse import lineupdb
    # MLS lineup data 1996-2010 from http://usasoccer.blogspot.com/

    print("Loading scaryice score data.")
    generic_load(soccer_db.mls_games, lineupdb.load_all_games_scaryice)

    print("Loading scaryice goal data.")
    generic_load(soccer_db.mls_goals, lineupdb.load_all_goals_scaryice)
    
    print( "Loading scaryice lineup data.")
    generic_load(soccer_db.mls_lineups, lineupdb.load_all_lineups_scaryice)




def load_us_minor():
    """
    Load all-time us minor league stats.
    """


    load_modern_minor()

    #load_asl2()
    #load_nafbl()
    #load_city()


def load_modern_minor():

    #from foulds.sites import nasl, uslsoccer
    from metadata.parse import awards
    #from soccerdata.text import  partial

    from parse.parse import rosters

    generic_load(soccer_db.us_minor_awards, awards.process_usl_awards)
    generic_load(soccer_db.us_minor_awards, awards.process_ussf2_awards)
    generic_load(soccer_db.us_minor_awards, awards.process_nasl2_awards)
    generic_load(soccer_db.us_minor_awards, awards.process_apsl_awards)
    generic_load(soccer_db.us_minor_awards, awards.process_pdl_awards)

    #generic_load(soccer_db['us_lower_games'], uslsoccer.scrape_2013_games) 
    #generic_load(soccer_db['us_lower_goals'], uslsoccer.scrape_2013_goals)
    #generic_load(soccer_db['us_lower_gstats'], uslsoccer.scrape_2013_game_stats) # Fix stat generation

    #generic_load(soccer_db['us_lower_games'], nasl.scrape_all_games)
    #generic_load(soccer_db['us_lower_goals'], nasl.scrape_all_goals)
    #generic_load(soccer_db['us_lower_gstats'], nasl.scrape_all_game_stats)
             

    # early
    load_standings_standard('us_minor', 'standings/d2/apsl', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d2/wsa', root=US_MINOR_DIR) # missing 1990 wsl standings
    load_standings_standard('us_minor', 'standings/minor/lssa', root=US_MINOR_DIR)

    # modern

    # d2

    # Missing 1996 USL First Division results (there is no USL1 in 1996?)

    load_standings_standard('us_minor', 'standings/d2/usl0', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d2/premier', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d2/usisl', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d2/12', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d2/ussf2', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d2/nasl2', root=US_MINOR_DIR)

    # d3
    load_standings_standard('us_minor', 'standings/d3/pro', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d3/usl_pro', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d3/select', root=US_MINOR_DIR)
 
   # d4
    """
    load_standings_standard('us_minor', 'standings/d4/pdl', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d4/pdl_2012', root=US_MINOR_DIR)
    load_standings_standard('us_minor', 'standings/d4/pdl_2013', root=US_MINOR_DIR)
    """

    # stats


    print("loading apsl stats")
    apsl_stats = stats.process_stats("stats/d2/apsl", root=US_MINOR_DIR)
    generic_load(soccer_db.us_minor_stats, apsl_stats)
    #generic_load(soccer_db.us_minor_stats, partial.process_apsl_partial)

    generic_load(soccer_db.us_minor_stats, process_usl1_stats)

    #for e in range(2011, 2016):
    for e in range(2011, 2014):
        generic_load(soccer_db.us_minor_stats, stats.process_stats("stats/d2/%s" % e, root=US_MINOR_DIR, delimiter=';'))

    generic_load(soccer_db.us_minor_stats, process_usl2_stats)
    #generic_load(soccer_db.us_minor_stats, process_pdl_stats)


    generic_load(soccer_db.us_minor_rosters, lambda: rosters.process_rosters3('rosters/d2/2012', root=US_MINOR_DIR))

    generic_load(soccer_db.us_minor_rosters, lambda: rosters.process_rosters3('rosters/d2/2014', root=US_MINOR_DIR))

    generic_load(soccer_db.us_minor_rosters, lambda: flatten_stats(soccer_db.us_minor_stats.find()))

    # games
    for e in range(1984, 2016):
        load_games_standard('us_minor', 'games/d2/modern/%s' % e, root=US_MINOR_DIR)

    for e in range(2003, 2016):
        load_games_standard('us_minor', 'games/d3/%s' % e, root=US_MINOR_DIR)


    """
    for e in range(1985, 1991):
        load_games_standard('us_minor', 'games/d3/wsa/%s' % e, root=US_MINOR_DIR)


    # Adapt parse.games to handle PDL hours correctly.
    for e in range(2007, 2015):
        load_games_standard('us_minor', 'games/d4/pdl/%s' % e, root=US_MINOR_DIR)
    """

    load_games_standard('us_minor', 'games/playoffs/apsl', root=US_MINOR_DIR)
    load_games_standard('us_minor', 'games/playoffs/wsa', root=US_MINOR_DIR)
    #load_games_standard('us_minor', 'games/apsl_professional', root=CUPS_DIR)  # this is a league cup.
    load_games_standard('us_minor', 'games/playoffs/usl1', root=US_MINOR_DIR)
    load_games_standard('us_minor', 'games/playoffs/usl2', root=US_MINOR_DIR)


def load_afc():

    #load_standings_standard('afc', 'standings/iran', root=AFC_DIR)
    #load_standings_standard('afc', 'standings/iraq', root=AFC_DIR)
    #load_standings_standard('afc', 'standings/saudi_arabia', root=AFC_DIR)
    #load_standings_standard('afc', 'standings/qatar', root=AFC_DIR)
    #load_standings_standard('afc', 'standings/uae', root=AFC_DIR)
    #load_standings_standard('afc', 'standings/uzbekistan', root=AFC_DIR)

    #load_standings_standard('afc', 'standings/india', root=AFC_DIR)

    load_australia()    
    load_east_asia()
    

    for e in range(2001, 2013):
        load_games_standard('afc', 'games/iran/%s' % e, root=AFC_DIR)

    for e in range(2011, 2014):
        load_games_standard('afc', 'games/india/%s' % e, root=AFC_DIR)

    for e in range(2010, 2014):
        load_games_standard('afc', 'games/uzbekistan/%s' % e, root=AFC_DIR)

    for e in range(2003, 2014):
        load_games_standard('afc', 'games/saudi_arabia/%s' % e, root=AFC_DIR)

    for e in range(2005, 2010):
        load_games_standard('afc', 'games/uae/%s' % e, root=AFC_DIR)

    for e in range(1997, 2010):
        load_games_standard('afc', 'games/qatar/%s' % e, root=AFC_DIR)


def load_east_asia():
    from metadata.parse import awards

    load_standings_standard('afc', 'standings/china', root=AFC_DIR)
    load_standings_standard('afc', 'standings/japan', root=AFC_DIR)
    load_standings_standard('afc', 'standings/korea', root=AFC_DIR)

    #load_standings_standard('afc', 'standings/thailand', root=AFC_DIR)
    #load_standings_standard('afc', 'standings/vietnam', root=AFC_DIR)
    #load_standings_standard('afc', 'standings/indonesia', root=AFC_DIR)

    generic_load(soccer_db.afc_awards, awards.process_china_awards)
    generic_load(soccer_db.afc_awards, awards.process_japan_awards)
    generic_load(soccer_db.afc_awards, awards.process_korea_awards)

    for e in range(2004, 2014):
        load_games_standard('afc', 'games/china/1/%s' % e, root=AFC_DIR)

    for e in range(1997, 2014):
        load_games_standard('afc', 'games/japan/1/%s' % e, root=AFC_DIR)

    for e in range(1983, 2014):
        load_games_standard('afc', 'games/korea/1/%s' % e, root=AFC_DIR)

    return

    for e in range(2011, 2012):
        load_games_standard('afc', 'games/vietnam/%s' % e, root=AFC_DIR)

    for e in range(2012, 2012):
        load_games_standard('afc', 'games/thailand/%s' % e, root=AFC_DIR)

    for e in range(2012, 2012):
        load_games_standard('afc', 'games/indonesia/%s' % e, root=AFC_DIR)


def load_australia():
    from metadata.parse import awards

    generic_load(soccer_db.afc_awards, awards.process_australia_awards)

    load_standings_standard('afc', 'standings/australia', root=AFC_DIR)

    for season in range(2005, 2014):
        load_games_standard('afc', 'games/australia/league/%s' % season, root=AFC_DIR)

    #load_games_standard('afc', 'games/australia/playoffs', root=AFC_DIR)

    return

    from foulds.sites.australia import scrape_aleague

    games, goals, lineups = scrape_aleague()
    generic_load(soccer_db['afc_games'], lambda: [e for e in games if e not in [{}, None]])
    generic_load(soccer_db['afc_goals'], lambda: [e for e in goals if e not in [{}, None]])
    generic_load(soccer_db['afc_lineups'], lambda: [e for e in lineups if e not in [{}, None]])



def load_mexico():
    from metadata.parse import awards

    generic_load(soccer_db.mexico_awards, awards.process_mexico_awards)

    #load_standings_standard('mexico', 'standings/mexico/primera_fuerza', root=CONCACAF_DIR)
    load_standings_standard('mexico', 'standings/mexico/1', CONCACAF_DIR)
    load_standings_standard('mexico', 'standings/mexico/short', CONCACAF_DIR)
    load_standings_standard('mexico', 'standings/mexico/ascenso', CONCACAF_DIR)

    for e in range(1970, 2014):
        load_games_standard('mexico', 'games/country/mexico/league/%s' % e, CONCACAF_DIR)

    for e in range(2001, 2014):
        load_games_standard('mexico', 'games/country/mexico/ascenso/%s' % e, CONCACAF_DIR)

    for e in range(1970, 2020, 10):
        load_games_standard('mexico', 'games/country/mexico/playoffs/%s' % e, CONCACAF_DIR)

        
    # league
    load_games_standard('mexico', 'games/country/mexico/league/1943', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/league/1963', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/league/1964', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/league/1967', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/league/1970mexico', CONCACAF_DIR)


    # Cups
    load_games_standard('mexico', 'games/country/mexico/interliga', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/pre_libertadores', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/super', CONCACAF_DIR)

    # Friendlies.
    load_games_standard('mexico', 'games/country/mexico/friendly/adolfo_lopez_mateos', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/agosto', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/chiapas', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/corona', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/gol', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/guadalajara', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/guadalajara2', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/guadalajara3', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/hidalgo', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/leon', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/mesoamericana', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/mexico_city', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/mexico_city2', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/milenio', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/monterrey', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/nike', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/pentagonal2', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/puebla', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/quadrangular', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/queretaro', CONCACAF_DIR)

    load_games_standard('mexico', 'games/country/mexico/friendly/tijuana', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/toluca', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/torreon', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/tour', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/universidades', CONCACAF_DIR)
    load_games_standard('mexico', 'games/country/mexico/friendly/veracruz', CONCACAF_DIR)


def load_ofc():
    load_games_standard('oceania', 'domestic/confederation/ofc/wantok')


def load_oceania_international():

    for e in range(1986, 2018, 4):
        load_games_standard('oceania_i', 'games/confederation/ofc/wcq/%s' % e, INTERNATIONAL_DIR)

    load_games_standard('oceania_i', 'games/confederation/ofc/cups/melanesia', INTERNATIONAL_DIR)
    load_games_standard('oceania_i', 'games/confederation/ofc/cups/polynesia', INTERNATIONAL_DIR)
    load_games_standard('oceania_i', 'games/confederation/ofc/cups/nations', INTERNATIONAL_DIR)


def load_uefa_international():
    load_games_standard('uefa_i', 'games/country/france', INTERNATIONAL_DIR)
    #load_games_standard('uefa_i', 'games/country/slovenia', INTERNATIONAL_DIR)

    #load_games_standard('uefa_i', 'games/country/netherlands', INTERNATIONAL_DIR)
    #load_games_standard('uefa_i', 'games/country/belgium', INTERNATIONAL_DIR)
    #load_games_standard('uefa_i', 'games/country/austria', INTERNATIONAL_DIR)
    #load_games_standard('uefa_i', 'games/country/hungary', INTERNATIONAL_DIR)

    return

    load_games_standard('uefa_i', 'games/country/germany', INTERNATIONAL_DIR)
    load_games_standard('uefa_i', 'games/country/spain', INTERNATIONAL_DIR)
    load_games_standard('uefa_i', 'games/country/italy', INTERNATIONAL_DIR)
    load_games_standard('uefa_i', 'games/country/sweden', INTERNATIONAL_DIR)
    load_games_standard('uefa_i', 'games/country/norway', INTERNATIONAL_DIR)
    load_games_standard('uefa_i', 'games/country/denmark', INTERNATIONAL_DIR)
    load_games_standard('uefa_i', 'games/country/portugal', INTERNATIONAL_DIR)



def load_asia_international():
    return
    load_games_standard('afc_i', 'games/country/south_korea', INTERNATIONAL_DIR)
    load_games_standard('afc_i', 'games/country/north_korea', INTERNATIONAL_DIR)

    for e in range(195, 201):
        load_games_standard('afc_i', 'games/country/japan/%s0' % e, INTERNATIONAL_DIR)


def load_africa_international():
    return
    load_games_standard('caf_i', 'games/country/nigeria', INTERNATIONAL_DIR)
    load_games_standard('caf_i', 'games/country/cameroon', INTERNATIONAL_DIR)
    load_games_standard('caf_i', 'games/country/ghana', INTERNATIONAL_DIR)


def load_mixed_confederation():

    load_games_standard('world', 'games/confederation/mixed/panpacific', WORLD_DIR)
    load_games_standard('world', 'games/confederation/mixed/interamerican', WORLD_DIR)
    load_games_standard('world', 'games/confederation/mixed/suruga', WORLD_DIR)

    for e in [1960, 1970, 1980, 1990, 2000]:
        load_games_standard('world', 'games/confederation/mixed/intercontinental/%s' % e, WORLD_DIR)



def load_conmebol():
    from metadata.parse import awards

    load_conmebol_leagues()

    generic_load(soccer_db.conmebol_awards, awards.process_conmebol_awards)

    for e in range(1960, 2014):
        load_games_standard('conmebol', 'games/confederation/libertadores/%s' % e, CONMEBOL_DIR)

    load_games_standard('conmebol', 'games/confederation/recopa_sudamericana', CONMEBOL_DIR)
    load_games_standard('conmebol', 'games/confederation/sacc', CONMEBOL_DIR)

    load_games_standard('conmebol', 'games/confederation/merconorte', CONMEBOL_DIR)
    load_games_standard('conmebol', 'games/confederation/mercosur', CONMEBOL_DIR)
    load_games_standard('conmebol', 'games/confederation/mercosul', CONMEBOL_DIR)

    for e in range(1992, 2000):
        load_games_standard('conmebol', 'games/confederation/conmebol/%s' % e, CONMEBOL_DIR)

    for e in range(2002, 2013):
        load_games_standard('conmebol', 'games/confederation/sudamericana/%s' % e, CONMEBOL_DIR)

    #load_games_standard('conmebol', 'games/confederation/aldao', CONMEBOL_DIR)
    #load_games_standard('conmebol', 'games/confederation/copa_ibarguren', CONMEBOL_DIR)

    #load_games_standard('conmebol', 'games/confederation/copa_tie', CONMEBOL_DIR)
    #load_games_standard('conmebol', 'games/confederation/masters', CONMEBOL_DIR)


def load_conmebol_international():
    from metadata.parse import awards
    generic_load(soccer_db.conmebol_i_awards, awards.process_conmebol_international_awards)

    for year in range(1958, 2015, 4):
        load_games_standard('conmebol_i', 'games/confederation/conmebol/wcq/%s' % year, INTERNATIONAL_DIR)

    load_copa_america()

    load_games_standard('conmebol_i', 'games/confederation/conmebol/early/sa', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/confederation/conmebol/early/premio', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/confederation/conmebol/early/atlantico', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/confederation/conmebol/early/newton', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/confederation/conmebol/early/lipton', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/confederation/conmebol/early/mayo', INTERNATIONAL_DIR)

    load_games_standard('conmebol_i', 'games/country/argentina', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/country/bolivia', INTERNATIONAL_DIR)
    #load_games_standard('conmebol_i', 'games/country/brazil', INTERNATIONAL_DIR)
    load_brazil_international()
    load_games_standard('conmebol_i', 'games/country/chile', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/country/colombia', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/country/ecuador', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/country/paraguay', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/country/peru', INTERNATIONAL_DIR)
    load_games_standard('conmebol_i', 'games/country/uruguay', INTERNATIONAL_DIR),
    load_games_standard('conmebol_i', 'games/country/venezuela', INTERNATIONAL_DIR)


def load_cfu():
    from metadata.parse import awards
    generic_load(soccer_db.concacaf_awards, awards.process_cfu_awards)

    load_games_standard('concacaf', 'games/confederation/cfu/1990', CONCACAF_DIR)
    load_games_standard('concacaf', 'games/confederation/cfu/2000', CONCACAF_DIR)
    load_games_standard('concacaf', 'games/confederation/cfu/2010', CONCACAF_DIR)

    # league results
    
    #load_standings_standard('concacaf', 'standings/bermuda', CONCACAF_DIR)
    #load_standings_standard('concacaf', 'standings/trinidad', CONCACAF_DIR)
    #load_standings_standard('concacaf', 'standings/curacao', CONCACAF_DIR)
    #load_standings_standard('concacaf', 'standings/martinique', CONCACAF_DIR)
    #load_standings_standard('concacaf', 'standings/jamaica', CONCACAF_DIR)


    for year in range(2001, 2012):
        load_games_standard('concacaf', 'games/country/jamaica/league/%s' % year, CONCACAF_DIR)

    for year in range(2002, 2012):
        load_games_standard('concacaf', 'games/country/trinidad/league/%s' % year, CONCACAF_DIR)

    for year in range(2012, 2012):
        load_games_standard('concacaf', 'games/country/cuba/%s' % year, CONCACAF_DIR)

    for year in range(2010, 2014):
        load_games_standard('concacaf', 'games/country/haiti/1/%s' % year, CONCACAF_DIR)



def load_uncaf_international():
    from metadata.parse import awards

    #generic_load(soccer_db.concacaf_i_awards, awards.process_uncaf_international_awards)

    load_games_standard('concacaf_i', 'games/confederation/concacaf/uncaf', INTERNATIONAL_DIR)

    load_games_standard('concacaf_i', 'games/country/belize', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/costa_rica', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/el_salvador', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/guatemala', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/honduras', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/nicaragua', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/panama', INTERNATIONAL_DIR)


def load_world_international():
    from metadata.parse import awards
    from parse.parse import rosters

    generic_load(soccer_db.world_i_awards, awards.process_world_cup_awards)
    generic_load(soccer_db.world_i_awards, awards.process_olympics_awards)

    #generic_load(soccer_db.world_i_rosters, lambda: rosters.process_rosters(olympics'))
    #generic_load(soccer_db.world_i_rosters, lambda: rosters.process_rosters2(os.path.join('soccerdata/data/rosters/international/confederations')))

    confed = [1992, 1995, 1997, 1999, 2001, 2003, 2005, 2009, 2013]

    for e in confed:
        load_games_standard('world_i', 'games/world/confederations/%s' % e, INTERNATIONAL_DIR)

    for e in [1930, 1934] + list(range(1950, 2015, 4)):
        load_games_standard('world_i', 'games/world/world_cup/%s' % e, INTERNATIONAL_DIR)

    #load_games_standard('world_i', 'international/world/u17')

    load_games_standard('world_i', 'games/world/artemio_franchi', INTERNATIONAL_DIR)
    #load_games_standard('world_i', 'games/world/interallied', INTERNATIONAL_DIR)
    load_games_standard('world_i', 'games/world/mundialito', INTERNATIONAL_DIR)

    olympics = [1900, 1904, 1908, 1912, 1920, 1924, 1928, 1936] + list(range(1948, 2000, 4))
    # list(range(1948, 2013, 4))

    return

    # Merge olympic data.
    for e in olympics:
        load_games_standard('world_i', 'games/world/olympics/%s' % e, INTERNATIONAL_DIR, games_only=True)

    for e in range(1977, 2014, 2):
        load_games_standard('world_i', 'games/world/u20/%s' % e, INTERNATIONAL_DIR)



def load_isl2():
    from metadata.parse import awards
    from parse.parse import rosters

    h = lambda fn: os.path.join(ISL_DIR, fn)

    load_games_standard('world', h('games'), ISL_DIR)
    load_standings_standard('world', h('standings'), ISL_DIR)
    generic_load(soccer_db.world_rosters, lambda: rosters.process_rosters2(h('rosters')))
    generic_load(soccer_db.world_awards, awards.process_isl_awards) # isl et al.


def load_world():
    from metadata.parse import awards
    from parse.parse import rosters
    generic_load(soccer_db.world_awards, awards.process_world_awards)

    load_mixed_confederation()

    # Club World Cup
    for e in [2000, 2001] + list(range(2005, 2014)):
        load_games_standard('world', 'games/world/club_world_cup/%s' % e, WORLD_DIR)

                      
    # International friendly club tournaments - ISL, Parmalat Cup, Copa Rio, etc.
    # Also existed in Brazil / Argentina / Colombia?

    #generic_load(soccer_db.world_rosters, lambda: rosters.process_rosters2(os.path.join(WORLD_DIR, 'rosters/domestic/cwc/2014')))
    #generic_load(soccer_db.world_rosters, lambda: rosters.process_rosters2(os.path.join(WORLD_DIR, 'rosters/domestic/copita')))

    #load_isl2()

    #load_games_standard('world', 'domestic/country/mexico/friendly/palmares')

    #load_games_standard('world', 'domestic/world/parmalat')
    #load_games_standard('world', 'domestic/world/copa_rio')
    #load_games_standard('world', 'domestic/confederation/conmebol/pequena')
    #load_games_standard('world', 'games/misc/fifa_world_stars_games', INTERNATIONAL_DIR)


def load_caribbean_international():
    from metadata.parse import awards

    generic_load(soccer_db.concacaf_i_awards, awards.process_caribbean_awards)

    load_games_standard('concacaf', 'games/confederation/concacaf/caribbean/cfu', INTERNATIONAL_DIR)
    load_games_standard('concacaf', 'games/confederation/concacaf/caribbean/1980', INTERNATIONAL_DIR)
    load_games_standard('concacaf', 'games/confederation/concacaf/caribbean/1990', INTERNATIONAL_DIR)
    load_games_standard('concacaf', 'games/confederation/concacaf/caribbean/2001', INTERNATIONAL_DIR)

    load_games_standard('concacaf_i', 'games/country/anguilla', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/antigua', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/aruba', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/bahamas', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/barbados', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/bermuda', INTERNATIONAL_DIR)    
    load_games_standard('concacaf_i', 'games/country/bvi', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/cayman', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/cuba', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/dominica', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/dr', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/french_guyana', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/grenada', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/guadeloupe', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/guyana', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/haiti', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/jamaica', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/martinique', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/montserrat', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/puerto_rico', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/nevis', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/st_lucia', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/saint_martin', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/st_vincent', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/sint_maarten', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/suriname', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/trinidad_tobago', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/turks_caicos', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/country/usvi', INTERNATIONAL_DIR)

    #load_games_standard('concacaf_i', 'games/country/saint_croix', INTERNATIONAL_DIR)
    #load_games_standard('concacaf_i', 'games/country/saint_thomas', INTERNATIONAL_DIR)    
    #load_games_standard('concacaf_i', 'games/country/tortola', INTERNATIONAL_DIR)
    #load_games_standard('concacaf_i', 'games/country/virgin_gorda', INTERNATIONAL_DIR)


def load_usmnt():
    from metadata.parse import awards

    generic_load(soccer_db.usa_awards, awards.load_hall_of_fame)

                      
    root = os.path.join(ROOT_DIR, 'usmnt_data')

    for e in range(1910, 2020, 10):
        load_games_standard('usa', 'games/%s' % e, root)

    load_games_standard('usa', 'games/world_cup', root)
    load_games_standard('usa', 'games/unofficial/us_cup', root)
    load_games_standard('usa', 'games/unofficial/friendly', root)

    
def load_concacaf_international():
    from metadata.parse import awards
    generic_load(soccer_db.concacaf_i_awards, awards.process_concacaf_international_awards)

    # World Cup qualifying
    for year in range(1994, 2015, 4):
        load_games_standard('concacaf_i', 'games/confederation/concacaf/wcq/%s' % year, INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/confederation/concacaf/wcq/world_cup_qualifying', INTERNATIONAL_DIR)

    # Olympic qualifying
    for year in range(2000, 2014, 4):
        load_games_standard('concacaf_i', 'games/confederation/concacaf/olympic/%s' % year, INTERNATIONAL_DIR)

    # U-20 World Cup qualifying
    for year in [2009, 2011, 2013]:
        load_games_standard('concacaf_i', 'games/confederation/concacaf/u20/%s' % year, INTERNATIONAL_DIR)

    # U-17 World Cup qualifying (incomplete)
    for year in [2009, 2011, 2013]:
        load_games_standard('concacaf_i', 'games/confederation/concacaf/u17/%s' % year, INTERNATIONAL_DIR)

    # Gold Cup and predecessors
    load_games_standard('concacaf_i', 'games/confederation/concacaf/gold/championship', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/confederation/concacaf/gold/cccf', INTERNATIONAL_DIR)

    for e in [1991, 1993, 1996, 1998, 2000, 2002, 2003, 2005, 2007, 2009, 2011, 2013]:
        load_games_standard('concacaf_i', 'games/confederation/concacaf/gold/%s' % e, INTERNATIONAL_DIR)

    # Miscellaneous
    load_games_standard('concacaf_i', 'games/confederation/concacaf/cacg', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/confederation/concacaf/martinez', INTERNATIONAL_DIR)
    load_games_standard('concacaf_i', 'games/confederation/concacaf/independence', INTERNATIONAL_DIR)
    load_games_standard('cloncacaf_i', 'games/confederation/concacaf/friendly', INTERNATIONAL_DIR)

    #load_panamerican()
    #generic_load(soccer_db.concacaf_i_awards, awards.process_panamerican_awards)

    #for e in [1951, 1955, 1959, 1963, 1967, 1971, 1975, 1979, 1983, 1987, 
    #          1991, 1995, 1999, 2003, 2007]:
    #    load_games_standard('concacaf_i', 'games/world/panamerican/%s' % e, INTERNATIONAL_DIR)


    # Results by team
    load_uncaf_international()
    load_caribbean_international()
    load_usmnt()
    load_games_standard('canada', 'games/country/canada/1900', INTERNATIONAL_DIR)
    load_games_standard('canada', 'games/country/canada/2000', INTERNATIONAL_DIR)
    load_games_standard('mexico', 'games/country/mexico/alltime', INTERNATIONAL_DIR)


def load_concacaf():
    from metadata.parse import awards
    from parse.parse import rosters

    for e in range(2008, 2012):
        generic_load(soccer_db.concacaf_rosters, lambda: rosters.process_rosters3('rosters/league/%s' % e, CONCACAF_DIR))


    generic_load(soccer_db.concacaf_awards, awards.process_concacaf_awards)

    for e in range(2008, 2014):
        load_games_standard('concacaf', 'games/confederation/champions/league/%s' % e, CONCACAF_DIR)

    return

    load_games_standard('concacaf', 'games/confederation/defunct/superliga', CONCACAF_DIR)
    load_games_standard('concacaf', 'games/confederation/defunct/giants', CONCACAF_DIR)
    load_games_standard('concacaf', 'games/confederation/defunct/recopa', CONCACAF_DIR)


    for e in [1960, 1970, 1980, 1990, 2000]:
        load_games_standard('concacaf', 'games/confederation/champions/%s' % e, CONCACAF_DIR)



    load_canada()
    load_mexico()
    load_cfu()
    load_uncaf()



def load_amateur():
    load_ncaa()
    # Olympics?


def load_ncaa():
    from metadata.parse import awards
    generic_load(soccer_db.ncaa_awards, awards.process_ncaa_awards)

    load_standings_standard('ncaa', 'standings/ncaa2', root=NCAA_DIR)

    #import pdb; pdb.set_trace()

    generic_load(soccer_db.ncaa_stats, process_ncaa_stats)

    #load_games_standard('ncaa', 'domestic/country/usa/college')

    for year in range(1959, 1963):
        load_games_standard('ncaa', 'games/championship/%s' % year, NCAA_DIR)

    for year in range(2011, 2014):
        load_games_standard('ncaa', 'games/championship/%s' % year, NCAA_DIR)





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





def load_ltrack():

    import ltrack_data.parse

    p = os.path.join(ROOT_DIR, 'ltrack_data/data')

    print("processing ltrack goals")
    generic_load(soccer_db.ltrack_goals, lambda: ltrack_data.parse.process_goals(p))

    print("processing ltrack games")
    generic_load(soccer_db.ltrack_games, lambda: ltrack_data.parse.process_games(p))

    print("processing ltrack lineups")
    generic_load(soccer_db.ltrack_lineups, lambda: ltrack_data.parse.process_lineups(p))


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



def process_ncaa_stats():

    l = []
    for e in [
        'akron', 
        #'berkeley',
        #'boston_college',
        'charlotte',
        #'chico',
        'clemson',
        'coastal_carolina',
        'conn',

        #'fairleigh_dickinson',
        #'fiu',

        'furman',
        'george_mason',
        'georgetown',

        #'harvard',


        #'indiana',

        'kentucky',
        'louisville',

        'maryland',
        'nc_state',
        #'new_mexico',
        'notre_dame',
        'ohio_state',
        'oregon_state',
        'penn_state',
        'rutgers',

        #'san_diego_state',
        #'san_franciso',
        #'slu',
        #'smu',
        'st_johns',
        #'stanford',

        #'uab',
        #'ucf',

        'ucla',
        
        'ucsb',

        'unc',
        'uva',
        'uwm',

        'wake_forest',
        ]:
        l.extend(stats.process_stats("stats/%s" % e, NCAA_DIR, format_name=True))
    
    return l


def process_usl1_stats():
    l = []
    l.extend(stats.process_stats("stats/d2/19972005", US_MINOR_DIR, format_name=True))

    for e in '06', '07', '08', '09':
        l.extend(stats.process_stats("stats/d2/20%s" % e, US_MINOR_DIR, format_name=True))

    return l

def process_usl2_stats():
    l = []
    l.extend(stats.process_stats("stats/d3/psl", US_MINOR_DIR, format_name=True))
    l.extend(stats.process_stats("stats/d3/20052009", US_MINOR_DIR, format_name=True))
    for e in range(2010, 2014):
        l.extend(stats.process_stats("stats/d3/%s" % e, US_MINOR_DIR, format_name=True))

    return l

def process_pdl_stats():
    l = []
    
    for e in range(2003, 2014):
        l.extend(stats.process_stats("stats/d4/%s" % e, US_MINOR_DIR, format_name=True)) 

    return l
        



if __name__ == "__main__":
    load()

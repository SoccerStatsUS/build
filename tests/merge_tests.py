
import datetime
from nose.tools import *

from soccerdata.build.merge import merge_games, merge_stats


def tst_identical_game_merge():
    games = [
        {'date': datetime.datetime(2012, 1, 1), 'season': 2012, 'team1': 'FC Dallas', 'team2': 'Colorado Rapids'},
        {'date': datetime.datetime(2012, 1, 1), 'season': 2012, 'team1': 'FC Dallas', 'team2': 'Colorado Rapids'},
        ]

    ngames = merge_games([games])
    assert_equal(len(ngames), 1)


def tst_reverse_teams_merge():
    games = [
        {'date': datetime.datetime(2012, 1, 1), 'team1': 'FC Dallas', 'team2': 'Colorado Rapids'},
        {'date': datetime.datetime(2012, 1, 1), 'team2': 'FC Dallas', 'team1': 'Colorado Rapids'},
        ]

    ngames = merge_games([games])
    assert_equal(len(ngames), 1)



def tst_location_merge():
    games = [
        {'date': datetime.datetime(2012, 1, 1), 'team1': 'FC Dallas', 'team2': 'Colorado Rapids', 'location': 'Dallas, TX'},
        {'date': datetime.datetime(2012, 1, 1), 'team2': 'FC Dallas', 'team1': 'Colorado Rapids'},
        ]

    ngames = merge_games([games])

    assert_equal(len(ngames), 1)
    assert_equal(ngames[0], 
                 {'date': datetime.datetime(2012, 1, 1), 'team1': 'FC Dallas', 'team2': 'Colorado Rapids', 'location': 'Dallas, TX'},
                 )


def tst_stats_merge():
    stats = [
        { 'name': 'Jason Kreis', 'team': 'FC Dallas', 'competition': 'MLS', 'season': '2001', 'goals': 3, 'assists': 5},
        { 'name': 'Jason Kreis', 'team': 'FC Dallas', 'competition': 'MLS', 'season': '2001', 'goals': 13, 'assists': 0},
        ]

    stats_lists = [stats]

    nstats = merge_stats(stats_lists)
    assert_equal(len(nstats), 1)
    assert_equal({ 'name': 'Jason Kreis', 'team': 'FC Dallas', 'competition': 'MLS', 'season': '2001', 'goals': 3, 'assists': 5}, nstats[0])

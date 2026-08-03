from standings import get_standings

MLS = 'Major League Soccer'


def played(home, away, home_score, away_score):
    return {
        'home_team': home, 'away_team': away,
        'home_score': home_score, 'away_score': away_score,
    }


def by_name(standings):
    return {s['name']: s for s in standings}


def test_winner_row_is_correct():
    s = by_name(get_standings([played('FC Dallas', 'Colorado Rapids', 3, 1)], MLS, '2012'))
    assert s['FC Dallas']['wins'] == 1
    assert s['FC Dallas']['losses'] == 0
    assert s['FC Dallas']['ties'] == 0
    assert s['FC Dallas']['goals_for'] == 3
    assert s['FC Dallas']['goals_against'] == 1


def test_points_are_three_per_win_plus_one_per_tie():
    games = [
        played('FC Dallas', 'Colorado Rapids', 3, 1),
        played('FC Dallas', 'Chicago Fire', 1, 1),
        played('FC Dallas', 'Real Salt Lake', 0, 2),
    ]
    s = by_name(get_standings(games, MLS, '2012'))
    assert s['FC Dallas']['wins'] == 1
    assert s['FC Dallas']['ties'] == 1
    assert s['FC Dallas']['losses'] == 1
    assert s['FC Dallas']['points'] == 4


def test_standings_are_ordered_by_points_descending():
    games = [
        played('FC Dallas', 'Colorado Rapids', 3, 1),
        played('FC Dallas', 'Chicago Fire', 2, 0),
        played('Chicago Fire', 'Colorado Rapids', 1, 0),
    ]
    points = [s['points'] for s in get_standings(games, MLS, '2012')]
    assert points == sorted(points, reverse=True)


def test_competition_and_season_are_carried_through():
    s = get_standings([played('FC Dallas', 'Colorado Rapids', 3, 1)], MLS, '2012')
    assert all(e['competition'] == MLS for e in s)
    assert all(e['season'] == '2012' for e in s)


def test_no_games_gives_no_standings():
    assert get_standings([], MLS, '2012') == []


def test_losing_team_appears_in_the_table():
    s = by_name(get_standings([played('FC Dallas', 'Colorado Rapids', 3, 1)], MLS, '2012'))
    assert s['Colorado Rapids']['wins'] == 0
    assert s['Colorado Rapids']['losses'] == 1
    assert s['Colorado Rapids']['points'] == 0
    assert s['Colorado Rapids']['goals_for'] == 1
    assert s['Colorado Rapids']['goals_against'] == 3


def test_a_round_of_draws_still_produces_a_table():
    s = by_name(get_standings([played('FC Dallas', 'Colorado Rapids', 2, 2)], MLS, '2012'))
    assert s['FC Dallas']['ties'] == 1
    assert s['Colorado Rapids']['ties'] == 1
    assert s['FC Dallas']['points'] == 1


def test_a_winless_team_still_has_a_row():
    games = [
        played('FC Dallas', 'Colorado Rapids', 3, 1),
        played('Chicago Fire', 'Colorado Rapids', 2, 0),
    ]
    s = by_name(get_standings(games, MLS, '2012'))
    assert s['Colorado Rapids']['losses'] == 2
    assert s['Colorado Rapids']['points'] == 0


def test_every_team_that_played_is_in_the_table():
    games = [
        played('FC Dallas', 'Colorado Rapids', 3, 1),
        played('Chicago Fire', 'FC Dallas', 2, 2),
        played('Colorado Rapids', 'Chicago Fire', 0, 4),
    ]
    names = {e['name'] for e in get_standings(games, MLS, '2012')}
    assert names == {'FC Dallas', 'Colorado Rapids', 'Chicago Fire'}


def test_goals_balance_across_the_table():
    games = [
        played('FC Dallas', 'Colorado Rapids', 3, 1),
        played('Chicago Fire', 'FC Dallas', 2, 2),
        played('Colorado Rapids', 'Chicago Fire', 0, 4),
    ]
    s = get_standings(games, MLS, '2012')
    assert sum(e['goals_for'] for e in s) == sum(e['goals_against'] for e in s)


def test_games_played_balance_across_the_table():
    games = [
        played('FC Dallas', 'Colorado Rapids', 3, 1),
        played('Chicago Fire', 'FC Dallas', 2, 2),
        played('Colorado Rapids', 'Chicago Fire', 0, 4),
    ]
    s = get_standings(games, MLS, '2012')
    # The invariant check_standings() enforces on loaded standings.
    assert sum(e['wins'] + e['losses'] + e['ties'] for e in s) == 2 * len(games)


def test_accepts_a_single_pass_iterable():
    # `games` is walked once, so a cursor works as well as a list.
    games = [played('FC Dallas', 'Colorado Rapids', 3, 1)]
    assert get_standings(iter(games), MLS, '2012') == get_standings(games, MLS, '2012')

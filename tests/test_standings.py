import pytest

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


# Known bugs, pinned so they announce themselves when fixed.
#
# Standing.standings() iterates `sorted(self.wins.keys())`, and `wins` is only
# populated for teams that won at least one game. Every assertion below is what
# the standings should say; strict xfail means these flip to failures the moment
# the iteration is widened to the full set of teams.

@pytest.mark.xfail(strict=True, reason='standings() iterates only wins.keys(), so a winless team is dropped')
def test_losing_team_appears_in_the_table():
    s = by_name(get_standings([played('FC Dallas', 'Colorado Rapids', 3, 1)], MLS, '2012'))
    assert s['Colorado Rapids']['losses'] == 1
    assert s['Colorado Rapids']['goals_for'] == 1
    assert s['Colorado Rapids']['goals_against'] == 3


@pytest.mark.xfail(strict=True, reason='no team has a win, so wins.keys() is empty and the table comes back empty')
def test_a_round_of_draws_still_produces_a_table():
    s = by_name(get_standings([played('FC Dallas', 'Colorado Rapids', 2, 2)], MLS, '2012'))
    assert s['FC Dallas']['ties'] == 1
    assert s['Colorado Rapids']['ties'] == 1


@pytest.mark.xfail(strict=True, reason='winless teams are missing, so their goals are absent from the totals')
def test_goals_balance_across_the_table():
    games = [
        played('FC Dallas', 'Colorado Rapids', 3, 1),
        played('Chicago Fire', 'FC Dallas', 2, 2),
        played('Colorado Rapids', 'Chicago Fire', 0, 4),
    ]
    s = get_standings(games, MLS, '2012')
    assert sum(e['goals_for'] for e in s) == sum(e['goals_against'] for e in s)


@pytest.mark.xfail(strict=True, raises=KeyError,
                   reason='Standing re-walks `games` once per column; a single-pass iterable is exhausted after the first')
def test_accepts_a_single_pass_iterable():
    # standings.py's own comment says "Games is probably a cursor object!".
    # It is not: generate.py passes a list. If that ever changes, this crashes.
    games = [played('FC Dallas', 'Colorado Rapids', 3, 1)]
    assert get_standings(iter(games), MLS, '2012') != []

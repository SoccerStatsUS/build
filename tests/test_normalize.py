import pytest

from fakedb import FakeDB
from normalize import (
    calculate_game_results,
    calculate_lineup_result,
    normalize_goal,
)


# calculate_game_results

def test_results_from_scores():
    assert calculate_game_results({'team1_score': 3, 'team2_score': 1}) == ('w', 'l')
    assert calculate_game_results({'team1_score': 1, 'team2_score': 3}) == ('l', 'w')
    assert calculate_game_results({'team1_score': 2, 'team2_score': 2}) == ('t', 't')


def test_results_from_scoreless_draw():
    assert calculate_game_results({'team1_score': 0, 'team2_score': 0}) == ('t', 't')


def test_results_unknown_when_no_scores():
    assert calculate_game_results({'team1_score': None, 'team2_score': None}) == ('', '')


def test_explicit_results_win_over_scores():
    # A recorded result beats anything inferred, e.g. a forfeit.
    d = {'team1_score': 3, 'team2_score': 1, 'team1_result': 'l', 'team2_result': 'w'}
    assert calculate_game_results(d) == ('l', 'w')


@pytest.mark.parametrize('given,expected', [
    ({'team1_result': 'w'}, ('w', 'l')),
    ({'team1_result': 'l'}, ('l', 'w')),
    ({'team2_result': 'w'}, ('l', 'w')),
    ({'team2_result': 'l'}, ('w', 'l')),
])
def test_results_from_one_sided_result_without_scores(given, expected):
    d = {'team1_score': None, 'team2_score': 1}
    d.update(given)
    assert calculate_game_results(d) == expected


# calculate_lineup_result

def test_lineup_result():
    assert calculate_lineup_result({'goals_for': 2, 'goals_against': 1}) == 'w'
    assert calculate_lineup_result({'goals_for': 1, 'goals_against': 2}) == 'l'
    assert calculate_lineup_result({'goals_for': 1, 'goals_against': 1}) == 't'


def test_lineup_result_unknown_without_goals():
    assert calculate_lineup_result({'goals_for': None, 'goals_against': 1}) is None
    assert calculate_lineup_result({'goals_for': 1, 'goals_against': None}) is None


# normalize_goal

def goal(**kw):
    e = {
        'competition': 'Major League Soccer',
        'season': '2010',
        'team': 'Seattle Sounders',
        'goal': 'Fredy Montero',
        'assists': [],
    }
    e.update(kw)
    return e


def test_normalize_goal_keeps_assists():
    e = normalize_goal(goal(assists=['Osvaldo Alonso']))
    assert e['goal'] == 'Fredy Montero'
    assert e['assists'] == ['Osvaldo Alonso']


def test_normalize_goal_unassisted_clears_assists():
    assert normalize_goal(goal(assists=['unassisted']))['assists'] == []
    assert normalize_goal(goal(assists=['ua']))['assists'] == []


def test_normalize_goal_penalty_kick_sets_flag():
    e = normalize_goal(goal(assists=['penalty kick']))
    assert e['assists'] == []
    assert e['penalty'] is True


def test_normalize_goal_free_kick_clears_assists_without_flag():
    e = normalize_goal(goal(assists=['free kick']))
    assert e['assists'] == []
    assert 'penalty' not in e


def test_normalize_goal_own_goal_moves_scorer_to_own_goal_player():
    e = normalize_goal(goal(goal='Own Goal', assists=['Fredy Montero']))
    assert e['own_goal'] is True
    assert e['goal'] is None
    assert e['own_goal_player'] == 'Fredy Montero'
    assert e['assists'] == []


def test_normalize_goal_normalizes_team_alias():
    # Dallas Burn -> FC Dallas, per README.
    e = normalize_goal(goal(team='Dallas Burn'))
    assert e['team'] == 'FC Dallas'


# make_location_normalizer

def location_normalizer(monkeypatch, stadiums):
    """A normalizer built over just these stadiums."""
    import normalize
    monkeypatch.setattr(normalize, 'soccer_db',
                        FakeDB(stadiums=[{'name': n, 'location': loc}
                                         for n, loc in stadiums]))
    return normalize.make_location_normalizer()


STUBHUB = [('StubHub Center', 'Carson, CA')]


def test_a_stadium_is_split_from_its_place(monkeypatch):
    getter = location_normalizer(monkeypatch, STUBHUB)

    assert getter('StubHub Center, Carson, CA') == ('StubHub Center', 'Carson, CA')


def test_case_does_not_decide_whether_a_venue_exists(monkeypatch):
    """
    "Stubhub Center" runs through the whole 2015 MLS file. Matched exactly it
    is not a stadium, and the build quietly turns it into a city of that name.
    """
    getter = location_normalizer(monkeypatch, STUBHUB)

    assert getter('Stubhub Center') == ('StubHub Center', 'Carson, CA')
    assert getter('STUBHUB CENTER') == ('StubHub Center', 'Carson, CA')


def test_a_place_that_is_not_a_stadium_stays_a_place(monkeypatch):
    getter = location_normalizer(monkeypatch, STUBHUB)

    assert getter('Richardson, Texas')[0] is None

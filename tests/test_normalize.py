import importlib.util
from pathlib import Path

import pytest

from fakedb import FakeDB
from normalize import (
    calculate_game_results,
    calculate_lineup_result,
    normalize_game,
    normalize_goal,
    normalize_salary,
    normalize_sponsorship,
    normalize_rules,
    normalize_transfer,
    normalize_valuation,
    normalize_ownership,
    salary_position,
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


# normalize_salary

def salary(**kw):
    e = {'name': 'Damarcus Beasley', 'team': 'Kansas City Wizards',
         'competition': 'Major League Soccer', 'season': '2004', 'base': '100000',
         'position': ''}
    e.update(kw)
    return e


def test_normalize_salary_normalizes_name_and_team():
    e = normalize_salary(salary())
    assert e['name'] == 'DaMarcus Beasley'
    assert e['team'] == 'Sporting Kansas City'


def test_normalize_salary_leaves_a_missing_team_missing():
    assert normalize_salary(salary(team=None))['team'] is None


def test_normalize_salary_groups_the_position():
    e = normalize_salary(salary(position='M-D'))
    assert e['position'] == 'Defender-Midfielder'
    assert e['position_group'] == 'Defender'


@pytest.mark.parametrize('printed, expected', [
    ('GK', ('Goalkeeper', 'Goalkeeper')),
    ('M', ('Midfielder', 'Midfielder')),
    ('M-F', ('Midfielder-Forward', 'Midfielder')),
    ('F-M', ('Midfielder-Forward', 'Midfielder')),
    ('F/M', ('Midfielder-Forward', 'Midfielder')),
    ('MF', ('Midfielder-Forward', 'Midfielder')),
    ('D/M', ('Defender-Midfielder', 'Defender')),
    ('F-D', ('Defender-Forward', 'Defender')),
    ('Center Forward/Attacking Midfielder', ('Center Forward/Attacking Midfielder', 'Midfielder')),
    ('Center-back', ('Center-back', 'Defender')),
    ('Left Wing', ('Left Wing', 'Forward')),
    ('Defensive Midfield', ('Defensive Midfield', 'Midfielder')),
    ('Substitute', ('Substitute', '')),
    ('', ('', '')),
])
def test_salary_position(printed, expected):
    assert salary_position(printed) == expected


def test_normalize_sponsorship_normalizes_the_club():
    e = normalize_sponsorship({'club': 'Kansas City Wizards', 'competition': 'Major League Soccer'})
    assert e['club'] == 'Sporting Kansas City'


def test_normalize_sponsorship_leaves_a_league_deal_without_a_club():
    assert normalize_sponsorship({'club': None, 'competition': 'Major League Soccer'})['club'] is None


def test_normalize_valuation_normalizes_the_team():
    e = normalize_valuation({'team': 'Montreal Impact', 'competition': 'Major League Soccer'})
    assert e['team'] == 'CF Montréal'


def test_normalize_ownership_normalizes_the_club():
    e = normalize_ownership({'club': 'Kansas City Wizards', 'competition': 'Major League Soccer'})
    assert e['club'] == 'Sporting Kansas City'


def test_an_unknown_salary_position_is_kept_ungrouped(capsys):
    assert salary_position('Libero') == ('Libero', '')
    assert 'unknown salary position' in capsys.readouterr().out


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


def test_normalization_uses_current_normalized_stadiums_each_run(monkeypatch):
    import normalize

    db = FakeDB()
    monkeypatch.setattr(normalize, 'soccer_db', db)
    monkeypatch.setattr(normalize, 'SOURCES', ['test'])
    monkeypatch.setattr(normalize, 'get_stadium',
                        lambda name: 'Build Stadium' if name == 'Raw Stadium' else name)

    for city in ('Carson, CA', 'Dallas, TX'):
        db.stadiums.drop()
        db.stadiums.insert_one({
            'name': 'Raw Stadium', 'location': city, 'opened': None, 'closed': None,
        })
        db.test_games.drop()
        db.test_games.insert_one({
            'team1': 'FC Dallas', 'team2': 'LA Galaxy',
            'team1_score': 1, 'team2_score': 0,
            'competition': 'Major League Soccer', 'season': '2010',
            'location': 'Build Stadium',
        })

        normalize.normalize()

        game = db.test_games.rows[0]
        assert game['stadium'] == 'Build Stadium'
        assert game['location'] == city


def test_importing_normalize_does_not_read_stadiums(monkeypatch):
    import normalize
    from build import mongo

    class UnavailableDatabase:
        def __getattr__(self, name):
            raise AssertionError(f'Import read the {name} collection')

    monkeypatch.setattr(mongo, 'soccer_db', UnavailableDatabase())
    spec = importlib.util.spec_from_file_location('normalize_import_test', Path(normalize.__file__))
    spec.loader.exec_module(importlib.util.module_from_spec(spec))


# normalize_game

def test_normalize_game_separates_shootout_winner():
    e = normalize_game({
        'competition': 'CONCACAF Champions League',
        'season': '2020',
        'date': None,
        'team1': 'Seattle Sounders',
        'team2': 'Olimpia',
        'team1_score': 2,
        'team2_score': 2,
        'shootout_winner': 'Olimpia',
    }, lambda location: (None, location))
    assert e['team1'] == 'CD Olimpia'
    assert e['shootout_winner'] == 'CD Olimpia'


def test_normalize_transfer_normalizes_clubs_and_leaves_an_empty_one():
    e = normalize_transfer({'name': 'Cade Cowell', 'from': 'Montreal Impact', 'to': '',
                            'competition': 'Major League Soccer'})
    assert e['from'] == 'CF Montréal'
    assert e['to'] == ''


def test_normalize_rules_normalizes_the_competition():
    assert normalize_rules({'competition': 'MLS'})['competition'] == 'Major League Soccer'

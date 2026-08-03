import pytest

import transform
from fakedb import FakeDB

U17 = 'FIFA U-17 World Cup'
MLS = 'Major League Soccer'


@pytest.fixture
def db(monkeypatch):
    """transform reads a module-global soccer_db; swap in an in-memory one."""
    fake = FakeDB(
        fifa_games=[
            {'competition': U17, 'team1': 'United States', 'team2': 'Brazil'},
            {'competition': MLS, 'team1': 'United States', 'team2': 'Brazil'},
        ],
        fifa_goals=[
            {'competition': U17, 'team': 'United States', 'goal': 'A Player'},
            {'competition': MLS, 'team': 'United States', 'goal': 'A Player'},
        ],
        fifa_lineups=[
            {'competition': U17, 'team': 'United States', 'name': 'A Player'},
            {'competition': MLS, 'team': 'United States', 'name': 'A Player'},
        ],
        fifa_stats=[
            {'competition': U17, 'team': 'United States', 'goals': 1},
            {'competition': MLS, 'team': 'United States', 'goals': 1},
        ],
    )
    monkeypatch.setattr(transform, 'soccer_db', fake)
    return fake


def rows(db, name):
    return list(db[name].find())


def test_youth_competition_gets_suffixed_team_names(db):
    transform.transform_team_names_for_competition('fifa', U17, '%s U-17')

    games = {g['competition']: g for g in rows(db, 'fifa_games')}
    assert games[U17]['team1'] == 'United States U-17'
    assert games[U17]['team2'] == 'Brazil U-17'


def test_other_competitions_are_untouched(db):
    transform.transform_team_names_for_competition('fifa', U17, '%s U-17')

    games = {g['competition']: g for g in rows(db, 'fifa_games')}
    assert games[MLS]['team1'] == 'United States'
    assert games[MLS]['team2'] == 'Brazil'


def test_goals_lineups_and_stats_are_transformed_too(db):
    transform.transform_team_names_for_competition('fifa', U17, '%s U-17')

    for coll in ('fifa_goals', 'fifa_lineups', 'fifa_stats'):
        by_comp = {e['competition']: e for e in rows(db, coll)}
        assert by_comp[U17]['team'] == 'United States U-17', coll
        assert by_comp[MLS]['team'] == 'United States', coll


def test_no_rows_are_lost(db):
    before = {c: len(rows(db, c)) for c in
              ('fifa_games', 'fifa_goals', 'fifa_lineups', 'fifa_stats')}

    transform.transform_team_names_for_competition('fifa', U17, '%s U-17')

    after = {c: len(rows(db, c)) for c in before}
    assert before == after


def test_transform_is_not_idempotent(db):
    # Running it twice suffixes twice. The build calls it once per competition;
    # this pins that re-running a partial build would corrupt team names.
    transform.transform_team_names_for_competition('fifa', U17, '%s U-17')
    transform.transform_team_names_for_competition('fifa', U17, '%s U-17')

    games = {g['competition']: g for g in rows(db, 'fifa_games')}
    assert games[U17]['team1'] == 'United States U-17 U-17'


def test_olympic_format_string(db):
    transform.transform_team_names_for_competition('fifa', U17, '%s Olympic')

    games = {g['competition']: g for g in rows(db, 'fifa_games')}
    assert games[U17]['team1'] == 'United States Olympic'

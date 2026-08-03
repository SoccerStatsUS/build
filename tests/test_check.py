import datetime

import pytest

import check
from fakedb import FakeDB

MLS = 'Major League Soccer'


def standing(**kw):
    e = {
        'name': 'FC Dallas', 'games': 3,
        'wins': 2, 'losses': 1, 'ties': 0,
        'shootout_wins': 0, 'shootout_losses': 0,
    }
    e.update(kw)
    return e


def full_game(**kw):
    e = {
        'team1': 'FC Dallas', 'team2': 'Colorado Rapids',
        'team1_score': 3, 'team2_score': 1,
        'date': datetime.datetime(2012, 1, 1),
        'season': '2012', 'competition': MLS,
    }
    e.update(kw)
    return e


@pytest.fixture
def db(monkeypatch):
    fake = FakeDB()
    monkeypatch.setattr(check.mongo, 'soccer_db', fake)
    return fake


@pytest.fixture
def pdb_hits(monkeypatch):
    """Stub pdb.set_trace the way make/__main__.py does for a batch run.

    Without this the checks below would open a real debugger under pytest.
    Returns a list that records each site that tripped.
    """
    import pdb as pdb_module
    import traceback

    hits = []

    def record(*args, **kwargs):
        caller = traceback.extract_stack()[-2]
        hits.append((caller.filename, caller.lineno, caller.name))

    monkeypatch.setattr(pdb_module, 'set_trace', record)
    return hits


# check_standings

def test_consistent_standing_is_silent(db, capsys):
    db.standings.rows = [standing()]
    check.check_standings()
    assert capsys.readouterr().out == ''


def test_shootout_results_count_towards_games(db, capsys):
    db.standings.rows = [standing(games=4, wins=2, losses=1, ties=0,
                                  shootout_wins=1, shootout_losses=0)]
    check.check_standings()
    assert capsys.readouterr().out == ''


def test_null_ties_are_treated_as_zero(db, capsys):
    # Sources that do not record ties leave the field null rather than 0.
    db.standings.rows = [standing(ties=None, shootout_wins=None, shootout_losses=None)]
    check.check_standings()
    assert capsys.readouterr().out == ''


def test_game_total_mismatch_is_reported(db, capsys):
    db.standings.rows = [standing(games=5)]
    check.check_standings()
    assert 'Games do not match' in capsys.readouterr().out


def test_every_bad_standing_is_reported(db, capsys):
    db.standings.rows = [standing(games=5), standing(name='Chicago Fire', games=9)]
    check.check_standings()
    assert capsys.readouterr().out.count('Games do not match') == 2


# check_games

def test_complete_game_is_silent(db, capsys):
    db.games.rows = [full_game()]
    check.check_games()
    assert capsys.readouterr().out == ''


def test_zero_scores_are_not_treated_as_missing(db, capsys):
    # The check is `field in game`, so a 0-0 game must still pass.
    db.games.rows = [full_game(team1_score=0, team2_score=0)]
    check.check_games()
    assert capsys.readouterr().out == ''


GAME_FIELDS = [
    'team1', 'team2', 'team1_score', 'team2_score', 'date', 'season', 'competition',
]


@pytest.mark.parametrize('missing', GAME_FIELDS)
def test_missing_field_is_named_in_the_report(db, capsys, pdb_hits, missing):
    game = full_game()
    del game[missing]
    db.games.rows = [game]

    check.check_games()

    out = capsys.readouterr().out
    assert missing in out
    assert pdb_hits == []


def test_report_identifies_the_offending_row(db, capsys, pdb_hits):
    # Naming the field is only half of it; the row has to be identifiable too.
    game = full_game()
    del game['date']
    db.games.rows = [game]

    check.check_games()

    out = capsys.readouterr().out
    assert 'FC Dallas' in out
    assert 'Colorado Rapids' in out


def test_each_missing_field_is_reported_separately(db, capsys, pdb_hits):
    game = full_game()
    del game['date']
    del game['season']
    db.games.rows = [game]

    check.check_games()

    out = capsys.readouterr().out
    assert 'date missing' in out
    assert 'season missing' in out
    assert pdb_hits == []


def test_a_complete_game_never_reaches_pdb(db, capsys, pdb_hits):
    db.games.rows = [full_game()]
    check.check_games()
    assert pdb_hits == []
    assert capsys.readouterr().out == ''

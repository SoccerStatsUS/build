import datetime

import denormalize
from fakedb import FakeDB


def test_game_stats_receive_historical_names_without_changing_bios(monkeypatch):
    rows = [
        {'team': 'FC Dallas', 'date': datetime.datetime(2000, 5, 1), 'goals': 2},
        {'team': 'FC Dallas', 'date': None, 'goals': 0},
    ]
    db = FakeDB(gstats=rows, bios=[{'name': 'Unchanged'}])
    monkeypatch.setattr(denormalize, 'soccer_db', db)

    denormalize.denormalize_game_stats()

    assert db.gstats.rows == [
        {**rows[0], 'team_original_name': 'Dallas Burn'},
        {**rows[1], 'team_original_name': 'FC Dallas'},
    ]
    assert db.bios.rows == [{'name': 'Unchanged'}]


def test_bios_have_their_own_denormalization_step(monkeypatch):
    db = FakeDB(
        awards=[
            {'award': 'US Soccer Hall of Fame', 'recipient': 'Inductee'},
            {'award': 'Other award', 'recipient': 'Other Player'},
        ],
        bios=[{'name': 'Inductee'}, {'name': 'Other Player', 'hall_of_fame': True}],
        gstats=[{'team': 'Unchanged'}],
    )
    monkeypatch.setattr(denormalize, 'soccer_db', db)

    denormalize.denormalize_bios()

    assert db.bios.rows == [
        {'name': 'Inductee', 'hall_of_fame': True},
        {'name': 'Other Player', 'hall_of_fame': False},
    ]
    assert db.gstats.rows == [{'team': 'Unchanged'}]


def test_full_denormalization_updates_game_stats_and_bios(monkeypatch):
    db = FakeDB(
        gstats=[{'team': 'FC Dallas', 'date': datetime.datetime(2000, 5, 1)}],
        bios=[{'name': 'Inductee'}],
        awards=[{'award': 'US Soccer Hall of Fame', 'recipient': 'Inductee'}],
    )
    monkeypatch.setattr(denormalize, 'soccer_db', db)

    denormalize.denormalize()

    assert db.gstats.rows[0]['team_original_name'] == 'Dallas Burn'
    assert db.bios.rows[0]['hall_of_fame'] is True

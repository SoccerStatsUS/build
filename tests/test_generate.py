from fakedb import FakeDB

import generate


def test_generated_stats_skip_seasons_with_loaded_stats(monkeypatch):
    """A season with stats from a source keeps them; only the rest are summed from games."""
    fake = FakeDB(
        stats=[{'name': 'Lionel Messi', 'team': 'Inter Miami', 'competition': 'MLS Cup Playoffs',
                'season': '2024', 'games_played': 3, 'goals': 1}],
        gstats=[
            {'player': 'Lionel Messi', 'team': 'Inter Miami', 'competition': 'MLS Cup Playoffs',
             'season': '2024', 'goals': 1, 'games_played': 1, 'games_started': 1, 'minutes': 90,
             'assists': 0, 'own_goals': 0},
            {'player': 'Landon Donovan', 'team': 'LA Galaxy', 'competition': 'MLS Cup Playoffs',
             'season': '2012', 'goals': 2, 'games_played': 1, 'games_started': 1, 'minutes': 90,
             'assists': 0, 'own_goals': 0},
            {'player': 'Landon Donovan', 'team': 'LA Galaxy', 'competition': 'MLS Cup Playoffs',
             'season': '2012', 'goals': 0, 'games_played': 1, 'games_started': 0, 'minutes': 30,
             'assists': 1, 'own_goals': 0},
        ],
    )
    monkeypatch.setattr(generate, 'soccer_db', fake)
    monkeypatch.setattr(generate, 'generic_load', lambda coll, fn: [coll.insert_one(r) for r in fn()])

    generate.generate_missing_stats('MLS Cup Playoffs')

    rows = {(r['name'], r['season']): r for r in fake.stats.find()}
    assert set(rows) == {('Lionel Messi', '2024'), ('Landon Donovan', '2012')}
    assert rows[('Lionel Messi', '2024')]['games_played'] == 3  # the loaded row, untouched
    assert (rows[('Landon Donovan', '2012')]['games_played'], rows[('Landon Donovan', '2012')]['goals'],
            rows[('Landon Donovan', '2012')]['assists']) == (2, 2, 1)

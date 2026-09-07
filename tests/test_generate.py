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


def test_home_team_inferred_only_from_a_stadium_with_one_tenant(monkeypatch):
    """A stated home side is kept; a stadium settles it only when exactly one club plays there."""
    def game(team1, team2, **extra):
        return {'team1': team1, 'team2': team2, 'date': None, 'home_team': None, **extra}
    fake = FakeDB(
        teams=[],
        games=[
            game('LA Galaxy', 'Real Salt Lake', home_team='Real Salt Lake', stadium='Rio Tinto Stadium'),
            game('New York City FC', 'Toronto FC', stadium='Yankees Stadium'),
            game('Toronto FC', 'New York City FC', stadium='Yankees Stadium'),
            game('Chivas USA', 'LA Galaxy', stadium='StubHub Center'),
            game('FC Dallas', 'Houston Dynamo', stadium='Stanford Stadium'),
            game('FC Dallas', 'Houston Dynamo'),
        ],
    )
    monkeypatch.setattr(generate, 'soccer_db', fake)
    monkeypatch.setattr(generate, 'insert_rows', lambda coll, rows: [coll.insert_one(r) for r in rows])
    monkeypatch.setattr(generate, 'make_stadium_getter', lambda: (lambda team, date: None))
    monkeypatch.setattr(generate, 'stadiums_to_teams', lambda: {
        'Rio Tinto Stadium': {'Real Salt Lake'},
        'Yankees Stadium': {'New York City FC', 'New York Cosmos'},
        'StubHub Center': {'LA Galaxy', 'Chivas USA'},
    })

    generate.generate_game_data()

    rows = list(fake.games.find())
    assert [(r['home_team'], r.get('home_team_inferred')) for r in rows] == [
        ('Real Salt Lake', None),
        ('New York City FC', True),
        ('New York City FC', True),
        (None, None),
        (None, None),
        (None, None),
    ]

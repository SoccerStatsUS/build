import datetime

import pytest

import openfootball_data


def parse(text, competition='Premier League'):
    return openfootball_data.process_lines(
        text.splitlines(), competition, 'https://example.test/source.txt',
        today=datetime.date.max,
    )


def test_parses_home_away_scores_and_infers_the_end_year():
    games = parse("""= English Premier League 2024/25
# Matches 2
▪ Matchday 1
Sat Aug 17 2024
  15:00  Arsenal FC  2-0 (1-0)  Wolves
Sun Jan 5
  Liverpool FC  v Manchester United  2-2 (0-0)
""")

    assert [(game['date'], game['team1'], game['team2']) for game in games] == [
        (datetime.datetime(2024, 8, 17), 'Arsenal FC', 'Wolves'),
        (datetime.datetime(2025, 1, 5), 'Liverpool FC', 'Manchester United'),
    ]
    assert games[0]['team1_score'] == 2
    assert games[0]['team2_score'] == 0
    assert games[0]['home_team'] == 'Arsenal FC'
    assert games[0]['sources'] == ['https://example.test/source.txt#L5']


def test_expands_a_season_across_a_century_boundary():
    game = parse("""= English Premier League 1999/00
# Matches 1
▪ Matchday 20
Sun Jan 2
  Sheffield Wednesday  v Arsenal  0-1
""")[0]

    assert game['season'] == '1999-2000'
    assert game['date'] == datetime.datetime(2000, 1, 2)


def test_parses_fixture_without_a_score_as_scheduled():
    game = parse("""= France | Ligue 1 2026/27
# Matches 1
▪ Matchday 1
Sun Aug 16 2026
  Lille OSC  v Paris FC
""", 'Ligue 1')[0]

    assert game['team1_score'] is None
    assert game['team2_score'] is None
    assert game['not_played'] is False


def test_discards_scores_from_future_fixtures():
    games = openfootball_data.process_lines(
        """= English Premier League 2026/27
# Matches 1
▪ Matchday 38
Sun May 30 2027
  Arsenal FC  v Liverpool FC  4-2 (2-1)
""".splitlines(),
        'Premier League',
        'https://example.test/source.txt',
        today=datetime.date(2026, 9, 12),
    )

    assert games[0]['team1_score'] is None
    assert games[0]['team2_score'] is None
    assert games[0]['not_played'] is False


def test_marks_an_awarded_result_as_a_forfeit():
    game = parse("""= Italian Serie A 2020/21
# Matches 1
▪ Matchday 1
Sat Sep 19 2020
  Hellas Verona FC  3-0  AS Roma  [awarded]
""", 'Serie A')[0]

    assert game['team1'] == 'Hellas Verona FC'
    assert game['team2'] == 'AS Roma'
    assert game['forfeit'] is True


def test_parses_shootout_and_neutral_champions_league_final():
    game = parse("""= UEFA Champions League 2025/26
# Matches 1
▪ Finals, Final
Sat May 30 2026
  Paris Saint-Germain FC (FRA) v Arsenal FC (ENG)  4-3 pen. 1-1 a.e.t. (1-1, 0-1)
""", 'UEFA Champions League')[0]

    assert game['team1'] == 'Paris Saint-Germain FC'
    assert game['team2'] == 'Arsenal FC'
    assert game['team1_score'] == game['team2_score'] == 1
    assert game['shootout_winner'] == 'Paris Saint-Germain FC'
    assert game['minutes'] == 120
    assert game['neutral'] is True
    assert game['home_team'] is None


@pytest.mark.parametrize('heading,competition,season,round_', [
    ('Playoffs, Conference Finals', 'MLS Cup Playoffs', '2024', 'Conference Finals'),
    ('Apertura, Matchday 1', 'Liga MX', '2024-2025 Apertura', 'Matchday 1'),
    ('Clausura Playoffs, Final', 'Liga MX Liguilla', '2024-2025 Clausura', 'Final'),
])
def test_splits_playoff_competitions(heading, competition, season, round_):
    original = 'Major League Soccer' if heading.startswith('Playoffs') else 'Liga MX'
    source_season = '2024' if original == 'Major League Soccer' else '2024/25'
    game = parse("""= League %s
# Matches 1
▪ %s
Sat Aug 17 2024
  Team One  v Team Two  1-0
""" % (source_season, heading), original)[0]

    assert game['competition'] == competition
    assert game['season'] == season
    assert game['round'] == round_


def test_fails_when_the_source_shape_drops_a_match():
    with pytest.raises(ValueError, match='expected 2 matches, parsed 1'):
        parse("""= English Premier League 2024/25
# Matches 2
▪ Matchday 1
Sat Aug 17 2024
  Arsenal FC  v Wolves  2-0
""")


def test_discovers_only_the_requested_datasets(tmp_path):
    for repo, _, pattern in openfootball_data.DATASETS:
        path = tmp_path / repo / pattern.replace('**/', '2024-25/').replace('*', '2024')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    found = openfootball_data.files(tmp_path)

    assert len(found) == len(openfootball_data.DATASETS)
    assert {competition for _, competition, _, _ in found} == {
        'Major League Soccer', 'Liga MX', 'CONCACAF Champions League',
        'UEFA Champions League', 'Premier League', 'La Liga',
        '1. Bundesliga', 'Serie A', 'Ligue 1',
    }

import datetime

from merge import merge_games, merge_rosters, merge_stats

JAN1 = datetime.datetime(2012, 1, 1)
JAN2 = datetime.datetime(2012, 1, 2)


def game(**kw):
    """merge_games needs the full key set; sources vary in what they supply."""
    e = {
        'date': JAN1,
        'season': '2012',
        'competition': 'Major League Soccer',
        'round': None,
        'team1': 'FC Dallas',
        'team2': 'Colorado Rapids',
        'team1_score': 2,
        'team2_score': 1,
        'team1_result': 'w',
        'team2_result': 'l',
    }
    e.update(kw)
    return e


def test_identical_games_merge():
    merged = merge_games([[game(), game()]])
    assert len(merged) == 1


def test_reversed_teams_merge():
    # Keys sort the team pair, so team order in the source does not matter.
    flipped = game(team1='Colorado Rapids', team2='FC Dallas',
                   team1_score=1, team2_score=2,
                   team1_result='l', team2_result='w')
    merged = merge_games([[game(), flipped]])
    assert len(merged) == 1
    assert merged[0]['team1'] == 'FC Dallas'
    assert merged[0]['team1_score'] == 2


def test_merge_fills_in_missing_location():
    merged = merge_games([[game(), game(location='Dallas, TX')]])
    assert len(merged) == 1
    assert merged[0]['location'] == 'Dallas, TX'


def test_merge_does_not_overwrite_a_known_value():
    merged = merge_games([[game(location='Dallas, TX'), game(location='Frisco, TX')]])
    assert len(merged) == 1
    assert merged[0]['location'] == 'Dallas, TX'


def test_merge_across_source_lists():
    merged = merge_games([[game()], [game(location='Dallas, TX')]])
    assert len(merged) == 1
    assert merged[0]['location'] == 'Dallas, TX'


def test_different_dates_do_not_merge():
    merged = merge_games([[game(), game(date=JAN2)]])
    assert len(merged) == 2


def test_different_teams_do_not_merge():
    merged = merge_games([[game(), game(team2='Chicago Fire')]])
    assert len(merged) == 2


def test_undated_games_merge_on_round():
    # No date, but a round: keyed on (teams, date, season, round).
    merged = merge_games([[game(date=None, round='Final'),
                           game(date=None, round='Final')]])
    assert len(merged) == 1


def test_game_without_date_or_round_is_discarded():
    # Neither key can be built, so the row cannot be merged safely.
    assert merge_games([[game(date=None, round=None)]]) == []


def test_merges_counter_and_sources_accumulate():
    merged = merge_games([[game(sources=['Imagination']),
                           game(sources=['Hearsay'])]])
    assert len(merged) == 1
    assert merged[0]['merges'] == 1
    assert sorted(merged[0]['sources']) == ['Hearsay', 'Imagination']


def test_unmerged_game_reports_zero_merges():
    merged = merge_games([[game()]])
    assert merged[0]['merges'] == 0
    assert merged[0]['sources'] == []


# merge_stats

def stat(**kw):
    e = {
        'name': 'Jason Kreis',
        'team': 'FC Dallas',
        'competition': 'Major League Soccer',
        'season': '2001',
        'goals': 0,
        'assists': 0,
    }
    e.update(kw)
    return e


def test_stats_merge_on_name_team_competition_season():
    merged = list(merge_stats([[stat(goals=3, assists=5), stat(goals=13, assists=0)]]))
    assert len(merged) == 1


def test_stats_merge_keeps_first_nonzero_value():
    # Falsy values lose to later truthy ones; established values are kept.
    merged = list(merge_stats([[stat(goals=3, assists=0), stat(goals=13, assists=5)]]))
    assert merged[0]['goals'] == 3
    assert merged[0]['assists'] == 5


def test_stats_for_different_seasons_stay_separate():
    merged = list(merge_stats([[stat(season='2001'), stat(season='2002')]]))
    assert len(merged) == 2


def test_stats_for_different_teams_stay_separate():
    merged = list(merge_stats([[stat(), stat(team='Real Salt Lake')]]))
    assert len(merged) == 2


# merge_rosters

def roster(**kw):
    e = {'team': 'FC Dallas', 'season': '2001', 'name': 'Jason Kreis'}
    e.update(kw)
    return e


def test_rosters_merge_on_team_season_name():
    merged = list(merge_rosters([[roster(), roster()]]))
    assert len(merged) == 1


def test_rosters_keep_the_first_record_seen():
    merged = list(merge_rosters([[roster(number=9), roster(number=99)]]))
    assert merged[0]['number'] == 9


def test_rosters_for_different_seasons_stay_separate():
    merged = list(merge_rosters([[roster(season='2001'), roster(season='2002')]]))
    assert len(merged) == 2

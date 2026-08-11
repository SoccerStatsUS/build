import datetime

import pytest

import reconcile


def game(**kw):
    e = {
        'season': 2024,
        'date': datetime.datetime(2024, 5, 4, 23, 0),
        'home': 'FC Dallas', 'away': 'Colorado Rapids',
        'home_score': 3, 'away_score': 1,
        'venue': 'Toyota Stadium', 'attendance': 15000,
        'goals': [], 'cards': [],
    }
    e.update(kw)
    return e


# normalize_team

@pytest.mark.parametrize('a,b', [
    ('Portland Thorns FC', 'Portland Thorns'),
    ('New York City Football Club', 'New York City FC'),
    ('Bay FC', 'Bay'),
    ('CF Montréal', 'CF Montreal'),
    ('Racing Louisville FC', 'Racing Louisville'),
])
def test_suffix_and_accent_differences_collapse(a, b):
    assert reconcile.normalize_team(a) == reconcile.normalize_team(b)


@pytest.mark.parametrize('a,b', [
    ('LAFC', 'Los Angeles Football Club'),
    ('Red Bull New York', 'New York Red Bulls'),
])
def test_aliased_names_collapse(a, b):
    assert reconcile.normalize_team(a) == reconcile.normalize_team(b)


def test_western_new_york_flash_folds_into_north_carolina_courage():
    # espn backdates the franchise's current name onto its Flash-era seasons.
    assert (reconcile.normalize_team('Western New York Flash') ==
            reconcile.normalize_team('North Carolina Courage'))


def test_distinct_clubs_stay_distinct():
    # FC Kansas City folded; the Current are a different franchise entirely.
    assert (reconcile.normalize_team('FC Kansas City') !=
            reconcile.normalize_team('Kansas City Current'))


# parse_date

def test_parses_the_espn_spelling_without_seconds():
    assert reconcile.parse_date('2020-02-29T18:00Z') == datetime.datetime(2020, 2, 29, 18, 0)


def test_parses_the_league_spelling_with_seconds():
    assert reconcile.parse_date('2017-03-04T02:30:00Z') == datetime.datetime(2017, 3, 4, 2, 30)


# match

def test_identical_games_pair_up():
    pairs, a_only, b_only, ambiguous = reconcile.match([game()], [game()])
    assert len(pairs) == 1
    assert (a_only, b_only, ambiguous) == ([], [], [])


def test_a_day_apart_still_pairs_up():
    # A 03:30Z kickoff is the previous evening locally, so the sources disagree
    # on the calendar date for a large share of games.
    a = game(date=datetime.datetime(2024, 5, 5, 3, 30))
    b = game(date=datetime.datetime(2024, 5, 4, 23, 0))
    pairs, _, _, _ = reconcile.match([a], [b])
    assert len(pairs) == 1


def test_two_days_apart_does_not_pair_up():
    a = game(date=datetime.datetime(2024, 5, 7, 23, 0))
    pairs, a_only, b_only, _ = reconcile.match([a], [game()])
    assert pairs == []
    assert len(a_only) == 1
    assert len(b_only) == 1


def test_home_and_away_are_not_interchangeable():
    reversed_game = game(home='Colorado Rapids', away='FC Dallas')
    pairs, a_only, b_only, _ = reconcile.match([game()], [reversed_game])
    assert pairs == []
    assert len(a_only) == 1 and len(b_only) == 1


def test_two_candidates_are_reported_not_guessed():
    # A doubleheader or a rescheduled fixture must never be paired off silently.
    b_games = [game(), game(date=datetime.datetime(2024, 5, 5, 3, 30))]
    pairs, a_only, _, ambiguous = reconcile.match([game()], b_games)
    assert pairs == []
    assert a_only == []
    assert len(ambiguous) == 1
    assert len(ambiguous[0][1]) == 2


def test_an_unmatched_b_game_is_not_lost():
    extra = game(home='Chicago Fire', away='LA Galaxy')
    _, _, b_only, _ = reconcile.match([game()], [game(), extra])
    assert len(b_only) == 1
    assert b_only[0]['home'] == 'Chicago Fire'


def test_a_matched_b_game_is_not_also_reported_as_unmatched():
    _, _, b_only, _ = reconcile.match([game()], [game()])
    assert b_only == []


# compare

def test_agreeing_games_have_nothing_to_report():
    assert reconcile.compare(game(), game()) == []


def test_score_disagreement_is_caught():
    assert 'score' in reconcile.compare(game(), game(away_score=2))


def test_date_disagreement_is_caught_within_the_match_tolerance():
    # The pair still matches; the day's difference is the finding.
    b = game(date=datetime.datetime(2024, 5, 5, 3, 30))
    assert 'date' in reconcile.compare(game(), b)


def test_a_missing_attendance_is_not_a_disagreement():
    # espn and mlssoccer write 0 for an unrecorded gate, nwslsoccer writes null.
    assert reconcile.compare(game(attendance=None), game()) == []
    assert reconcile.compare(game(attendance=0), game()) == []


def test_differing_attendance_is_caught():
    assert 'attendance' in reconcile.compare(game(), game(attendance=15001))


def test_goal_counts_are_only_compared_when_both_sides_have_events():
    # Whole seasons carry no event data in one archive or the other.
    scored = game(goals=[{'minute': '5'}, {'minute': '9'}])
    assert reconcile.compare(scored, game(goals=[])) == []
    assert 'goal_count' in reconcile.compare(scored, game(goals=[{'minute': '5'}]))


def test_card_counts_are_only_compared_when_both_sides_have_events():
    booked = game(cards=[{'minute': '30'}])
    assert reconcile.compare(booked, game(cards=[])) == []
    assert 'card_count' in reconcile.compare(
        booked, game(cards=[{'minute': '30'}, {'minute': '70'}]))


def test_every_disagreement_is_reported_not_just_the_first():
    bad = reconcile.compare(game(), game(away_score=2, attendance=99))
    assert 'score' in bad
    assert 'attendance' in bad


# attendance

@pytest.mark.parametrize('raw', [0, None])
def test_unrecorded_gate_normalizes_to_none(raw):
    assert reconcile.attendance(raw) is None


def test_a_real_gate_survives():
    assert reconcile.attendance(15000) == 15000


# short_goals

def test_a_goal_list_matching_the_score_is_fine():
    g = game(home_score=2, away_score=1, goals=[{}, {}, {}])
    assert reconcile.short_goals([g]) == 0


def test_a_goal_list_short_of_the_score_is_caught():
    # nwslsoccer's 2022 games carry the right score and almost no goals.
    g = game(home_score=6, away_score=0, goals=[{}])
    assert reconcile.short_goals([g]) == 1


def test_a_source_with_no_events_at_all_is_not_blamed():
    # espn records no NWSL events for whole seasons; that is absence, not error.
    assert reconcile.short_goals([game(goals=[])]) == 0


def test_a_goalless_draw_needs_no_goals():
    assert reconcile.short_goals([game(home_score=0, away_score=0, goals=[])]) == 0


# reporting

def test_hard_fields_all_know_how_to_print_themselves():
    for field in reconcile.HARD_FIELDS:
        assert field in reconcile.VALUES
        assert reconcile.VALUES[field](game())

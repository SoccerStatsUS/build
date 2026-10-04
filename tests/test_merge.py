import datetime

from merge import fill_bio_birthdates, merge_bio_rows, merge_games, merge_rosters, merge_stats
from metadata.utils import person_identity_key

JAN1 = datetime.datetime(2012, 1, 1)
JAN2 = datetime.datetime(2012, 1, 2)


def test_bios_merge_across_diacritics_and_keep_the_accented_name():
    rows = merge_bio_rows([[
        {'name': 'Josef Martinez', 'birthdate': JAN1},
        {'name': 'Josef Martínez', 'birthplace': 'Valencia, Venezuela'},
    ]])

    assert list(rows) == [{
        'name': 'Josef Martínez',
        'birthdate': JAN1,
        'birthplace': 'Valencia, Venezuela',
    }]


def test_bios_merge_across_case_and_nonbreaking_spaces():
    rows = merge_bio_rows([[
        {'name': 'John\N{NO-BREAK SPACE}McGuire'},
        {'name': 'john mcguire', 'birthplace': 'Scotland'},
    ]])

    assert list(rows) == [{'name': 'John McGuire', 'birthplace': 'Scotland'}]


def test_bios_with_different_normalized_names_stay_separate():
    rows = merge_bio_rows([[
        {'name': 'Willie Reid'},
        {'name': 'Mike Reid'},
    ]])

    assert len(list(rows)) == 2


TODAY = datetime.date(2026, 10, 4)
SULLIVAN = {'name': 'Cavan Sullivan', 'dob': '2009-09-28', 'seasons': [2024, 2025, 2026]}
BORN = datetime.datetime(2009, 9, 28)


def fill(bios, scraped, years):
    """Appearances are keyed the way merge keys a name, spelled as the site spells it."""
    keys = {person_identity_key(name): seasons for name, seasons in years.items()}
    names = {person_identity_key(name): name for name in years}
    bios, tally, conflicts = fill_bio_birthdates(bios, scraped, keys, names, TODAY)
    return bios, dict(tally), conflicts


def test_a_scraped_birth_date_fills_a_bio_that_has_none():
    bios, tally, _ = fill([{'name': 'Cavan Sullivan', 'birthplace': 'Philadelphia'}],
                          [SULLIVAN], {'Cavan Sullivan': {2024, 2025, 2026}})

    assert bios == [{'name': 'Cavan Sullivan', 'birthplace': 'Philadelphia', 'birthdate': BORN}]
    assert tally == {'filled': 1}


def test_a_player_on_record_through_appearances_alone_gets_a_bio_row():
    bios, tally, _ = fill([], [SULLIVAN], {'Cavan Sullivan': {2024, 2025}})

    assert bios == [{'name': 'Cavan Sullivan', 'source': 'MLSSoccer.com', 'birthdate': BORN}]


def test_a_scraped_player_who_appears_nowhere_is_not_added():
    bios, tally, _ = fill([], [SULLIVAN], {})

    assert bios == []
    assert tally == {'skipped, not on record': 1}


def test_a_birth_date_already_held_is_kept_and_the_disagreement_reported():
    held = datetime.datetime(1976, 4, 29)
    bios, tally, conflicts = fill(
        [{'name': 'Sean Nealis', 'birthdate': held}],
        [{'name': 'Sean Nealis', 'dob': '1997-01-13', 'seasons': [2019]}],
        {'Sean Nealis': {2019}})

    assert bios == [{'name': 'Sean Nealis', 'birthdate': held}]
    assert conflicts == [('Sean Nealis', '1976-04-29', '1997-01-13')]
    assert tally == {'conflicting': 1}


def test_a_namesake_with_no_season_in_common_is_left_alone():
    # The Benjamín Galindo on record played 1993-1998; the scraped one was born in 1999.
    bios, tally, _ = fill(
        [], [{'name': 'Benjamín Galindo', 'dob': '1999-03-10', 'seasons': [2025]}],
        {'Benjamín Galindo': {1993, 1998}})

    assert bios == []
    assert tally == {'skipped, no season in common': 1}


def test_an_age_no_player_could_be_in_a_season_on_record_is_left_alone():
    # Two people already merged under one name: a season in common, and one from 2009.
    bios, tally, _ = fill(
        [], [{'name': 'André Luiz', 'dob': '2002-02-23', 'seasons': [2026]}],
        {'André Luiz': {2009, 2026}})

    assert bios == []
    assert tally == {'skipped, implausible age': 1}


def test_a_name_two_scraped_players_share_is_left_alone():
    bios, tally, _ = fill(
        [],
        [{'name': 'Luis Suárez', 'dob': '1987-01-24', 'seasons': [2025], 'player_id': 'A'},
         {'name': 'Luis Suárez', 'dob': '2006-03-12', 'seasons': [2025], 'player_id': 'B'}],
        {'Luis Suárez': {2025}})

    assert bios == []
    assert tally == {'skipped, name shared by scraped players': 2}


def test_one_player_listed_under_two_spellings_is_not_a_shared_name():
    rows = [{'name': name, 'dob': '2000-05-02', 'seasons': [2025], 'player_id': 'A'}
            for name in ('Dagur Thorhallsson', 'Dagur Thórhallsson')]
    bios, tally, _ = fill([], rows, {'Dagur Thórhallsson': {2025}})

    assert [b['name'] for b in bios] == ['Dagur Thórhallsson']
    assert tally == {'filled': 1}


def test_a_player_is_found_under_whichever_of_his_names_the_site_uses():
    # The profile says Zakrzewski; the roster, the stats and the site say Hall.
    rows = [{'name': name, 'dob': '2008-03-24', 'seasons': [2023, 2026], 'player_id': 'A'}
            for name in ('Julian Hall', 'Julian Zakrzewski')]
    bios, tally, _ = fill([], rows, {'Julian Hall': {2023, 2026}})

    assert bios == [{'name': 'Julian Hall', 'source': 'MLSSoccer.com',
                     'birthdate': datetime.datetime(2008, 3, 24)}]
    assert tally == {'filled': 1, 'skipped, not on record': 1}


def test_a_date_that_is_missing_or_makes_the_player_a_child_today_is_dropped():
    bios, tally, _ = fill(
        [],
        [{'name': 'Taylor Booth', 'dob': '2026-05-31', 'seasons': [2026]},
         {'name': 'No Date', 'dob': None, 'seasons': [2026]}],
        {'Taylor Booth': {2026}, 'No Date': {2026}})

    assert bios == []
    assert tally == {'skipped, no usable date': 2}


def test_a_timestamped_scraped_date_is_read_as_its_day():
    bios, _, _ = fill([], [{'name': 'Alexander López', 'dob': '1992-06-05T00:00:00Z',
                            'seasons': [2025]}], {'Alexander López': {2025}})

    assert bios[0]['birthdate'] == datetime.datetime(1992, 6, 5)


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


def test_a_game_recorded_without_a_score_takes_one_from_a_later_source():
    # nwslsoccer carries whole NWSL seasons as fixtures with lineups and no
    # score; espn has the scores. Normalize runs first, so the scoreless record
    # arrives with empty results.
    fixture = game(team1_score=None, team2_score=None,
                   team1_result='', team2_result='')
    merged = merge_games([[fixture], [game()]])

    assert len(merged) == 1
    assert merged[0]['team1_score'] == 2
    assert merged[0]['team2_score'] == 1
    assert merged[0]['team1_result'] == 'w'
    assert merged[0]['team2_result'] == 'l'


def test_a_scoreless_record_takes_a_reversed_score_the_right_way_round():
    fixture = game(team1_score=None, team2_score=None,
                   team1_result='', team2_result='')
    flipped = game(team1='Colorado Rapids', team2='FC Dallas',
                   team1_score=1, team2_score=2,
                   team1_result='l', team2_result='w')
    merged = merge_games([[fixture], [flipped]])

    assert len(merged) == 1
    assert merged[0]['team1'] == 'FC Dallas'
    assert merged[0]['team1_score'] == 2
    assert merged[0]['team2_score'] == 1
    assert merged[0]['team1_result'] == 'w'


def test_a_recorded_score_is_never_replaced():
    merged = merge_games([[game()], [game(team1_score=5, team2_score=0,
                                          team1_result='w', team2_result='l')]])
    assert len(merged) == 1
    assert merged[0]['team1_score'] == 2
    assert merged[0]['team2_score'] == 1


def test_a_recorded_nil_is_a_score_not_a_blank():
    # The bug the score guard was written against: 0 read as an empty field and
    # overwritten with the other record's larger score.
    nil = game(team1_score=0, team2_score=0, team1_result='t', team2_result='t')
    merged = merge_games([[nil], [game()]])

    assert len(merged) == 1
    assert merged[0]['team1_score'] == 0
    assert merged[0]['team2_score'] == 0
    assert merged[0]['team1_result'] == 't'


def test_a_half_recorded_score_does_not_fill_a_blank():
    fixture = game(team1_score=None, team2_score=None,
                   team1_result='', team2_result='')
    half = game(team1_score=3, team2_score=None, team1_result='', team2_result='')
    merged = merge_games([[fixture], [half]])

    assert len(merged) == 1
    assert merged[0]['team1_score'] is None


def test_a_scoreless_game_stays_scoreless_when_no_source_has_one():
    fixture = game(team1_score=None, team2_score=None,
                   team1_result='', team2_result='')
    merged = merge_games([[fixture], [dict(fixture)]])

    assert len(merged) == 1
    assert merged[0]['team1_score'] is None
    assert merged[0]['team1_result'] == ''


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


def test_stats_merge_names_that_differ_only_by_diacritics():
    merged = list(merge_stats([[
        stat(name='Josef Martinez', goals=3),
        stat(name='Josef Martínez', assists=5),
    ]]))

    assert len(merged) == 1
    assert merged[0]['name'] == 'Josef Martínez'
    assert merged[0]['goals'] == 3
    assert merged[0]['assists'] == 5


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


def test_rosters_merge_names_that_differ_only_by_case_and_spacing():
    merged = list(merge_rosters([[
        roster(name='John\N{NO-BREAK SPACE}McGuire'),
        roster(name='john mcguire'),
    ]]))

    assert len(merged) == 1
    assert merged[0]['name'] == 'John McGuire'


def test_rosters_keep_the_first_record_seen():
    merged = list(merge_rosters([[roster(number=9), roster(number=99)]]))
    assert merged[0]['number'] == 9


def test_rosters_for_different_seasons_stay_separate():
    merged = list(merge_rosters([[roster(season='2001'), roster(season='2002')]]))
    assert len(merged) == 2

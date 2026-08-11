"""Compare two independent scrapes of the same competition against each other.

The build merges hand-coded sources, and merging is where errors show up. These
archives are the one place we have two machine-collected copies of the same
games, so a disagreement between them is unambiguously an error in one side.

Standalone: reads the jsonl archives directly, touches no database, and is not
called from build() or check(). `metadata.alias.get_team` is deliberately not
reused -- it imports build.mongo, which would pull a live database in behind a
tool that otherwise needs nothing.
"""

import collections
import datetime
import json
import os
import re
import unicodedata

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Names that survive normalization as genuinely different strings.
#
# The last entry is a franchise move, not an alias: Western New York Flash
# became the North Carolina Courage in 2017. espn applies the current name to
# the franchise's earlier seasons, the league site uses the name the club played
# under. Folding them together is right *for matching* -- the two names never
# denote two clubs in the same season -- but it is not a claim that the build
# should call the 2016 club by its 2017 name.
TEAM_ALIASES = {
    'lafc': 'losangeles',
    'redbullnewyork': 'newyorkredbulls',
    'westernnewyorkflash': 'northcarolinacourage',
}

# A game in one source is matched to a game in the other if the teams agree and
# the dates are within this many days. Kickoffs are stored in UTC and a 03:30Z
# MLS kickoff is the previous evening locally, so same-date is too strict.
DATE_TOLERANCE = datetime.timedelta(days=1)


def normalize_team(name):
    name = unicodedata.normalize('NFKD', name.lower())
    name = ''.join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r'\bfootball club\b', '', name)
    name = re.sub(r'\b(fc|sc|cf|afc|club)\b', '', name)
    name = re.sub(r'[^a-z]', '', name)
    return TEAM_ALIASES.get(name, name)


def parse_date(s):
    """Parse the two timestamp spellings in these archives.

    espn writes 2020-02-29T18:00Z, the league sites write 2017-03-04T02:30:00Z.
    """
    s = s.rstrip('Z')
    fmt = '%Y-%m-%dT%H:%M:%S' if s.count(':') == 2 else '%Y-%m-%dT%H:%M'
    return datetime.datetime.strptime(s, fmt)


def read(path):
    with open(os.path.join(ROOT_DIR, path)) as f:
        return [json.loads(line) for line in f]


def attendance(value):
    # espn and mlssoccer write 0 for an unrecorded gate; nwslsoccer writes null.
    return value or None


def game(row, goals, cards):
    return {
        'season': row['season'],
        'date': parse_date(row['date']),
        'home': row['home']['name'],
        'away': row['away']['name'],
        'home_score': row['home']['score'],
        'away_score': row['away']['score'],
        'venue': row.get('venue'),
        'attendance': attendance(row.get('attendance')),
        'goals': goals,
        'cards': cards,
    }


def read_espn(path, season_types):
    """espn keeps scores, cards and goals together in a flat `details` list.

    Unplayed rows have to go. espn carries ghost fixtures -- a 2015 NWSL game
    appears once as a real result under the franchise's *current* name and again
    as a STATUS_SCHEDULED 0-0 under the name it played under, on two different
    game ids. Comparing those against a source that lists each game once turns
    every one of them into a phantom score disagreement.
    """
    games, skipped = [], 0
    for row in read(path):
        if row['season_type'] not in season_types:
            continue
        if not row['completed']:
            skipped += 1
            continue
        details = row.get('details') or []
        games.append(game(
            row,
            [d for d in details if d['scoring_play']],
            [d for d in details if d['red_card'] or d['yellow_card']],
        ))
    return games, skipped


def read_league(path, competitions, played):
    """The league sites keep goals and cards in their own lists."""
    games, skipped = [], 0
    for row in read(path):
        if competitions is not None and row['competition'] not in competitions:
            continue
        if row['status'] not in played:
            skipped += 1
            continue
        games.append(game(row, row.get('goals') or [], row.get('cards') or []))
    return games, skipped


# espn spells the NWSL regular season two different ways depending on the
# season, which is itself worth knowing about.
#
# nwslsoccer gets no competition filter because it has nothing to filter on:
# every row is competition 'NWSL' and its `round` field is null on all 1450 of
# them, so the archive cannot tell a playoff game from a regular season one.
# The handful of "nwslsoccer only" games each season are that -- playoffs, which
# espn files under season types this excludes. They are listed, not silenced.
SOURCES = {
    'MLS': [
        ('espn', lambda: read_espn('espn_data/parsed/mls.jsonl', {'regular-season'})),
        ('mlssoccer', lambda: read_league('mlssoccer_data/parsed/mls.jsonl',
                                          {'Major League Soccer - Regular Season'},
                                          {'finalWhistle'})),
    ],
    'NWSL': [
        ('espn', lambda: read_espn('espn_data/parsed/nwsl.jsonl', {'regular-season', 'regular'})),
        ('nwslsoccer', lambda: read_league('nwslsoccer_data/parsed/nwsl.jsonl', None,
                                           {'FINISHED'})),
    ],
}


def match(a_games, b_games):
    """Pair games across two sources on teams plus an approximate date.

    Returns (pairs, a_only, b_only, ambiguous). A game with more than one
    candidate is never silently paired off -- doubleheaders and rescheduled
    fixtures land there and need to be looked at.
    """
    index = collections.defaultdict(list)
    for b in b_games:
        index[(normalize_team(b['home']), normalize_team(b['away']))].append(b)

    pairs, a_only, ambiguous = [], [], []
    taken = set()

    for a in a_games:
        key = (normalize_team(a['home']), normalize_team(a['away']))
        candidates = [b for b in index[key]
                      if abs(b['date'] - a['date']) <= DATE_TOLERANCE]
        if len(candidates) == 1:
            pairs.append((a, candidates[0]))
            taken.add(id(candidates[0]))
        elif not candidates:
            a_only.append(a)
        else:
            ambiguous.append((a, candidates))

    b_only = [b for b in b_games if id(b) not in taken]
    return pairs, a_only, b_only, ambiguous


# Fields where a disagreement is always an error in one source, and so gets
# listed row by row rather than just counted. Attendance and venue disagree
# constantly and would bury everything else.
HARD_FIELDS = ['score', 'date', 'goal_count']

VALUES = {
    'score': lambda g: '%d-%d' % (g['home_score'], g['away_score']),
    'date': lambda g: str(g['date'].date()),
    'goal_count': lambda g: '%d goals' % len(g['goals']),
}


def compare(a, b):
    """Return the names of the fields on which two matched games disagree."""
    bad = []

    if (a['home_score'], a['away_score']) != (b['home_score'], b['away_score']):
        bad.append('score')

    if a['date'].date() != b['date'].date():
        bad.append('date')

    if a['attendance'] and b['attendance'] and a['attendance'] != b['attendance']:
        bad.append('attendance')

    if a['venue'] and b['venue'] and normalize_team(a['venue']) != normalize_team(b['venue']):
        bad.append('venue')

    # Event lists are empty for whole seasons in both archives, so only compare
    # counts where both sides actually recorded events.
    if a['goals'] and b['goals'] and len(a['goals']) != len(b['goals']):
        bad.append('goal_count')

    if a['cards'] and b['cards'] and len(a['cards']) != len(b['cards']):
        bad.append('card_count')

    return bad


def short_goals(games):
    """Games whose goal list does not account for the game's own score.

    A cross-source goal-count difference says the two disagree but not which one
    is wrong. Both sides carry the score independently of the event list, so
    checking each source against itself settles it -- that is what separates
    nwslsoccer's broken 2022 goal lists (score right, events missing) from a
    genuine disagreement about what happened.
    """
    short = [g for g in games
             if g['goals'] and len(g['goals']) != g['home_score'] + g['away_score']]
    return len(short)


def describe(g):
    return '%s %s vs %s' % (g['date'].date(), g['home'], g['away'])


def report_season(competition, season, a_name, b_name, a_games, b_games):
    pairs, a_only, b_only, ambiguous = match(a_games, b_games)

    print('%s %s  %s=%d  %s=%d' % (
        competition, season, a_name, len(a_games), b_name, len(b_games)))
    print('  matched         %4d' % len(pairs))
    print('  %-14s %4d' % ('%s only' % a_name, len(a_only)))
    print('  %-14s %4d' % ('%s only' % b_name, len(b_only)))
    print('  ambiguous       %4d' % len(ambiguous))

    for g in a_only:
        print('    %s only: %s' % (a_name, describe(g)))
    for g in b_only:
        print('    %s only: %s' % (b_name, describe(g)))
    for g, candidates in ambiguous:
        print('    ambiguous: %s -> %d candidates' % (describe(g), len(candidates)))

    counts = collections.Counter()
    for a, b in pairs:
        bad = compare(a, b)
        counts.update(bad)
        for field in bad:
            if field in HARD_FIELDS:
                value = VALUES[field]
                print('    %s: %s | %s %s vs %s %s' % (
                    field, describe(a), a_name, value(a), b_name, value(b)))

    if counts:
        print('  disagreements:')
        for field, n in counts.most_common():
            print('    %-14s %4d' % (field, n))

    for name, games in ((a_name, a_games), (b_name, b_games)):
        n = short_goals(games)
        if n:
            print('  %s goal lists short of the score: %d' % (name, n))
    print()


def reconcile():
    for competition, sources in SOURCES.items():
        (a_name, a_load), (b_name, b_load) = sources
        (a_games, a_skipped), (b_games, b_skipped) = a_load(), b_load()

        print('%s: skipped unplayed rows -- %s %d, %s %d\n' % (
            competition, a_name, a_skipped, b_name, b_skipped))

        a_seasons = {g['season'] for g in a_games}
        b_seasons = {g['season'] for g in b_games}
        seasons = a_seasons & b_seasons

        # A season present in one source but not the other is a hole worth
        # naming. nwslsoccer's whole 2015 season is fixtures with no results,
        # so it drops out here rather than showing up as 93 disagreements.
        for name, missing in ((b_name, a_seasons - b_seasons),
                              (a_name, b_seasons - a_seasons)):
            for season in sorted(missing):
                print('%s %s: no played games from %s\n' % (competition, season, name))

        if not seasons:
            print('%s: no overlapping seasons\n' % competition)
            continue

        for season in sorted(seasons):
            report_season(
                competition, season, a_name, b_name,
                [g for g in a_games if g['season'] == season],
                [g for g in b_games if g['season'] == season],
            )


if __name__ == "__main__":
    reconcile()

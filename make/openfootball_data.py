import datetime
import hashlib
import re
from pathlib import Path


DATASETS = (
    ('world', 'Major League Soccer', 'north-america/major-league-soccer/*_mls.txt'),
    ('world', 'Liga MX', 'north-america/mexico/*_mx1.txt'),
    ('world', 'CONCACAF Champions League',
     'north-america/champions-league/*_concacafcl.txt'),
    ('champions-league', 'UEFA Champions League', '**/cl.txt'),
    ('champions-league', 'UEFA Champions League', '**/clq.txt'),
    ('england', 'Premier League', '**/1-premierleague.txt'),
    ('espana', 'La Liga', '**/1-liga.txt'),
    ('deutschland', '1. Bundesliga', '**/1-bundesliga.txt'),
    ('italy', 'Serie A', '**/1-seriea.txt'),
    ('europe', 'Ligue 1', 'france/*_fr1.txt'),
)

DATE_RE = re.compile(
    r'^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) '
    r'(?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) '
    r'(?P<day>\d{1,2})(?: (?P<year>\d{4}))?\b'
)
HEADER_RE = re.compile(r'^= .*? (?P<year>\d{4})(?:/(?P<end>\d{2}|\d{4}))?\s*$')
TIME_RE = re.compile(r'^\d{1,2}:\d{2}\s+')
SCORE_PATTERN = (
    r'(?:(?P<pen1>\d+)-(?P<pen2>\d+) pen\.\s+)?'
    r'(?P<score1>\d+)-(?P<score2>\d+)'
    r'(?P<aet> a\.e\.t\.)?'
    r'(?: \([^)]*\))?'
)
SCORE_RE = re.compile(SCORE_PATTERN + r'(?:\s+\[(?P<note>[^]]+)\])?$')
NO_V_RE = re.compile(
    r'^(?P<team1>.+?)\s{2,}' + SCORE_PATTERN
    + r'\s{2,}(?P<team2>.+?)(?:\s{2,}\[(?P<note>[^]]+)\])?$'
)
COUNTRY_SUFFIX_RE = re.compile(r'\s+\([A-Z]{3}\)$')


def files(root):
    root = Path(root)
    missing = []
    found = []

    for repo, competition, pattern in DATASETS:
        repo_root = root / repo
        if not repo_root.is_dir():
            missing.append(repo)
            continue
        paths = sorted(repo_root.glob(pattern))
        if not paths:
            raise FileNotFoundError('%s contains no files matching %s' % (repo_root, pattern))
        found.extend((repo, competition, repo_root, path) for path in paths)

    if missing:
        names = ', '.join(sorted(set(missing)))
        raise FileNotFoundError(
            'missing OpenFootball repositories in %s: %s; run build/install/of.sh'
            % (root, names)
        )

    return found


def load(root):
    games = []
    for repo, competition, repo_root, path in files(root):
        relative = path.relative_to(repo_root)
        source = 'https://github.com/openfootball/%s/blob/master/%s' % (repo, relative)
        print('openfootball/%s/%s' % (repo, relative))
        games.extend(process_file(path, competition, source))
    return games


def process_file(path, competition, source=None):
    path = Path(path)
    if source is None:
        source = path.as_uri()
    with path.open(encoding='utf-8-sig') as stream:
        return process_lines(stream, competition, source)


def process_lines(lines, competition, source, today=None):
    if today is None:
        today = datetime.date.today()
    games = []
    season = None
    date = None
    heading = None
    expected = None

    for line_number, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line:
            continue

        header = HEADER_RE.match(line)
        if header:
            season = _season(header.group('year'), header.group('end'))
            continue

        if line.startswith('# Matches'):
            expected = int(line.split()[2])
            continue

        if line.startswith('▪'):
            heading = line.removeprefix('▪').strip()
            continue

        date_match = DATE_RE.match(line)
        if date_match:
            if season is None:
                raise ValueError('%s:%d: date appears before season header' % (source, line_number))
            date = _date(date_match, season)
            continue

        if date is None or heading is None:
            continue

        match = _match(line)
        if match is None:
            continue

        game_competition, game_season, stage, group, round_ = _context(
            competition, season, heading
        )
        team1, team2, score1, score2, penalty1, penalty2, note, aet = match
        if date.date() > today:
            score1 = score2 = penalty1 = penalty2 = None
            aet = False
        neutral = game_competition == 'UEFA Champions League' and round_ == 'Final'
        line_source = '%s#L%d' % (source, line_number)
        lower_note = note.lower()
        games.append({
            'gid': hashlib.sha1(line_source.encode()).hexdigest(),
            'competition': game_competition,
            'season': game_season,
            'round': round_,
            'group': group,
            'stage': stage,
            'date': date,
            'team1': team1,
            'team2': team2,
            'home_team': None if neutral else team1,
            'neutral': neutral,
            'result_unknown': False,
            'not_played': any(word in lower_note for word in (
                'abandoned', 'cancelled', 'postponed',
            )),
            'forfeit': 'awarded' in lower_note,
            'team1_score': score1,
            'team2_score': score2,
            'team1_result': None,
            'team2_result': None,
            'shootout_winner': _shootout_winner(team1, team2, penalty1, penalty2),
            'location': '',
            'referee': None,
            'linesmen': [],
            'attendance': None,
            'minigame': False,
            'sources': [line_source],
            'notes': note,
            'video': '',
            'minutes': 120 if aet else 90,
        })

    if season is None:
        raise ValueError('%s: missing season header' % source)
    if expected is not None and len(games) != expected:
        raise ValueError('%s: expected %d matches, parsed %d' % (source, expected, len(games)))
    return games


def _season(start, end):
    if end is None:
        return start
    if len(end) == 2:
        century = int(start[:2])
        if int(end) < int(start[-2:]):
            century += 1
        end = str(century * 100 + int(end))
    return '%s-%s' % (start, end)


def _date(match, season):
    month = datetime.datetime.strptime(match.group('month'), '%b').month
    year = match.group('year')
    if year is None:
        start, separator, end = season.partition('-')
        year = start if not separator or month >= 7 else end
    return datetime.datetime(int(year), month, int(match.group('day')))


def _match(line):
    line = TIME_RE.sub('', line, count=1).strip()
    note = ''

    if ' v ' in line:
        team1, rest = line.split(' v ', 1)
        score = SCORE_RE.search(rest)
        if score:
            team2 = rest[:score.start()].strip()
        else:
            team2 = rest
            note_match = re.search(r'\s+\[([^]]+)\]$', team2)
            if note_match:
                note = note_match.group(1)
                team2 = team2[:note_match.start()].strip()
        return _match_parts(team1, team2, score, note)

    score = NO_V_RE.match(line)
    if score is None:
        return None
    return _match_parts(score.group('team1'), score.group('team2'), score, note)


def _match_parts(team1, team2, score, note):
    if score:
        score1 = int(score.group('score1'))
        score2 = int(score.group('score2'))
        penalty1 = _int_or_none(score.group('pen1'))
        penalty2 = _int_or_none(score.group('pen2'))
        note = score.group('note') or note
        aet = bool(score.group('aet'))
    else:
        score1 = score2 = penalty1 = penalty2 = None
        aet = False

    team1 = COUNTRY_SUFFIX_RE.sub('', team1).strip()
    team2 = COUNTRY_SUFFIX_RE.sub('', team2).strip()
    if not team1 or not team2:
        return None
    return team1, team2, score1, score2, penalty1, penalty2, note, aet


def _int_or_none(value):
    return int(value) if value is not None else None


def _shootout_winner(team1, team2, penalty1, penalty2):
    if penalty1 is None:
        return None
    return team1 if penalty1 > penalty2 else team2


def _context(competition, season, heading):
    stage = ''
    group = ''
    round_ = heading

    if competition == 'Major League Soccer' and heading.startswith('Playoffs,'):
        competition = 'MLS Cup Playoffs'
        stage = 'Playoffs'
        round_ = heading.split(',', 1)[1].strip()
    elif competition == 'Liga MX':
        phase = heading.split(',', 1)[0]
        if phase.startswith(('Apertura', 'Clausura')):
            half = phase.split()[0]
            season = '%s %s' % (season, half)
            if 'Playoffs' in phase:
                competition = 'Liga MX Liguilla'
            stage = phase
            round_ = heading.split(',', 1)[1].strip() if ',' in heading else None
    elif heading.startswith('Group '):
        group = heading.removeprefix('Group ').strip()
        round_ = None
    elif ',' in heading:
        stage, round_ = [part.strip() for part in heading.split(',', 1)]

    return competition, season, stage, group, round_

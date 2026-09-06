import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from metadata.utils import person_identity_key


ROOT = Path(__file__).resolve().parent.parent
COUNTRY_ALIASES = {
    'n. ireland': 'northern ireland',
    'northern ireland': 'northern ireland',
    'usa': 'united states',
    'u.s.a.': 'united states',
}


def clean_country(country):
    country = country.strip().casefold()
    return COUNTRY_ALIASES.get(country, country)


def read_semicolon_bios(path):
    bios = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith('*'):
            continue
        fields = [field.strip() for field in line.split(';')]
        fields.extend([None] * (3 - len(fields)))
        bios.append({
            'name': fields[0],
            'birthdate': fields[1],
            'birthplace': fields[2],
        })
    return bios


def read_nasl_stats(path):
    stats = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip() or line.startswith(('*', 'Key:', 'BlockSource:')):
            continue
        fields = [field.strip() for field in line.replace('\N{NO-BREAK SPACE}', '').split(';')]
        if len(fields) < 11 or not fields[4]:
            continue
        stats.append({
            'line': line_number,
            'team': fields[0],
            'season': fields[1],
            'name': fields[4],
            'nationality': fields[10],
        })
    return stats


def candidate_label(candidate):
    return '%s (%s)' % (candidate['name'], candidate['birthdate'] or 'birth date unknown')


def birthplace_country(candidate):
    if not candidate['birthplace']:
        return None
    return clean_country(candidate['birthplace'].rsplit(',', 1)[-1])


def nationality_countries(stat):
    return {clean_country(country) for country in stat['nationality'].split('/') if country.strip()}


def audit_nasl(root=ROOT):
    bios = read_semicolon_bios(root / 'metadata/data/people/nasl')
    stats = read_nasl_stats(root / 'usd1_data/data/stats/nasl')
    bios_by_key = defaultdict(list)
    stats_by_key = defaultdict(list)
    for bio in bios:
        bios_by_key[person_identity_key(bio['name'])].append(bio)
    for stat in stats:
        stats_by_key[person_identity_key(stat['name'])].append(stat)

    identities = []
    for key, candidates in sorted(bios_by_key.items()):
        birthdates = {candidate['birthdate'] for candidate in candidates if candidate['birthdate']}
        if len(birthdates) < 2:
            continue

        candidates = sorted(candidates, key=lambda candidate: candidate_label(candidate))
        occurrences = []
        for stat in sorted(stats_by_key[key], key=lambda row: (row['season'], row['team'], row['line'])):
            countries = nationality_countries(stat)
            supported = [
                candidate_label(candidate)
                for candidate in candidates
                if birthplace_country(candidate) in countries
            ]
            occurrences.append({
                **stat,
                'classification': 'supported' if len(supported) == 1 else 'unresolved',
                'candidates': supported or [candidate_label(candidate) for candidate in candidates],
            })

        identities.append({
            'key': key,
            'name': candidates[0]['name'],
            'candidates': candidates,
            'occurrences': occurrences,
        })

    return identities


def read_asl_stats(path):
    stats = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip() or line.startswith('*'):
            continue
        fields = line.split('\t')
        stats.append({
            'line': line_number,
            'name': fields[0].strip(),
            'team': fields[1].strip(),
            'season': fields[2].strip(),
        })
    return stats


def read_asl_bio_names(root=ROOT):
    names = {bio['name'] for bio in read_semicolon_bios(root / 'metadata/data/people/asl')}
    for line in (root / 'metadata/data/people/asl_bios.csv').read_text().splitlines():
        if line.strip() and not line.startswith('*'):
            names.add(line.split(';', 1)[0].strip())
    return names


def is_abbreviated_name(name):
    first = name.split()[0]
    return bool(re.fullmatch(r'(?:[A-Za-z]\.)+', first))


def abbreviation_matches(abbreviation, candidate):
    short_parts = abbreviation.split()
    candidate_parts = candidate.split()
    if len(candidate_parts) < 2 or is_abbreviated_name(candidate):
        return False
    if person_identity_key(short_parts[-1]) != person_identity_key(candidate_parts[-1]):
        return False

    initials = ''.join(character.casefold() for character in short_parts[0] if character.isalpha())
    candidate_initials = ''.join(part[0].casefold() for part in candidate_parts[:-1] if part)
    return candidate_initials.startswith(initials)


def audit_asl(root=ROOT):
    stats = read_asl_stats(root / 'usd1_data/data/stats/asl')
    full_names = read_asl_bio_names(root)
    full_names.update(stat['name'] for stat in stats if not is_abbreviated_name(stat['name']))

    contexts = defaultdict(set)
    for stat in stats:
        if not is_abbreviated_name(stat['name']):
            contexts[stat['name']].add((stat['team'], stat['season']))

    rows = []
    for stat in stats:
        if not is_abbreviated_name(stat['name']):
            continue
        candidates = sorted(name for name in full_names if abbreviation_matches(stat['name'], name))
        same_team = [
            candidate for candidate in candidates
            if any(team == stat['team'] for team, _ in contexts[candidate])
        ]
        if len(same_team) == 1:
            classification = 'supported'
            matches = same_team
            evidence = 'same-team career'
        elif len(candidates) == 1:
            classification = 'candidate'
            matches = candidates
            evidence = 'unique initial-and-surname match'
        else:
            classification = 'unresolved'
            matches = candidates
            evidence = None
        rows.append({
            **stat,
            'classification': classification,
            'candidates': matches,
            'evidence': evidence,
        })

    return sorted(rows, key=lambda row: (row['name'], row['season'], row['team'], row['line']))


def audit(root=ROOT):
    nasl = audit_nasl(root)
    asl = audit_asl(root)
    return {
        'nasl': {
            'ambiguous_identities': len(nasl),
            'classifications': dict(sorted(Counter(
                occurrence['classification']
                for identity in nasl
                for occurrence in identity['occurrences']
            ).items())),
            'identities': nasl,
        },
        'asl': {
            'abbreviated_rows': len(asl),
            'distinct_abbreviations': len({row['name'] for row in asl}),
            'classifications': dict(sorted(Counter(row['classification'] for row in asl).items())),
            'rows': asl,
        },
    }


def format_markdown(report):
    lines = [
        '# Player identity audit',
        '',
        '## NASL',
        '',
        '%s normalized names have conflicting birth dates.' % report['nasl']['ambiguous_identities'],
        '',
    ]
    for identity in report['nasl']['identities']:
        lines.extend(['### %s' % identity['name'], ''])
        for candidate in identity['candidates']:
            lines.append('- %s — %s' % (candidate_label(candidate), candidate['birthplace'] or 'birthplace unknown'))
        lines.extend(['', '| Season | Team | Nationality | Classification | Candidates |',
                      '| --- | --- | --- | --- | --- |'])
        for row in identity['occurrences']:
            lines.append('| %s | %s | %s | %s | %s |' % (
                row['season'], row['team'], row['nationality'], row['classification'],
                ', '.join(row['candidates'])))
        lines.append('')

    asl = report['asl']
    lines.extend([
        '## ASL',
        '',
        '%s abbreviated stat rows use %s distinct abbreviations.' % (
            asl['abbreviated_rows'], asl['distinct_abbreviations']),
        '',
        '| Classification | Rows |',
        '| --- | ---: |',
    ])
    for classification, count in asl['classifications'].items():
        lines.append('| %s | %s |' % (classification, count))

    lines.extend(['', '### Supported and candidate matches', '',
                  '| Name | Team | Season | Classification | Candidate | Evidence |',
                  '| --- | --- | --- | --- | --- | --- |'])
    for row in asl['rows']:
        if row['classification'] == 'unresolved':
            continue
        lines.append('| %s | %s | %s | %s | %s | %s |' % (
            row['name'], row['team'], row['season'], row['classification'],
            ', '.join(row['candidates']), row['evidence']))

    unresolved = Counter(row['name'] for row in asl['rows'] if row['classification'] == 'unresolved')
    lines.extend(['', '### Unresolved abbreviations', '', '| Name | Rows |', '| --- | ---: |'])
    for name, count in sorted(unresolved.items()):
        lines.append('| %s | %s |' % (name, count))
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', choices=('json', 'markdown'), default='markdown')
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    report = audit(args.root)
    if args.format == 'json':
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_markdown(report), end='')


if __name__ == '__main__':
    main()

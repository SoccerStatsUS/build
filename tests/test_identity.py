from identity import abbreviation_matches, audit_asl, audit_nasl, format_markdown


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_nasl_nationality_supports_one_homonym(tmp_path):
    write(tmp_path / 'metadata/data/people/nasl', """\
Jimmy Kelly; 5/2/1957; Carlisle, England
Jimmy Kelly; 2/6/1954; Aldergrove, Northern Ireland
""")
    write(tmp_path / 'usd1_data/data/stats/nasl', """\
Key: team; season; competition; number; name; position; games_played; goals; assists; points; nationality
Portland Timbers; 1975; North American Soccer League; 11; Jimmy Kelly; F; 20; 2; 8; 12; N. Ireland
Chicago Sting; 1976; North American Soccer League; 6; Jimmy Kelly; M; 21; 5; 2; 12; England
""")

    identities = audit_nasl(tmp_path)

    assert len(identities) == 1
    assert [row['candidates'] for row in identities[0]['occurrences']] == [
        ['Jimmy Kelly (2/6/1954)'],
        ['Jimmy Kelly (5/2/1957)'],
    ]
    assert {row['classification'] for row in identities[0]['occurrences']} == {'supported'}


def test_nasl_keeps_shared_nationality_unresolved(tmp_path):
    write(tmp_path / 'metadata/data/people/nasl', """\
Peter Daniel; 12/22/1946; Ripley, England
Peter Daniel; 12/12/1955; Hull, England
""")
    write(tmp_path / 'usd1_data/data/stats/nasl', """\
Vancouver Whitecaps; 1978; North American Soccer League; 17; Peter Daniel; D; 20; 1; 0; 2; England
""")

    row = audit_nasl(tmp_path)[0]['occurrences'][0]

    assert row['classification'] == 'unresolved'
    assert len(row['candidates']) == 2


def test_abbreviation_matching_uses_all_supplied_initials():
    assert abbreviation_matches('F.G. Carnegie', 'Frederick George Carnegie')
    assert not abbreviation_matches('F.G. Carnegie', 'Fred Carnegie')
    assert not abbreviation_matches('J. Brown', 'Jimmy Black')


def test_asl_prefers_a_unique_same_team_candidate(tmp_path):
    write(tmp_path / 'metadata/data/people/asl', """\
James Brown;; Scotland
John Brown;; England
""")
    write(tmp_path / 'metadata/data/people/asl_bios.csv', '')
    write(tmp_path / 'usd1_data/data/stats/asl', """\
James Brown\tNewark\t23-24\t1
J. Brown\tNewark\t24-25\t2
John Brown\tBoston\t24-25\t3
""")

    row = audit_asl(tmp_path)[0]

    assert row['classification'] == 'supported'
    assert row['candidates'] == ['James Brown']
    assert row['evidence'] == 'same-team career'


def test_asl_does_not_claim_an_ambiguous_global_match(tmp_path):
    write(tmp_path / 'metadata/data/people/asl', """\
James Brown;; Scotland
John Brown;; England
""")
    write(tmp_path / 'metadata/data/people/asl_bios.csv', '')
    write(tmp_path / 'usd1_data/data/stats/asl', 'J. Brown\tNewark\t24-25\t2\n')

    row = audit_asl(tmp_path)[0]

    assert row['classification'] == 'unresolved'
    assert row['candidates'] == ['James Brown', 'John Brown']


def test_markdown_report_is_deterministic(tmp_path):
    write(tmp_path / 'metadata/data/people/nasl', '')
    write(tmp_path / 'usd1_data/data/stats/nasl', '')
    write(tmp_path / 'metadata/data/people/asl', 'Bow Ford;; Scotland\n')
    write(tmp_path / 'metadata/data/people/asl_bios.csv', '')
    write(tmp_path / 'usd1_data/data/stats/asl', 'B. Ford\tNewark\t24-25\t2\n')

    report = {
        'nasl': {'ambiguous_identities': 0, 'classifications': {}, 'identities': audit_nasl(tmp_path)},
        'asl': {
            'abbreviated_rows': 1,
            'distinct_abbreviations': 1,
            'classifications': {'candidate': 1},
            'rows': audit_asl(tmp_path),
        },
    }

    assert '| B. Ford | Newark | 24-25 | candidate | Bow Ford |' in format_markdown(report)

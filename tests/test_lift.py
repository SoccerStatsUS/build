from helpers import string_to_ascii
from lift import get_name_from_fragment


def candidates(*names):
    """Rosters are stored as (ascii_name, name) pairs; build that from full names."""
    return {(string_to_ascii(n), n) for n in names}


def test_string_to_ascii_folds_accents():
    assert string_to_ascii('Cuscatlán') == 'cuscatlan'
    assert string_to_ascii('Özil') == 'ozil'
    assert string_to_ascii('Šuker') == 'suker'


def test_string_to_ascii_lowercases():
    assert string_to_ascii('Thierry Henry') == 'thierry henry'


def test_surname_lifts_to_full_name():
    # The example from README.md.
    c = candidates('Thierry Henry', 'Patrick Vieira')
    assert get_name_from_fragment('Henry', c) == 'Thierry Henry'


def test_full_name_is_left_alone():
    # A fragment equal to a candidate is excluded, so lifting is idempotent.
    c = candidates('Thierry Henry', 'Patrick Vieira')
    assert get_name_from_fragment('Thierry Henry', c) == 'Thierry Henry'


def test_ambiguous_surname_is_left_alone():
    c = candidates('Willie Reid', 'Mike Reid')
    assert get_name_from_fragment('Reid', c) == 'Reid'


def test_no_match_is_left_alone():
    c = candidates('Thierry Henry', 'Patrick Vieira')
    assert get_name_from_fragment('Donovan', c) == 'Donovan'


def test_initial_disambiguates_shared_surname():
    c = candidates('Willie Reid', 'Mike Reid')
    assert get_name_from_fragment('W. Reid', c) == 'Willie Reid'


def test_initial_matching_nobody_is_left_alone():
    c = candidates('Willie Reid', 'Mike Reid')
    assert get_name_from_fragment('Z. Reid', c) == 'Z. Reid'


def test_accented_fragment_matches_accented_candidate():
    c = candidates('Cuauhtémoc Blanco', 'Kevin Hartman')
    assert get_name_from_fragment('Blanco', c) == 'Cuauhtémoc Blanco'


def test_unaccented_fragment_matches_accented_candidate():
    # The point of storing ascii_name: sources spell the surname both ways.
    c = candidates('Mesut Özil', 'Kevin Hartman')
    assert get_name_from_fragment('Ozil', c) == 'Mesut Özil'


def test_unaccented_full_name_is_not_restored():
    # Documents a limit: the `ascii != ascii_fragment` guard that makes lifting
    # idempotent also means a fully-spelled unaccented name is left alone here.
    # Restoring accents on a full name is normalize's job, via the alias tables.
    c = candidates('Cuauhtémoc Blanco', 'Kevin Hartman')
    assert get_name_from_fragment('Cuauhtemoc Blanco', c) == 'Cuauhtemoc Blanco'


def test_embedded_name_matches():
    # Handles Sabah -> Miguel Sabah Gerardo, where the fragment is interior.
    c = candidates('Miguel Sabah Gerardo', 'Kevin Hartman')
    assert get_name_from_fragment('Sabah', c) == 'Miguel Sabah Gerardo'


def test_none_fragment_passes_through():
    assert get_name_from_fragment(None, candidates('Thierry Henry')) is None


def test_empty_candidates_leaves_fragment_alone():
    assert get_name_from_fragment('Henry', set()) == 'Henry'

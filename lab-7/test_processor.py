"""Run with: python -m pytest test_processor.py -q

Use the same tests before and after replacing tennis_scoring.py.
The unfinished test_tennis_scoring.py from the repo is not needed for this run.
"""

import re

import pytest
from hypothesis import example, given, settings, strategies as st

from tennis_scoring import game_lead, parse_score, set_spread


# A bounded mix of valid types, wrong types and nested containers.
atom = st.one_of(st.none(), st.booleans(), st.integers(), st.floats(),
                 st.text(max_size=200), st.binary(max_size=100))
inputs = st.one_of(atom, st.lists(atom, max_size=10),
                   st.dictionaries(st.text(max_size=20), atom, max_size=5),
                   st.tuples(atom, atom))
counts = st.integers(min_value=0, max_value=10**12)
labels = ('0', '15', '30', '40')
padding = st.sampled_from(('', ' ', '\t', '\n', '  '))


def expected_counts(value, separator, required_length=None):
    """Independent format oracle for bounded fuzz strings."""
    if not isinstance(value, str):
        return None
    fields = value.split(separator)
    if required_length is not None and len(fields) != required_length:
        return None
    if any(re.fullmatch(r'[0-9]+', field.strip()) is None for field in fields):
        return None
    try:
        return [int(field.strip()) for field in fields]
    except ValueError:
        return None


@settings(max_examples=300, deadline=None)
@given(inputs)
@example(None)
@example('')
@example('3-2')
def test_parse_score_no_crash(value):
    parsed = expected_counts(value, '-', 2)
    expected = None if parsed is None else tuple(parsed)
    assert parse_score(value) == expected


@settings(max_examples=300, deadline=None)
@given(inputs)
@example(None)
@example('')
@example('40-30')
def test_game_lead_no_crash(value):
    expected = None
    if isinstance(value, str):
        parts = [field.strip() for field in value.split('-')]
        if len(parts) == 2 and all(field in labels for field in parts):
            expected = labels.index(parts[0]) - labels.index(parts[1])
    assert game_lead(value) == expected


@settings(max_examples=300, deadline=None)
@given(inputs)
@example(None)
@example('')
@example('6,4,7')
def test_set_spread_no_crash(value):
    parsed = expected_counts(value, ',')
    expected = None if parsed is None else max(parsed) - min(parsed)
    assert set_spread(value) == expected


@given(counts, counts, padding)
def test_parse_score_valid(a, b, space):
    assert parse_score(f'{space}{a}{space}-{space}{b}{space}') == (a, b)


@given(st.sampled_from(labels), st.sampled_from(labels), padding)
def test_game_lead_valid(a, b, space):
    result = game_lead(f'{space}{a}{space}-{space}{b}{space}')
    assert result == labels.index(a) - labels.index(b)
    assert result == -game_lead(f'{b}-{a}')


@given(st.lists(counts, min_size=1, max_size=50), padding)
def test_set_spread_valid(games, space):
    value = ','.join(f'{space}{game}{space}' for game in games)
    assert set_spread(value) == max(games) - min(games)
    assert set_spread(','.join(map(str, reversed(games)))) == set_spread(value)


@pytest.mark.parametrize('a', labels)
@pytest.mark.parametrize('b', labels)
def test_all_game_labels(a, b):
    assert game_lead(f'{a}-{b}') == labels.index(a) - labels.index(b)


@pytest.mark.parametrize('value', [
    None, 42, True, 3.5, b'3-2', [], {}, '', ' ', '3', '3-2-1',
    '-1-2', '1--2', '1.5-2', '+3-2', 'a-b', '3-', '-2',
    '1_0-2', '\u00b2-2', '\u0663-2', '3\x00-2',
])
def test_parse_score_invalid(value):
    assert parse_score(value) is None


@pytest.mark.parametrize('value', [
    None, 42, True, b'40-30', [], {}, '', ' ', '40', '40-30-0',
    '45-30', '1-0', 'AD-40', 'forty-30', '015-30', '+15-0',
    '40-', '-30', '40--30', '40.0-30', '\u0664\u0660-30',
])
def test_game_lead_invalid(value):
    assert game_lead(value) is None


@pytest.mark.parametrize('value', [
    None, 42, True, b'6,4,7', [], {}, '', ' ', ',', '6,,7',
    '6,', ',6', '-1,6', '6.5,4', 'six,4', '+6,4', '1_0,4',
    '\u00b2,4', '\u0666,4', '6\x00,4',
])
def test_set_spread_invalid(value):
    assert set_spread(value) is None


@pytest.mark.parametrize('function,value,expected', [
    (parse_score, ' 003 - 02 ', (3, 2)),
    (parse_score, '0-0', (0, 0)),
    (game_lead, ' 40 - 30 ', 1),
    (game_lead, '15-40', -2),
    (game_lead, '40-40', 0),
    (set_spread, '6,4,7', 3),
    (set_spread, '6', 0),
    (set_spread, '0,0', 0),
    (set_spread, ' 06 , 4 , 07 ', 3),
])
def test_regressions(function, value, expected):
    assert function(value) == expected


@pytest.mark.parametrize('function,suffix', [(parse_score, '-0'), (set_spread, ',0')])
def test_very_long_integer_does_not_crash(function, suffix):
    # Some Python versions limit integer conversion length; others accept it.
    # Either outcome must be handled without a crash.
    value = '9' * 5000
    try:
        number = int(value)
    except ValueError:
        expected = None
    else:
        expected = (number, 0) if function is parse_score else number
    assert function(value + suffix) == expected

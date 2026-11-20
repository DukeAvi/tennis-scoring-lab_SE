import pytest

from tennis_scoring import game_score, set_winner, match_status


# Negative-point validation: both operands and both outcomes
@pytest.mark.parametrize(
    "a, b",
    [
        (-1, 0),
        (0, -1),
        (0, 0),
    ],
)
def test_negative_point_branches(a, b):
    if a < 0 or b < 0:
        with pytest.raises(ValueError):
            game_score(a, b)
    else:
        assert game_score(a, b) == "0-0"


# The two conditions deciding whether scoring is in deuce territory
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, "30-40"),
        (3, 2, "40-30"),
        (3, 3, "deuce"),
        (4, 3, "advantage A"),
        (3, 4, "advantage B"),
        (5, 3, "game A"),
        (3, 5, "game B"),
        (4, 0, "game A"),
        (0, 4, "game B"),
        (2, 2, "30-30"),
    ],
)
def test_game_score_branches(a, b, expected):
    assert game_score(a, b) == expected


# Set-winning conditions, including each special tiebreak case
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 0, "A"),
        (6, 5, None),
        (5, 6, None),
        (0, 6, "B"),
        (6, 6, None),
        (7, 6, "A"),
        (6, 7, "B"),
        (5, 5, None),
        (7, 5, "A"),
        (5, 7, "B"),
    ],
)
def test_set_winner_branches(a, b, expected):
    assert set_winner(a, b) == expected


# Match outcomes: both winners, decider, and in-progress cases
@pytest.mark.parametrize(
    "sets_a, sets_b, best_of, expected",
    [
        (2, 0, 3, "A wins"),
        (0, 2, 3, "B wins"),
        (1, 1, 3, "decider"),
        (1, 0, 3, "in progress"),
        (0, 1, 3, "in progress"),
        (0, 0, 3, "in progress"),
        (3, 1, 5, "A wins"),
        (1, 3, 5, "B wins"),
        (2, 2, 5, "decider"),
    ],
)
def test_match_status_branches(sets_a, sets_b, best_of, expected):
    assert match_status(sets_a, sets_b, best_of) == expected

import pytest

from tennis_scoring import game_score, set_winner, match_status


# Game scoring: ordinary points
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 0, "0-0"),
        (1, 0, "15-0"),
        (2, 1, "30-15"),
        (3, 0, "40-0"),
        (0, 3, "0-40"),
    ],
)
def test_ordinary_game_scores(a, b, expected):
    assert game_score(a, b) == expected


# Game scoring: invalid inputs
@pytest.mark.parametrize("a, b", [(-1, 0), (0, -1)])
def test_negative_points_raise_error(a, b):
    with pytest.raises(ValueError, match="negative points"):
        game_score(a, b)


# Game scoring: non-deuce winning conditions
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (4, 0, "game A"),
        (0, 4, "game B"),
    ],
)
def test_game_winner_before_deuce(a, b, expected):
    assert game_score(a, b) == expected


# Game scoring: deuce and advantage
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (3, 3, "deuce"),
        (4, 4, "deuce"),
        (5, 3, "game A"),
        (3, 5, "game B"),
        (4, 3, "advantage A"),
        (3, 4, "advantage B"),
    ],
)
def test_deuce_advantage_and_winners(a, b, expected):
    assert game_score(a, b) == expected


# Set winner
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 0, "A"),
        (6, 4, "A"),
        (0, 6, "B"),
        (4, 6, "B"),
        (7, 6, "A"),
        (6, 7, "B"),
        (5, 5, None),
        (6, 5, None),
        (5, 6, None),
        (6, 6, None),
    ],
)
def test_set_winner(a, b, expected):
    assert set_winner(a, b) == expected


# Match status: best-of-three
@pytest.mark.parametrize(
    "sets_a, sets_b, best_of, expected",
    [
        (2, 0, 3, "A wins"),
        (0, 2, 3, "B wins"),
        (1, 1, 3, "decider"),
        (1, 0, 3, "in progress"),
        (0, 0, 3, "in progress"),
    ],
)
def test_match_status(sets_a, sets_b, best_of, expected):
    assert match_status(sets_a, sets_b, best_of) == expected

"""Lab 7 tennis scoring with input validation.

Invalid inputs return None. Surrounding whitespace is allowed, but numeric
fields must contain only ASCII digits and represent non-negative integers.
"""


def _non_negative_int(value):
    value = value.strip()
    if not value or not value.isascii() or not value.isdecimal():
        return None
    try:
        return int(value)
    except ValueError:
        # Python may reject unusually long integer strings.
        return None


def parse_score(text):
    """Return the two point tallies in A-B format, or None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('-')
    if len(parts) != 2:
        return None
    a = _non_negative_int(parts[0])
    b = _non_negative_int(parts[1])
    if a is None or b is None:
        return None
    return a, b


def game_lead(text):
    """Return A's lead in point steps using the labels 0, 15, 30 and 40."""
    if not isinstance(text, str):
        return None
    parts = text.split('-')
    if len(parts) != 2:
        return None
    first, second = (part.strip() for part in parts)
    points = {'0': 0, '15': 1, '30': 2, '40': 3}
    if first not in points or second not in points:
        return None
    return points[first] - points[second]


def set_spread(games_csv):
    """Return max minus min for a nonempty CSV of game counts, or None."""
    if not isinstance(games_csv, str):
        return None
    games = [_non_negative_int(game) for game in games_csv.split(',')]
    if any(game is None for game in games):
        return None
    return max(games) - min(games)


def main():
    print("==== Running parse_score ====")
    user_input = input("Enter points won as A-B (e.g. 3-2): ")
    result = parse_score(user_input)
    print("Points A and B:", result)

    print("\n==== Running game_lead ====")
    user_input = input("Enter a game score (e.g. 40-30): ")
    result = game_lead(user_input)
    print("Lead in Points:", result)

    print("\n==== Running set_spread ====")
    user_input = input("Enter games won per set as CSV (e.g. 6,4,7): ")
    result = set_spread(user_input)
    print("Spread:", result)


if __name__ == "__main__":
    main()

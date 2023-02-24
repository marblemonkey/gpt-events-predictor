import math


def round_to_significant_digits(n, digits):
    """Rounds a number to the specified number of significant digits."""

    if n == 0:
        return 0
    return round(n, -int(math.floor(math.log10(abs(n)))) + (digits - 1))

import functools
import itertools

from test_framework import generic_test


def roman_to_integer(s: str) -> int:
    """
    Start: 18:06
    I = 1
    V = 5
    X = 10

    XI = 11
    VI = 6

    VII = 7

    IIIX = 7 ???? NO!  it says I can immediately precede, V and X

    XIV
    10 + 4 = 14

    Input is guaranteed to be valid.

    iterate through the array...
    groupby
    get the total of the group
    look at the next number, if it's smaller than the previous group (or we're at the end), add the previous total
    otherwise subtract the previous total

    LIX
    1L1I1X
    (50)(1)(10)
     ?  50  49 59

    O(n) time complexity -> n is len of string
    O(1) space complexity

    Finished 18:34 about 30 mins.

    A good point is 'why did I bother grouping stuff'??? It's not required and makes the code more complex.
    It also explains why they worded the question the way they did.  why they say 'immediately preceding'.
    """
    lookup = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    prev_total = None
    for c, group in itertools.groupby(s):
        count = functools.reduce(lambda p, _: p + 1, group, 0)
        total = lookup[c] * count
        if prev_total is not None:
            if prev_total < total:
                result -= prev_total
            else:
                result += prev_total
        prev_total = total
    if prev_total is not None:
        result += prev_total
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "roman_to_integer.py", "roman_to_integer.tsv", roman_to_integer
        )
    )

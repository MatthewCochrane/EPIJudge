from typing import List

from test_framework import generic_test


def smallest_nonconstructible_value(A: List[int]) -> int:
    """
    Start: 9:55
    Find the smallest value that we cannot construct from the list of values given.

    Example:
        A: 1,1,2
        can construct
        1 -> 1
        2 -> 1,1 or 2
        3 -> 1,2
        4 -> no
        Here the result is just sum(A) + 1
        This is always the 'worst case' result.  We obviously can't sum to the sum + 1

    Example:
        1,1,10
        1 -> 1
        2 -> 1,1
        3 -> no
        Here the result is 3

    Example:
        2,3,4
        1 -> no
        Result is 1

    Example:
        1,2,3,9
        1,3,6,
        1 -> 1
        2 -> 2
        3 -> 3
        4 -> 3,1
        5 -> 3,2
        6 -> 3,2,1
        7 -> no

    Example:
        1,2,3,3,3,  9,20
        1,3,6,9,12,21,41
        1 -> 1
        2 -> 2
        3 -> 3
        4 -> 3,1
        5 -> 3,2
        6 -> 3,3
        7 -> 3,3,1
        ...
        9 -> 9
        10 -> 9,1
        11, 9,2

        We know we can reach any number up to x - 1
        so if we can also reach x, then we can reach any number up to 2x-1

        sort A
        total = 0
        for v in A:
            if v > total + 1:
                return total + 1
            total += v



    Have to be able to 'make it' to the next number before you can start using it.

    One approach:
    sort
    sum from left to right.
    If the sum is less than the next number, return the sum + 1
    """
    A.sort()
    total = 0
    for v in A:
        if v > total + 1:
            return total + 1
        total += v
    return total + 1


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('smallest_nonconstructible_value.py',
                                       'smallest_nonconstructible_value.tsv',
                                       smallest_nonconstructible_value))

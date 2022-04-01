from bisect import bisect_left
from typing import List

from test_framework import generic_test


def search_smallest(A: List[int]) -> int:
    """
    Start: 15:49
    Find the position of the smallest element in a cyclically sorted array.

    example

    1 2 3 4 5 6
    shift
    5 6 1 2 3 4
        |
    find the index that it was shifted to...

    If we think about how bisect works...
    where should i insert so that this is the first of this value

    5 6 1 2 3 4
    F F T T T T

    1 2 3 4 5
    F F F F F

    2 3 4 5 1
    F F F F T

    class Helper:
        def __getitem__(self, i):
            return A[i] < A[0]

    return bisect_left(Helper(), True, 0, len(A)) % len(A)


    O(log n) time, O(1) space
    All passed first run.
    Finish: 16:00
    Took 11 mins
    """
    class Helper:
        def __getitem__(self, i):
            return A[i] < A[0]

    # Convert A into a sequence of falses before the start and true's after the start.
    return bisect_left(Helper(), True, 0, len(A)) % len(A)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_shifted_sorted_array.py',
                                       'search_shifted_sorted_array.tsv',
                                       search_smallest))

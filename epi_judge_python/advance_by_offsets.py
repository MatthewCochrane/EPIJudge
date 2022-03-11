from typing import List

from test_framework import generic_test


def can_reach_end(A: List[int]) -> bool:
    """
    Start 17:27
    integer -> maximum you can advance from that position in one move.
    Write a program which takes array of n ints, and returns whether it's possible
    to advance to the last index starting from the beginning.

    Example
        [3,3,1,0,2,0,1]
        [o,o,x,x,o,x,o]

    In this approach
    Start at the end of the array, mark the last value as true
    because you can get to here starting here.
    Then go to the next value back.
    Ask, can I get to the end of the array from here?
    Can we answer this question in O(1) time?
    In the naive approach we can answer this in O(val).
    Ie if the number is 2, check the next two values in the array
    and check if they are true.
    We can do better though.  Instead of recording the true/false
    values for every index in the array, record the earliest value
    that can get to the end.

    Try this again
    [3,3,1,0,2,0,1]
     |
    earliest = 0
    is idx + val >= earliest?, if so, earliest = idx
    return earliest == 0

    pseudo code
    earliest = len - 1
    traverse array in reverse:
        if we can get to earliest or past it from here, update earliest to idx
    return true we can get to the end from 0 (earliest == 0)

    Time complexity is O(n)
    Space: O(1)
    Time: 17:46 -> 19 mins.  Pretty good!
    """
    earliest = len(A) - 1
    for i in reversed(range(len(A) - 1)):
        if i + A[i] >= earliest:
            earliest = i
    return earliest == 0


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('advance_by_offsets.py',
                                       'advance_by_offsets.tsv',
                                       can_reach_end))

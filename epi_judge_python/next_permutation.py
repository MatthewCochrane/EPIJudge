import math
from typing import List

from test_framework import generic_test


def next_permutation(perm: List[int]) -> List[int]:
    """
    Start: 10:15
    Take an input permutation (perm) and return the next permutation.
    If the permutation is the last permutation, return an empty list.

    Example
    0123 -> 0132
    0132
    0213
    0231
    0312
    0321
    1023
    1032
    1203
    1230
    ...
    1320
    2310
    2013


     598764321


    Pseudo code
    search from right to left until you find a decrease
    swap that number with the rightmost number that's less than the number we found above
    reverse from the left swap to the end

    O(n) time -> two passes, may be able to get to one pass?
    O(1) space -> can do in place, or copy to new array
    Will write out in-place then we can optimise for one pass?

    Finish at 10:52
    Had a bug, was swapping with the wrong value.  Needed to put the next largest in the head not the smallest.
    """
    last_val = -math.inf
    decrease_idx = None
    for i in reversed(range(len(perm))):
        if perm[i] < last_val:
            decrease_idx = i
            break
        last_val = perm[i]
    if decrease_idx is None:
        # If there is no decrease it's the last permutation.
        # Return empty array as per the specification.
        return []
    # Copy perm so we don't mutate it
    result = perm[:]
    next_largest_idx = None
    for i in reversed(range(len(perm))):
        if perm[i] > perm[decrease_idx]:
            next_largest_idx = i
            break
    result[next_largest_idx], result[decrease_idx] = result[decrease_idx], result[next_largest_idx]
    # Reverse all values from decrease_idx to end
    l = decrease_idx + 1
    r = len(result) - 1
    while l < r:
        result[l], result[r] = result[r], result[l]
        l += 1
        r -= 1
    return result


if __name__ == "__main__":
    next_permutation([1,2,3])
    exit(
        generic_test.generic_test_main(
            "next_permutation.py", "next_permutation.tsv", next_permutation
        )
    )

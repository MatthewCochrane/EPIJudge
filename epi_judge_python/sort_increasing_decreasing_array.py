import heapq
import math
from typing import List

from test_framework import generic_test


def sort_k_increasing_decreasing_array(A: List[int]) -> List[int]:
    """
    Start: 21:19
    k-increasing decreasing increases k/2 times and decreases k/2 times kind of

    1 3 5 7 9
    1-increasing decreasing

    1 3 5 7 6 3 2
    2 - increasing decreasing

    1 3 5 7 6 3 2 8 9 10
    1 3 5 7 6 - all numbers that are increasing until we see one decrease
    2 3 - all decreasing until we see one increase
    8 9 10 - all increasing... etc.
    3-increasing decreasing

    We want to sort this.
    We can do this in O(n log n) time if we use a standard sorting algorithm...
    We have k sorted sub-lists.
    We can merge k sorted lists in O(k log n) time.
    So if we can find the start and end of each sublist we can do this in O(k log n)
    If we split this into separate lists, it would require O(n) space
    Or if we can use iterators etc. instead then we only need O(k) extra space.
    Nothing was said about the section lengths.

    Pseudo code
    range(a, b, x)
    lists = [] #[range(a,b,x)]
    prev = -inf
    start_idx = 0
    dir = 1 # 1 = increasing, -1 = decreasing
    for i, item in enumerate(data):
        if (dir == increasing and item < prev) or (dir == decreasing and item > prev):
            lists.append(islice(start_idx, i, dir))
    # add last one
    return list(heapq.merge(*lists))

    O(n + k log n) = O(k log n) time
    O(k) space

    Finished: 21:50
    """
    ranges = []
    prev = -math.inf
    start_idx = 0
    direction = 1  # 1 == increasing, -1 == decreasing
    for i, item in enumerate(A):
        if (direction == 1 and item < prev) or (direction == -1 and item > prev):
            rng = range(start_idx, i)
            if direction == -1:
                rng = reversed(rng)
            ranges.append(map(lambda idx: A[idx], rng))
            start_idx, direction = i, -direction
        prev = item
    rng = range(start_idx, len(A))
    if direction == -1:
        rng = reversed(rng)
    ranges.append(map(lambda idx: A[idx], rng))

    return list(heapq.merge(*ranges))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sort_increasing_decreasing_array.py",
            "sort_increasing_decreasing_array.tsv",
            sort_k_increasing_decreasing_array,
        )
    )

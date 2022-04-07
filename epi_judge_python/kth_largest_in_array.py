import heapq
import random
from typing import List

from test_framework import generic_test


# The numbering starts from one, i.e., if A = [3, 1, -1, 2]
# find_kth_largest(1, A) returns 3, find_kth_largest(2, A) returns 2,
# find_kth_largest(3, A) returns 1, and find_kth_largest(4, A) returns -1.
def find_kth_largest(k: int, A: List[int]) -> int:
    """
    Can do this in O(k) space and O(n log k) using a heap.

    Can we do better?
    Could we do this in less than n log k time?
    Could we do this in less than O(k) space?

    A better way to do this is to use quickselect.
    From my understanding quickselect is like quicksort but we don't recurse into both halves.

    So for quicksort we just need to
    1. pick a pivot
    2. move all items less than pivot to the left of it
    3. move all items greater than pivot to the right of it

    Now the pivot will be in its correct location.
    If we're looking for the kth largest

    2 4 8 3 9 1 7
    k=3
    pivot=7
    2 4 1 3 7 8 9
    if pos of sorted item = len(A) - k  (eg. 7-3=4 here)
    then the answer is that value
    if the pos of the sorted item is < len(A) - k then the answer is in that subarray.  Recurse into it.
    if the pos of the sorted item is > len(A) - k then the answer is in that subarray.  Recurse into it.

    def partition(left, right, pivot_pos):
        pivot_val = A[pivot_pos]
        end_pos = right
        swap pivot with A[end_pos]
        right -= 1
        while left < right:
            if left < pivot_val:
                left += 1
            elif right > pivot_val:
                right -= 1
            else:
                swap left and right
        swap left and end_pos


    result_pos = len(A) - k
    l, r = 0, len(A) - 1
    while l < r:
        pivot = rand between l and r
        partition the array between start and finish about the pivot.  The pivot will end up in it's position.
        pivot_pos = partition(l, r, pivot_pos)
        if pivot_pos == result_pos:
            return A[pivot_pos]
        elif pivot_pos < result_pos:
            r = pivot_pos - 1
        else:
            l = pivot_pos + 1
    """
    pass

if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "kth_largest_in_array.py", "kth_largest_in_array.tsv", find_kth_largest
        )
    )

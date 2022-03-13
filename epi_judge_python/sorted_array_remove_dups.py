import functools
import math
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


# Returns the number of valid entries after deletion.
def delete_duplicates(A: List[int]) -> int:
    """
    Start: 14:48
    Take a sorted array, update it so that all duplicates have been removed and remaining elements
    are shifted to the left.  Return the number of valid entries.  You cannot use library functions.

    Example 1:
        [1,1,1,2,3,4,5,5] - 8 elements
        [1,2,3,4,5,X,X,X]

    Example 2:
        [1,2,3]
        [1,2,3]

    Example 3:
        [9,9,9]
        [9,X,X]

    Example 4:
        []
        []

    Example 5:
        [1,1,2]
        [1,2,X]


    Walk Through
    [1,1,1,3,3,4,5,5] - 8 elements
    [1,3,4,5,3,1,1,5] - 8 elements
             n       |
    last_val = 5
    walk through the array, if you see a duplicate, move it to the end.
    walk through the array, if you see a unique number, leave it there, or move it forward to the next available spot
    if you see a duplicate, step the second pointer forward.
    This is O(n) time, O(1) space.

    Can we do better?  The array is sorted and we're not taking advantage of that.
    Do we need to look at every item in the array?  Not really.
    in an array like
    [1,1,1,1,1,1,1,1,1,1,2]
    we could see the 1, then immediately binary search to find the 2.
    Can do a bisect right searching for the place to put a 1 so that it would be the last 1.
    In this crafted example the time complexity is better.  In general this is
    O(k*log n) where k is the number of items in the result array and n is the number of items in the input array.
    This could be better than O(n) in certain situations, but will often be worse.
    Ok, let's go with the O(n) solution for now.  Which means we don't take advantage of the fact that it's sorted.
    If it wasn't sorted, we would still have a harder time getting to O(n) time O(1) space because you wouldn't have
    the duplicates grouped together and you'd probably have to use a hashmap or similar to remember what you'd seen.

    Pseudo code
    walk through the array, if you see a unique number, leave it there, or move it forward to the next available spot
    if you see a duplicate, step the second pointer forward.

    set the largest_seen number to -inf
    set pointer for next_insertion
    for each item in the array:
        if the number is > largest seen:
            move it to the next insertion pointer
            increment next insertion pointer
            set largest_seen to that number

    [1,1,1,3,3,4,5,5] - 8 elements
    largest_seen = -inf
    next_insertion = 0
    i = 0
    if 1 > largest (True):
    swap 1 with itself, no effect...
    next_ins += 1 = 1
    largest = 1
    i = 1
    if 1 > 1 (False)
    i = 2
    if 1 > 1 (False)
    i = 3
    if 3 > 1 (True)
    swap ary[1] with ary[3]
    [1,3,1,1,3,4,5,5]
    next_ins += 1 = 2
    largest = 3
    i = 4
    if 3 > 3 (False)
    i = 5
    if 4 > 3 True
    swap [2] with [5]
    [1,3,4,1,3,1,5,5]
    next_ins = 3
    largest = 4
    i = 6
    5 > 4
    swap [3] and [6]
    [1,3,4,5,3,1,1,5]
    nins = 4
    lrg = 5
    i = 7
    5 > 5 False
    i = 8 exit
    return nins

    O(n) time
    O(1) space

    Time: 15:16
    Time taken = 12 + 16 = 28 mins
    All passed first time :)
    Same solution as the book.

    A note that I probably should have re-considered the edge cases before running it.
    In the book they didn't use the largest_seen var, instead they just used the last written
    item in the array since it also contains that value.  I dunno, I think this is slightly
    more clear.  Much of a muchness.  This approach saves the -1's in some of the indexing
    the other way.
    """
    largest_seen = -math.inf
    next_insertion = 0
    for i, v in enumerate(A):
        if v > largest_seen:
            A[i], A[next_insertion] = A[next_insertion], A[i]
            next_insertion += 1
            largest_seen = v
    return next_insertion


@enable_executor_hook
def delete_duplicates_wrapper(executor, A):
    idx = executor.run(functools.partial(delete_duplicates, A))
    return A[:idx]


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sorted_array_remove_dups.py',
                                       'sorted_array_remove_dups.tsv',
                                       delete_duplicates_wrapper))

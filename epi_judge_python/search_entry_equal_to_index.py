import functools
from itertools import starmap
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook
import bisect


def search_entry_equal_to_its_index(A: List[int]) -> int:
    """
     Start: 15:07

           v
     FFFFFFTTTTTT

      l        r
     [-6,0,1,4,8,9,10,11,12,13,14]
       0 1 2 3 4 5 6  7  8  9  10

    -2-1 0 1 2 3 4 5
     0 1 2 3 4 5 6 7

     3 X   4
     3 4 5 6 7

     If A[i] > i then we can discard all elements to the right
     If A[i] < i then the number cannot be on the left

     class Helper:
         def __getitem__(self, i):
             return A[i] > i

     bisect.bisect_left(Helper(), True, 0, len(A))


    Finished: 15:34
    I think it's been a while since I've done binary search questions.
    You just need to find an increasing sequence
    """

    # a third way though it requires O(n) extra space
    def helper(idx, val):
        return val == idx

    i = bisect.bisect_left(list(starmap(helper, enumerate(A))), True)
    if i < len(A) and A[i] == i:
        return i
    return -1

    # I actually found this easier to code I think...
    # Second attempt.   Finished at 15:38
    # l, r = 0, len(A)
    # while l < r:
    #     mid = l + (r - l) // 2
    #     if A[mid] > mid:
    #         r = mid - 1
    #     elif A[mid] == mid:
    #         return mid
    #     else:
    #         l = mid + 1
    # return -1

    # First Attempt..
    # class Helper:
    #     def __getitem__(self, i):
    #         return A[i] >= i
    #
    # i = bisect.bisect_left(Helper(), True, 0, len(A))
    # if i < len(A) and A[i] == i:
    #     return i
    # return -1


@enable_executor_hook
def search_entry_equal_to_its_index_wrapper(executor, A):
    result = executor.run(functools.partial(search_entry_equal_to_its_index, A))
    if result != -1:
        if A[result] != result:
            raise TestFailure("Entry does not equal to its index")
    else:
        if any(i == a for i, a in enumerate(A)):
            raise TestFailure("There are entries which equal to its index")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "search_entry_equal_to_index.py",
            "search_entry_equal_to_index.tsv",
            search_entry_equal_to_its_index_wrapper,
        )
    )

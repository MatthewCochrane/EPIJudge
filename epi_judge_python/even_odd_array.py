import collections
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def even_odd(A: List[int]) -> None:
    """
    Input is an array of integers.  Reorder them so that the even entries appear first.
    It doesn't specify if we should preserver the ordering apart from this.

    Example 1:
        [1,2,3,4,5,6]
        [1,2,5,2,4,6]

    Example 2:
        [1,2]
        [1,2]

    Example 3:
        [2,1]
        [1,2]

    Example 4:
        [1,1,1]
        [1,1,1]

    Negative numbers aren't special.

    Approach 1:
        Sort the entries by odd/evenness
        O(n log n) time
        O(n) space

    Approach 2:
        Iterate through the array and swap positions.

        [2,1,3,3]
         | |
        [4,3,2,1]
           | |

        while l < r
            if l is even, increment l
            if r is odd, increment r
            if neither of those, then l is odd and r is even, so swap l and r and increment both

        O(n) time complexity
        O(1) space complexity

    Average and median time to run was the same in both approaches.  Timsort might be helping in approach 1.
    """
    l, r = 0, len(A) - 1
    while l < r:
        if A[l] % 2 == 0:
            # is even
            l += 1
        elif A[r] % 2:
            # is odd
            r -= 1
        else:
            A[l], A[r] = A[r], A[l]
            l += 1
            r -= 1


@enable_executor_hook
def even_odd_wrapper(executor, A):
    before = collections.Counter(A)

    executor.run(functools.partial(even_odd, A))

    in_odd = False
    for a in A:
        if a % 2 == 0:
            if in_odd:
                raise TestFailure("Even elements appear in odd part")
        else:
            in_odd = True
    after = collections.Counter(A)
    if before != after:
        raise TestFailure("Elements mismatch")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "even_odd_array.py", "even_odd_array.tsv", even_odd_wrapper
        )
    )

import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import PropertyName, TestFailure
from test_framework.test_utils import enable_executor_hook


def rearrange(A: List[int]) -> None:
    """
    Q 5.8
    Write a program that takes an array A of n numbers, and rearranges A's elements to get a new array B
    having the property that...
    B[0] <= B[1] >= B[2] <= B[3] >= B[4] <= B[5] >= ...

    Start: 15:20

    example of B
    1, 10, 2, 9, 8, ...

    Example 1
    Input:  1,2,3,4,5
    Result: 1,5,2,4,3
    Result: 1,4,2,5,3 (alternative correct answer)
    Result: 1,3,2,5,4 (alternative correct answer)
    1,7,3,4,5
    3,1,7,4,5
    1,3,4,5,7



    Example 2
    Input: 1,1,1,1,1
    Result: 1,1,1,1,1

    Example 3
    Input: 1,1,1,2,2,2
    Result: 1,2,1,2,1,2

    Example 4
    Input: 9,9,9,9,1
    Result: 1,9,9,9,9

    Example 5
    Input: 9,9,9,9,1,1
    Sorted: 1,1,9,9,9,9
    Result: 1,9,1,9,9,9

    A[i] -> A[even * 2] if even*2 < len

    Something like:
    next smallest, next largest, next smallest, next largest, ...

    Approach 1:
    sort
    build new array
    pop from left, pop from right consecutively
    O(n log n) time
    O(n) space for the extra array

    I don't think there's any way around sorting.....
    Fundamentally this question ask us to sort the array (into a non-standard order), so
    it shouldn't be possible to do this in better than Theta(n log n)

    Questions:
    Can we do it in O(1) space? Yes, should be able to.
    Can we do it in 'one pass' without rearranging after the sort? Not sure about this

    Approach 2:
    O(n log n) time, O(1) space approach
    sort in place
    two pointer thing

    Input: 1,1,1,1,2,2,2
           |           |
           1,1,1,1,2,2,2
             |         |
           1,2,1,1,2,2,1
               |     |
           1,2,1,1,2,2,1 A[2] < A[1] so do nothing
               |     |
           1,2,1,2,2,1,1
                 |   |
           1,2,1,2,2,1,1
                   ||
           1,2,1,2,1,2,1
                   | |

    Input: 1,2,3,4,5,6,7,8 start with l=1, r=len-1
             |           |
           1,8,3,4,5,6,7,2 swap l and r values, increment l by two and r by 1
             |           |
           1,8,3,7,5,6,4,2 swap l and r values, increment l by two and r by 1
                 |     |
           1,8,3,7,5,6,4,2 swap l and r values, increment l by two and r by 1
                     ||
           1,8,3,7,2,6,4,5 swap l and r values, increment l by two and r by 1
                   |     |

    Input: 1,2,3,4,5,6,7,8 start with l=1, r=len-1
             |           |
           1,8,3,4,5,6,7,2 swap, increment l by 1
               |         |
           1,8,2,4,5,6,7,3 swap
               |       `|

    Input: 1,2,3,4,5,6,7,8 start with l=1, r=len-1
    Input:   1,2,3,4,5,6,7,8 start with l=1, r=len-1
    Want to reverse and offset

    Is it easy to calculate the new location for each index?
    eg. i=0 goes to i=0
    i=1 goes to ...

    A[i] -> A[even * 2] if even*2 < len
    Input: 1,2,3,4,5,6,7,8
           0 1 2 3 4 5 6 7
           0 2 4 6 ? ? ? ?
           ? ? ? ? 7 5 3 1
           0 2 4 6 7 5 3 1
           0 7 1 6 3 5 3 4
    working from the end... A[len-1-k] -> A[(k*2)+1]

    Steps...
    A[0] stays where it is
    A[len-1] gets moved to A[1]
    A[1] gets moved to

    Formula:
    if 2*i < len(A):
        j = 2*i
    else:
        j = ((len(A)-1-i)*2)+1

    Algo:
    sort
    for each index as i:
        move to next position in chain
            if we get back to i, stop

    Wow, I missed so much in this...
    So my assumption that we have to sort was false.
    We can do this in O(n) time, O(n)? space by 'rearranging around the median' not exactly sure
    what that means though.  There's something I'm not getting here.
    Then finally, we realise that we don't even need the median.  If we iterate through the array and
    swap A[i] with A[i+1] when either
    - i is even and A[i] > A[i+1], or
    - i is odd and A[i] < A[i+1]

    """
    # 1,8,2,4,3,6,7,5
    #     |
    # tmp =
    # i = 2
    # pi =
    # ni =
    A.sort()
    b = []
    l, r = 0, len(A) - 1
    while l < r:
        b.append(A[l])
        b.append(A[r])
        l += 1
        r -= 1
    if l == r:
        b.append(A[r])
    for i, val in enumerate(b):
        A[i] = val
    #
    #
    # def get_next_idx(idx):
    #     return 2 * idx if 2 * idx < len(A) else (len(A) - 1 - idx) * 2 + 1
    #
    # for i in range(1, len(A), 2):
    #     prev_idx = i
    #     tmp = A[i]
    #     while (next_idx := get_next_idx(prev_idx)) != i:
    #         # print(prev_idx, next_idx)
    #         tmp, A[next_idx] = A[next_idx], tmp
    #         prev_idx = next_idx
    #     A[i] = tmp


@enable_executor_hook
def rearrange_wrapper(executor, A):
    def check_answer(A):
        for i in range(len(A)):
            if i % 2:
                if A[i] < A[i - 1]:
                    raise TestFailure().with_property(
                        PropertyName.RESULT, A
                    ).with_mismatch_info(
                        i,
                        "A[{}] <= A[{}]".format(i - 1, i),
                        "{} > {}".format(A[i - 1], A[i]),
                    )
                if i + 1 < len(A):
                    if A[i] < A[i + 1]:
                        raise TestFailure().with_property(
                            PropertyName.RESULT, A
                        ).with_mismatch_info(
                            i,
                            "A[{}] >= A[{}]".format(i, i + 1),
                            "{} < {}".format(A[i], A[i + 1]),
                        )
            else:
                if i > 0:
                    if A[i - 1] < A[i]:
                        raise TestFailure().with_property(
                            PropertyName.RESULT, A
                        ).with_mismatch_info(
                            i,
                            "A[{}] >= A[{}]".format(i - 1, i),
                            "{} < {}".format(A[i - 1], A[i]),
                        )
                if i + 1 < len(A):
                    if A[i + 1] < A[i]:
                        raise TestFailure().with_property(
                            PropertyName.RESULT, A
                        ).with_mismatch_info(
                            i,
                            "A[{}] <= A[{}]".format(i, i + 1),
                            "{} > {}".format(A[i], A[i + 1]),
                        )

    executor.run(functools.partial(rearrange, A))
    check_answer(A)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "alternating_array.py", "alternating_array.tsv", rearrange_wrapper
        )
    )

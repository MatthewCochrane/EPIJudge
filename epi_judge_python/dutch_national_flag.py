import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

RED, WHITE, BLUE = range(3)


def dutch_flag_partition(pivot_index: int, A: List[int]) -> None:
    """
    Partition an array into three parts.
    Values < pivot should go on the left.
    Values > pivot should go on the right.
    Values = pivot should go in the middle.

    Example
        [3,6,2,3,5,1,2,5], pivot_idx = 3, pivot = 3
        [2,1,5,3,5,6,3,3]
        [2,1,3,3,3,5,5,6]

    So looks like we can do this in two passes.

    move all the items < pivot to the left
    move all the items > pivot to the right

    moving smaller items to the left

    next_small_idx = 0
    for each index:
        if item < pivot:
            swap item with next_small_idx
            next_small_idx += 1

    Test:
    [3,6,2,3,5,1,2,5], pivot_idx = 3, pivot = 3
    [2,1,2,3,5,6,3,5]

    moving larger items to the right
    next_large_idx = len(A) - 1
    for each idx in reverse:
        if item < pivot:
            # We've hit the section that is already partitioned
            # so we're done.
            break
        elif item > pivot:
            swap item with next_large_idx
            next_large_idx += 1

    O(n) time
    O(1) space
    Two passes
    """

    # [3,6,2,3,5,1,2,5], pivot_idx = 3, pivot = 3
    # [2,1,2,3,3,5,6,5]
    #      |   |
    pivot = A[pivot_index]
    # move all the items < pivot to the left
    next_small_idx = 0
    for i in range(len(A)):
        if A[i] < pivot:
            A[i], A[next_small_idx] = A[next_small_idx], A[i]
            next_small_idx += 1

    # move all the items > pivot to the right
    next_large_idx = len(A) - 1
    for i in reversed(range(len(A))):
        if A[i] < pivot:
            break
        elif A[i] > pivot:
            A[i], A[next_large_idx] = A[next_large_idx], A[i]
            next_large_idx -= 1


def dutch_flag_partition_book(pivot_index: int, A: List[int]) -> None:
    """
    This is the solution from the book.
    I wanted to code it to see how it performed.
    It's a lot simpler than my solution!  And it's faster too.
    I really like the idea.
    roughly

    move all of the smaller items to the start
    move all the larger items to the end
    by definition, the items larger than the pivot are in the middle.
    """
    pivot = A[pivot_index]
    # First pass: group elements smaller than pivot.
    smaller = 0
    for i in range(len(A)):
        if A[i] < pivot:
            A[i], A[smaller] = A[smaller], A[i]
            smaller += 1
    # Second pass: group elements larger than pivot.
    larger = len(A) - 1
    for i in reversed(range(len(A))):
        if A[i] < pivot:
            break
        elif A[i] > pivot:
            A[i], A[larger] = A[larger], A[i]
            larger -= 1


def dutch_flag_partition_mine(pivot_index: int, A: List[int]) -> None:
    """
    Write a program that takes an array A and an index i, and rearranges the elements
    such that all elements less than the pivot (A[i]) appear first, followed by elements
    equal to the pivot, followed by elements greater than the pivot.

    Example:
        [1,2,4,5,2,3,2,3,4], pivot = 2 (val = 4)
        [1,2,2,3,2,3,4,4,5]

    Example: Pivot is smallest
        [2,3,1,2,3], pivot = 2 (val = 1)
        [1,2,3,2,3]

    Example: Pivot is largest
        [2,3,1,2,3], pivot = 1 (val = 3)
        [2,1,2,3,3]

    We could do a sort...  But that's O(n log n) and kind of defeats the purpose.

    We can scan through the array, if we see an item less than the pivot, we put it
    at the front.  If we see an item more than the pivot we put it at the end.
    [1,2,4,5,2,3,2,3,4], pivot = 5 (val = 3)
         lm        r
    How do we move some unknown number of items into the middle when we don't know
    how big the middle is going to be yet?  We could use multiple passes?

    we could do a pass where we count the number of <, == and >.  Then use three pointers
    and do one more pass, when we encounter each value, put it in it's correct position.
    Though then we would need to skip over some items.

    [1,2,4,5,2,3,2,3,4], pivot = 5 (val = 3)

    < count  4
    == count 2
    > count  3

    [1,2,4,5,2,3,2,3,4], pivot = 5 (val = 3)
    [1,2,2,2,3,3,4,5,4], pivot = 5 (val = 3)

    Count the sections
    While less_ptr < equal start and equal_ptr < more_start and more_ptr < length
        Increment all the pointers that are in the right place already.
        If the less than hasn't run out and it's more than, and the more than is less than:
            swap less and more
            increment both
        If the less than hasn't run out and is equal, and the equal is less than:
            swap less and equal
            increment both
        If the equals hasn't run out and is more than, and the more than is equal:
            swap equal and more
            increment both
        Else:
            do a three way swap
            g = max(a,b,c)
            l = max(a,b,c)
            A[<] = l
            A[>] = g
            A[=] = pivot_val
            increment all three

    O(n) time
    O(1) space
    """
    #              s
    # [1,2,2,2,3,3,4,5,4], pivot = 5 (val = 3)
    #          <   =     >
    lt_size, eq_size, gt_size = 0, 0, 0  # 4, 2, 3
    pivot_val = A[pivot_index]
    for v in A:
        if v < pivot_val:
            lt_size += 1
        elif v == pivot_val:
            eq_size += 1
        else:
            gt_size += 1
    lt_ptr = 0
    eq_ptr = lt_size
    gt_start_idx = lt_size + eq_size
    gt_ptr = gt_start_idx
    while True:
        while lt_ptr < lt_size and A[lt_ptr] < pivot_val:
            lt_ptr += 1
        while eq_ptr < gt_start_idx and A[eq_ptr] == pivot_val:
            eq_ptr += 1
        while gt_ptr < len(A) and A[gt_ptr] > pivot_val:
            gt_ptr += 1

        if lt_ptr >= lt_size and eq_ptr >= gt_start_idx and gt_ptr >= len(A):
            break

        if lt_ptr < lt_size and A[lt_ptr] == pivot_val and A[eq_ptr] < pivot_val:
            A[lt_ptr], A[eq_ptr] = A[eq_ptr], A[lt_ptr]
        elif lt_ptr < lt_size and A[lt_ptr] > pivot_val and A[gt_ptr] < pivot_val:
            A[lt_ptr], A[gt_ptr] = A[gt_ptr], A[lt_ptr]
        elif eq_ptr < gt_start_idx and A[eq_ptr] > pivot_val and A[gt_ptr] == pivot_val:
            A[eq_ptr], A[gt_ptr] = A[gt_ptr], A[eq_ptr]
        else:
            smallest = min(A[lt_ptr], A[eq_ptr], A[gt_ptr])
            largest = max(A[lt_ptr], A[eq_ptr], A[gt_ptr])
            A[lt_ptr], A[eq_ptr], A[gt_ptr] = smallest, pivot_val, largest


@enable_executor_hook
def dutch_flag_partition_wrapper(executor, A, pivot_idx):
    count = [0, 0, 0]
    for x in A:
        count[x] += 1
    pivot = A[pivot_idx]

    executor.run(functools.partial(dutch_flag_partition, pivot_idx, A))

    i = 0
    while i < len(A) and A[i] < pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] == pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] > pivot:
        count[A[i]] -= 1
        i += 1

    if i != len(A):
        raise TestFailure("Not partitioned after {}th element".format(i))
    elif any(count):
        raise TestFailure("Some elements are missing from original array")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "dutch_national_flag.py",
            "dutch_national_flag.tsv",
            dutch_flag_partition_wrapper,
        )
    )

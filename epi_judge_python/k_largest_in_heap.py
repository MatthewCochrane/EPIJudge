import heapq
from typing import List

from test_framework import generic_test, test_utils


def k_largest_in_binary_heap(A: List[int], k: int) -> List[int]:
    """
    Start: 13:22 after reading about binary heaps
    Pick the n largest elements from a heap without modifying the heap
    Thing about a max-heap is that the parent is always larger than the children

           9|
        8    6
      1  7  5 2
    0

    0  1  2  3  4  5  6  7
    9, 8, 6, 1, 7, 5, 2, 0
       |     l  r

    idx*2 + 1
    idx*2 + 2

    4 largest
    9, 8, 7, 6

    If we could modify the heap we can extract the k max elements in O(k log n) time
    So we probably can't do better than that.
    We could use another heap of size k to extract the k max in O(n log k) time, O(1) space - not including result
    If we extract the items then put them back that would take O(k log n) to extract and O(k) to put them back
    The heap might be different but it would hold the same information.

    What if we take the root, then if L < R

           9
        8    6
      1  7  5 2
    0

    A... k=4
    len(A) = 8
    0  1  2  3  4  5  6  7
    9, 8, 6, 1, 7, 5, 2, 0
       |     l  r

    result = [9, 8, 7, 6]
    heap = [(-5, 5), (-2, 6), (-1, 3)]
    p = 2
    np = 2*2+1 = 5 and 6


    if len(A) < k:
        return [*A]
    heap = [(-A[0], 0)]
    result = []
    while len(result) < k:
        max_el, ptr = extract max from heap
        push -max_el to result
        if (new_ptr := ptr*2 + 1) < len(A):
            # left child
            push (-A[new_ptr], new_ptr) to heap
        if (new_ptr := ptr*2 + 2) < len(A):
            # right child
            push (-A[new_ptr], new_ptr) to heap
    return result


    heap size = 1,2,3,4,...,k
    O(k) space
    time complexity is O(log k) per step so overall time complexity ends up as O(k log k)

    All tests pass
    Time: 13:58
    36 mins.  That's great.  Good problem solving.  You do need to know how heaps work internally!
    That's actually really insane that you worked that out!  You need to trust yourself!  And get more practise in
    interview-like environments!
    """
    if len(A) < k:
        return [*A]
    # This is a max-heap so store negated values
    heap = [(-A[0], 0)]
    result = []
    while len(result) < k:
        max_el, ptr = heapq.heappop(heap)
        result.append(-max_el)
        if (new_ptr := ptr * 2 + 1) < len(A):
            # left child
            heapq.heappush(heap, (-A[new_ptr], new_ptr))
        if (new_ptr := ptr * 2 + 2) < len(A):
            # right child
            heapq.heappush(heap, (-A[new_ptr], new_ptr))
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "k_largest_in_heap.py",
            "k_largest_in_heap.tsv",
            k_largest_in_binary_heap,
            comparator=test_utils.unordered_compare,
        )
    )

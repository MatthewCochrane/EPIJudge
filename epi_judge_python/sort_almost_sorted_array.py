import heapq
from itertools import islice
from typing import Iterator, List

from test_framework import generic_test


def sort_approximately_sorted_array(sequence: Iterator[int], k: int) -> List[int]:
    """
    The k last items go into a heap, pop the lowest item off and insert it, then push the new item.
    heap stays at size k

    eg.

    1,2,3,5,4,6,7,9,8,10,11
    1,2,3,4,5,6,7,8,9,h h

    init heap
    for i in k:
        take from seq
        if was None:
            break
        add to heap
    while (val := next(it, None)) is not None:
        add to heap
        pop item off heap and add to result
    while heap:
        pop item off heap
        add to result
    return result

    O(k log n) time
    O(k) space

    Standard k-way heap sorting question

    Finished at 22:19 about 25 mins.
    """
    result = []
    heap = []
    # Slightly nicer than the code below...
    # islice won't overrun
    for val in islice(sequence, k):
        heapq.heappush(heap, val)

    # for i in range(k):
    #     val = next(sequence, None)
    #     if val is None:
    #         break
    #     heapq.heappush(heap, val)
    # while (val := next(sequence, None)) is not None:
    # this is a better way to do it...  Won't break if the sequence is exhausted.
    for val in sequence:
        result.append(heapq.heappushpop(heap, val))
    while heap:
        result.append(heapq.heappop(heap))
    return result


def sort_approximately_sorted_array_wrapper(sequence, k):
    return sort_approximately_sorted_array(iter(sequence), k)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sort_almost_sorted_array.py",
            "sort_almost_sorted_array.tsv",
            sort_approximately_sorted_array_wrapper,
        )
    )

import heapq
from typing import List

from test_framework import generic_test


def merge_sorted_arrays(sorted_arrays: List[List[int]]) -> List[int]:
    """
    Start: 19:27
    Merge a set of lists together.
    We have a lot of data...
    Generally, if we want to merge two sorted lists together, we can do so in O(n) time with O(1) space
    We can do the same thing with many sorted arrays, the difference is that we have a set of many options to chose from.

    1,5,7
        |
    4,5,9,10
          |
    0,4,6,8
          |
    []
    0,1,4,4,5,6,7,8,9,10

    When merging two lists we only needed to do one comparison.
    So time complexity was O(n*1)
    When we have multiple lists ie > 2 we need to find the smallest
    sort, pick min... this is O(l log l) where l is number of lists
    Overall time complexity would be O(n*l log l)
    [1,2,3] -> find the minimum then add a new item into it.
    This could be a heap.
    All we need to do is keep pulling out the minimum.
    O(n*log l)

    Pseudo code
    heap = []
    for each list:
        push item to heap((first item in list, list index, 1))
    while heap has data:
        data, list_idx, next_data_idx = heapq.heappop(heap)
        result.append(data)
        if next_data_idx < length of that list:
            heapq.heappush((next item from that list, list_idx, next_data_idx + 1))
    return sorted list

    Finished: 20:01
    Took 30 mins

    """
    heap = []
    result = []
    for i, ary in enumerate(sorted_arrays):
        heapq.heappush(heap, (ary[0], i, 1))
    while heap:
        data, ary_idx, next_data_idx = heapq.heappop(heap)
        result.append(data)
        if next_data_idx < len(sorted_arrays[ary_idx]):
            heapq.heappush(
                heap,
                (sorted_arrays[ary_idx][next_data_idx], ary_idx, next_data_idx + 1),
            )
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sorted_arrays_merge.py", "sorted_arrays_merge.tsv", merge_sorted_arrays
        )
    )

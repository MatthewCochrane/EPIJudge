from typing import List

from test_framework import generic_test
import bisect


def search_first_of_k(A: List[int], k: int) -> int:
    """
    Start: 14:47
    I still had a bug in my first implementation.  I just checked if A[i] == k and didn't think
    what happens if i >= len(A)....
    Finish: 14:50
    Ok, what about implementing this without bisect?
    Start 14:52

    binary search

    find the first index

    # right starts after end
    l, r = 0, len(A)
    mid = (l + r) // 2
    while l != r:
        if A[mid] < k:
            # discard all left vals
            l = mid + 1
        elif A[mid] >= k:
            # discard all right vals
            r = mid
    if l < len(A) and A[l] == k:
        return l
    return -1

    Also works
    Time: 15:04 - took 12 mins.  it felt slow though haha..
    """
    # 'cheaty' answer
    # i = bisect.bisect_left(A, k)
    # return i if i < len(A) and A[i] == k else -1

    # right starts after end
    l, r = 0, len(A)
    while l != r:
        mid = (l + r) // 2
        if A[mid] < k:
            # discard that val and all left vals
            l = mid + 1
        elif A[mid] >= k:
            # discard all right vals
            r = mid
    if l < len(A) and A[l] == k:
        return l
    return -1



if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "search_first_key.py", "search_first_key.tsv", search_first_of_k
        )
    )

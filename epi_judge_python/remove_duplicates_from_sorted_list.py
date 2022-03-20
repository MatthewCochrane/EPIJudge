from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def remove_duplicates(L: ListNode) -> Optional[ListNode]:
    """
    Start: 7:07
    We have a list which is sorted.  Remove any duplicates.

    Example:
        input 2->2->3->4->6->6->6
        result 2->3->4->6

        input 1
        result 1

        input 1->1->1
        result 1

    Approach
        if not L:
            return L
        prev, current = L, L.next
        while current:
            if next value is same as previous,
                previous.next, current = current.next, current.next
            else:
                previous, current = current, current.next
        return L

    Time complexity is O(n)
    Space complexity is O(1)

    Time: 7:23
    16 mins and still felt a bit slow.  Very easy question though.
    """
    # 2-3-5-7-11
    #          p c
    if not L:
        return L
    previous, current = L, L.next
    while current:
        if previous.data == current.data:
            previous.next, current = current.next, current.next
        else:
            previous, current = current, current.next
    return L


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "remove_duplicates_from_sorted_list.py",
            "remove_duplicates_from_sorted_list.tsv",
            remove_duplicates,
        )
    )

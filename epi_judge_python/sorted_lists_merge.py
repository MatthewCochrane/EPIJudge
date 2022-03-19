from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def merge_two_sorted_lists(
    L1: Optional[ListNode], L2: Optional[ListNode]
) -> Optional[ListNode]:
    """
    Start: 9:56
    Merge two sorted linked lists

    Example:
        2,5,7
        3,11
        2,3,5,7,11

    2->5->7
    3->11

    Start with dummy/sentinel

    dummy->
    pick min of L1 (2) and L2 (3)
    dummy->2
    Used L1 so move L1 forward
    L1 = 5->7
    L2 = 3->11
    pick min of L1 and L2
    dummy->2->3
    L1 = 5->7
    L2 = 11
    pick min of L1 and L2
    dummy->2->3->5
    L1 = 7
    L2 = 11
    pick min of L1 and L2
    dummy->2->3->5->7
    L1 = None
    L2 = 11
    When one of the lists is empty, just connect to the head of the other list
    dummy->2->3->5->7->11
    Even if it was 11->12 this would take only one operation.
    return dummy.next

    Edge cases:
        0 length of one list
        0 length of both lists
        all of one list comes before the other?

    Tests of Pseudo code
    None
    None
    d->

    11
    d->2->5->7->11
    return 2->5->...

    Pseudo code
    create dummy node
    head = dummy
    while L1 and L2 both have nodes:
        update head to point to min of L1/L2, then move that list forward one node
    update head to point to the list with remaining nodes
    return head.next

    O(n+m) time
    O(1) space
    Time: 10:15 -> 20 mins
    1 bug, forgot to move head in the loop

    Notes:
    What I'm calling head in my code, every body else calls 'tail'.  That's definitely worth fixing up.
    So head is where we start, and tail is the end, that we add to, that points to None.
    I updated my code below
    """
    dummy = ListNode()
    tail = dummy
    while L1 and L2:
        if L1.data < L2.data:
            tail.next = L1
            L1 = L1.next
        else:
            tail.next = L2
            L2 = L2.next
        tail = tail.next
    if L1:
        tail.next = L1
    elif L2:
        tail.next = L2
    return dummy.next


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sorted_lists_merge.py", "sorted_lists_merge.tsv", merge_two_sorted_lists
        )
    )

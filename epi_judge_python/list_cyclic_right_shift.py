from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def cyclically_right_shift_list(L: ListNode, k: int) -> Optional[ListNode]:
    """
    Start: 7:26
    Perform a cyclic right shift on a linked list

    Examples:
        input: 1->2->3->4->5->6, k=1
        result: 6->1->2->3->4->5

        input: 1->2->3->4->5->6, k=3
        result: 4->5->6->1->2->3

        input: 1->2->3->4->5->6, k=9
        result: 4->5->6->1->2->3 *shift by mod(len)

        input: 1->2, k=1
        result: 2->1

    Approach
        Find the length of the list
        modulo k by the length
        if k == 0 return L
        Find the k+1th last item and point it to None
        point the last item to the start

    O(n) time
    O(1) space
    All tests pass
    Finished 7:48
    22 mins
    """
    if L is None:
        return L
    # Find length and last node
    node, length = L, 1
    while node.next:
        node, length = node.next, length + 1
    last_node = node

    k %= length
    if k == 0:
        return L
    node = L
    for _ in range(length - k - 1):
        node = node.next

    # Rearrange the linked list
    new_start = node.next
    node.next = None
    last_node.next = L
    return new_start


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "list_cyclic_right_shift.py",
            "list_cyclic_right_shift.tsv",
            cyclically_right_shift_list,
        )
    )

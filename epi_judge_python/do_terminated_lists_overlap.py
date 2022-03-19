import functools
from typing import Optional, Tuple

from list_node import ListNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def overlapping_no_cycle_lists(
    l0: Optional[ListNode], l1: Optional[ListNode]
) -> Optional[ListNode]:
    """
    Start: 14:52
    Determine if there is a common node between the two lists.
    The lists do not have cycles.

    L0 1->2->3->4
    L1    2-/

    L0 1->2->3->4
    L1 1->2-/

    There could be many common nodes.  If we traverse to the end of both lists and the last node is the same
    then there must be common nodes.  This isn't necessarily the *first* common node though and the question
    does not ask us to determine that.

    What would you like to return?  What should we return if there's no common node?

    Possibilities:
        use a dict - O(n+m) time, O(n) space
        iterate one list multiple times - O(n*m) time, O(1) space
        step in sync after finding diff - O(n+m) time, O(1) space

    Pseudo code
    traverse l0 to the last non-None node (also count length)
    traverse l1 to the last non-None node (also count length)
    if l0 is not l1 return None
    find difference in lengths
    reinitialise pointers to start of list
    step longer list forward the size of the diff
    step each node forward together, when you find a match return it, that's the first common node
    len0 = 4
    len1 = 3
                |
    L0 1->2->3->4
    L1    2-/
    """

    def get_last_and_len(head: ListNode) -> Tuple[Optional[ListNode], int]:
        list_len = 1
        while head and head.next:
            head = head.next
            list_len += 1
        return head, list_len

    if l0 is None or l1 is None:
        return None

    l0_last, l0_len = get_last_and_len(l0)
    l1_last, l1_len = get_last_and_len(l1)
    if l0_last is not l1_last:
        return None
    len_diff = abs(l0_len - l1_len)
    short_list, long_list = (l0, l1) if l0_len < l1_len else (l1, l0)
    for _ in range(len_diff):
        long_list = long_list.next
    while short_list is not long_list:
        short_list, long_list = short_list.next, long_list.next
    return short_list


@enable_executor_hook
def overlapping_no_cycle_lists_wrapper(executor, l0, l1, common):
    if common:
        if l0:
            i = l0
            while i.next:
                i = i.next
            i.next = common
        else:
            l0 = common

        if l1:
            i = l1
            while i.next:
                i = i.next
            i.next = common
        else:
            l1 = common

    result = executor.run(functools.partial(overlapping_no_cycle_lists, l0, l1))

    if result != common:
        raise TestFailure("Invalid result")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "do_terminated_lists_overlap.py",
            "do_terminated_lists_overlap.tsv",
            overlapping_no_cycle_lists_wrapper,
        )
    )

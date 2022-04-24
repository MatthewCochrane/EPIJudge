from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def stable_sort_list(L: ListNode) -> Optional[ListNode]:
    """
    Could use merge sort.  It's stable and O(n log n) on arrays.
    We'd need to iterate to find the end of the list.

    def merge_sort_list(ll, ll_len):
        if ll_len <= 1:
            return
        l1 = ll
        l2 = walk ll forward ll_len // 2 steps
        break the tail to l2
        head1 = merge_sort_list(ll, ll_len // 2)
        head2 = merge_sort_list(ll_updated, ll_len - ll_len // 2)
        new_head = merge_lists(head1, head2)
        return new_head # tail will not be connected to anything after this.


    3->5->2  6->9->2->5
    1        2
    len = 7
    3  5->2
    1  2
    len = 7

    5  2
    1  2
    len=2

    2->5
    3
    2->3->5
    2->5->6->9
    2->2->3->5->6->9

    def merge_sort_list(ll, ll_len):
        if ll_len <= 1:
            return
        l1 = ll
        l2 = walk ll forward ll_len // 2 - 1 steps
        break the tail of l2 and step forward one
        head1 = merge_sort_list(l1, ll_len // 2)
        head2 = merge_sort_list(l2, ll_len - ll_len // 2)
        new_head = merge_lists(head1, head2)
        return new_head # tail will not be connected to anything after this.


    Nice one!  had one little bug in there and worked it out reasonably quickly.
    """

    def merge_lists(l1: ListNode, l2: ListNode) -> ListNode:
        """
        1->2->3
              a
        1->2
              b
        d->1->1->2->2
                    h

        while a and b:
            if a <= b:
                head.next = a
                a = a.next
            else:
                head.next = b
                b = b.next
            head = head.next
        if a:
            head.next = a
        elif b:
            head.next = b


        """
        head = dummy = ListNode()
        while l1 and l2:
            if l1.data <= l2.data:
                head.next = l1
                l1 = l1.next
            else:
                head.next = l2
                l2 = l2.next
            head = head.next
        if l1:
            head.next = l1
        elif l2:
            head.next = l2
        return dummy.next

    def merge_sort_ll(ll: ListNode, ll_len: int) -> ListNode:
        if ll_len == 1:
            return ll
        l1 = ll
        l2 = l1
        for _ in range((ll_len // 2) - 1):
            l2 = l2.next
        # Had a bug here, was doing something else like l2, l2.next = l2.next, None here which didn't work...
        t = l2.next
        l2.next = None
        l2 = t
        head1 = merge_sort_ll(l1, ll_len // 2)
        head2 = merge_sort_ll(l2, ll_len - (ll_len // 2))
        new_head = merge_lists(head1, head2)
        return new_head

    if not L:
        return None
    list_len = 1
    t = L
    while t.next:
        t = t.next
        list_len += 1
    return merge_sort_ll(L, list_len)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sort_list.py", "sort_list.tsv", stable_sort_list
        )
    )

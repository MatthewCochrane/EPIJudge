from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def even_odd_merge(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Start: 15:05
    Compute the even-odd merge of the list starting with head.

    Example:
        Input:  0->1->2->3->4->5->None
        Output: 0->2->4->1->3->5->None

        Input:  0->1->2->3->4->None
        Output: 0->2->4->1->3->None

        Input:  None
        Output: None


    Worked Example:
        Input: 0->1->2->3->4->None
               p  c                  store c!
               0  1->2->3->4->None
               \---->/
                  /---->\
                  p  c
               0  1  2->3->4->None
               \---->/
                  /---->\
                     p  c
               0  1  2  3->4->None
               \---->|---->/
                  /---->\
                        p  c
                        /---->\
               0  1  2  3  4  None
               \---->|---->/
                  \<-------/

        Length 1
               0->1->2->3->None
               p  c                  store c!
               0  1->2->3->None
               \---->/
                  p  c
                  /---->\
               0  1  2->3->None
               \---->/
                     p  c
                  /---->\
               0  1  2  3->None
               \---->/
                  \<-/


        # Return as is for 0 length lists
        if not head or not head.next:
            return head
        p, c = head, head.next
        first_odd = c
        while c.next:
            p.next = c.next
            step p and c forward
        if p is odd:
            p.next = None
            c.next = first_odd
        else:
            p.next = first_odd

        Two cases when c.next is None:
        if c is even:
            p.next = c.next
        c.next = first_odd

        if p is odd:
            p.next = None
        c.next = first_odd

        while c.next
            ...
        if p is even

        Two options
        1. use extra pointer.  Requires dummy node and extra pointer
        2. stop when c.next is None.  Requires extra check for length 1 list


        O(n) time, O(1) space
    Time: 15:43
    This was too slow.  I got tricked up.  It's not that hard just tricky.
    """
    # Return as is for 0 length lists
    if not head or not head.next:
        return head
    p, c = head, head.next
    first_odd = c
    p_is_odd = False
    while c.next:
        p.next = c.next
        p, c = c, c.next
        p_is_odd ^= 1
    if p_is_odd:
        p.next = None
        c.next = first_odd
    else:
        p.next = first_odd
    return head


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "even_odd_list_merge.py", "even_odd_list_merge.tsv", even_odd_merge
        )
    )

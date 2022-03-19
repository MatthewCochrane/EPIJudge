from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def reverse_sublist(L: ListNode, start: int, finish: int) -> Optional[ListNode]:
    """
    Reverse the items in the linked list from start to finish inclusive

    1->2->3->4->5  start=2, finish=4
    1->4->3->2->5

          /---->\
       /---->\
          /<-\
    1->2  3  4  5  start=2, finish=4
       h  i     t

    traverse to start
    1->2->3->4->5  start=2, finish=4
       |
    store start node so we can point it to 5 later
    move to 3
    point 3 to 2
    1->2<->3 4->5  start=2, finish=4
    * can't move to 4 if we already pointed 3 to 2
    move to 4, point 4 to 3
    1->2<->3<-4 5  start=2, finish=4
    4 is end...
    point 1->4
    point 2->5
      /-------\
    1 2<-3<-4 5  start=2, finish=4
    \-------/
    1->4->3->2->5

    traverse to start
    save the previous node
    next = current.next
    save the first node (current)
    previous, current, next = current, next, next.next
    while current index <= finish:
        point current to prev
        previous, current, next = current, next, next.next
    point saved prev node to previous
    point first node to current

    O(finish) time
    O(1) space

    Brutal.  So many edge cases...
    I should definitely repeat this question!
    They did this in 11 lines while it took me 22... Hmm

    Their approach:
    Create a dummy head and point at L
    find sublist head by stepping a pointer forward exactly 'start'-1 times
    start with the node after the sublist head found above
    make exactly finish-start steps:
        store the next node
        node.next =


    Ok, so another way to reverse a linked list is to keep pointing the start back one and updating what that points
    to

    eg.

    0->1->2->3->4->5

    /---->\
    0  1<-2  3->4->5
       \---->/

    /------->\
    0  1<-2<-3  4->5
       \------->/

    /---------->\
    0  1<-2<-3<-4  5
       \---------->/

    /------------->\
    0  1<-2<-3<-4<-5
       \------------->/


    """
    # Their solution
    # dummy_head = sublist_head = ListNode(next=L)
    # for _ in range(1, start):
    #     sublist_head = sublist_head.next
    #
    # sublist_iter = sublist_head.next
    # for _ in range(finish - start):
    #     temp = sublist_iter.next
    #     sublist_iter.next, temp.next, sublist_head.next = (
    #         temp.next,
    #         sublist_head.next,
    #         temp,
    #     )
    # return dummy_head.next

    if start <= 0 or finish <= 0 or L is None or start == finish:
        return L
    dummy = ListNode(next=L)
    pre, cur = dummy, L
    cur_idx = 1
    while cur_idx < start and cur:
        pre, cur = cur, cur.next
        cur_idx += 1
    if cur_idx != start:
        raise IndexError()
    node_before_start = pre
    first_node = cur
    # Can have an error here if cur.next is None
    # print(cur_idx, pre, cur.data, cur.next.data)
    pre, cur, nxt = cur, cur.next, cur.next.next
    cur_idx += 1
    while cur_idx <= finish:
        cur.next = pre
        pre, cur, nxt = cur, nxt, (nxt.next if nxt else None)
        cur_idx += 1
    node_before_start.next = pre
    first_node.next = cur
    return dummy.next


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "reverse_sublist.py", "reverse_sublist.tsv", reverse_sublist
        )
    )

from typing import Optional

from list_node import ListNode
from test_framework import generic_test


# Assumes L has at least k nodes, deletes the k-th last node in L.
def remove_kth_last(L: ListNode, k: int) -> Optional[ListNode]:
    """
    Start: 17:16
    Delete the kth last node without storing the length of the list.

    If we could store the length we'd just count the length, then subtract k, then traverse that far from the start
    then delete that node.

    z->a->b->c->d->e->f->g->h    k=2 -ie we want to delete g
                      b        f

    what if we walk forward k nodes
    then step the two pointers forward in lock-step until one goes off the end of the list and then we delete the
    node at the first pointer

    d->a->b
    |        |

    Use a dummy node at the start!

    Pseudo code
    create dummy node and point it to L
    initialise two pointers (back, front) at dummy and at L
    move front forward k times -> there are at least k nodes so this can't break
    while front is not None:
        move front and back forward
    delete the node after back (back.next = back.next.next)

    O(n) time, O(1) space, doesn't store the length of the list.
    Finished: 17:27 -> 11 mins nice
    """
    dummy = ListNode(next=L)
    back, front = dummy, L
    for _ in range(k):
        front = front.next
    while front is not None:
        back, front = back.next, front.next
    back.next = back.next.next
    return dummy.next



if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('delete_kth_last_from_list.py',
                                       'delete_kth_last_from_list.tsv',
                                       remove_kth_last))

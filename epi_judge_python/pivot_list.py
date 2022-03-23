import functools
from typing import Optional

from list_node import ListNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def list_pivoting(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    Start: 17:33
    Pivot about the value k
    Example
        1,2,6,4,2,2,3,4,5,3, k=3
        1,2,2,2,3,3,6,4,4,5

    How I did this in my head:
        three passes
        pass 1 -> find elements < k
        pass 2 -> find elements == k
        pass 3 -> find elements > k

    We could do this all in one pass with three separate lists
        o-> k=3
        l->1->2->2->2
        e->3->3
        g->6->4->4->5

        join l->e->g

    Pseudo code
    orig_dummy point at head
    less_dummy point at None, less_tail
    eq_dummy point at None, eq_tail
    more_dummy point at None, more_tail
    while orig_dummy.next:
        cur = orig_dummy.next
        if cur data < pivot:
            point less_tail at cur
            set less_tail to cur
        elif cur data is pivot:
            point eq_tail to cur
            set eq_tail to cur
        else:
            point more_tail to cur
            set more_tail to cur
    result_dummy = less_dummy
    less_tail.next = eq_dummy.next
    eq_tail.next = more_dummy.next

    d->
    d->e
    d->g->g->g

    Join three linked lists that may be empty
    head, tail = None, None
    for (pd, pt) in [(ld, lt), (ed, et), (md, mt)]:
        if pd.next is None:
            continue
        if head is None:
            head = pd.next
        else:
            tail.next = pd.next
        tail = pt
    tail.next = None
    return head

    Time: O(n)
    Space: O(1)

    Finished: 18:12
    About 45 mins.  Too slow really.  Decent but could be better.
    Had two very small bugs.
    """
    cur = head
    less_dummy = less_tail = ListNode()
    eq_dummy = eq_tail = ListNode()
    more_dummy = more_tail = ListNode()
    while cur:
        if cur.data < k:
            less_tail.next = cur
            less_tail = cur
        elif cur.data == k:
            eq_tail.next = cur
            eq_tail = cur
        else:
            more_tail.next = cur
            more_tail = cur
        cur = cur.next

    # This is a nicer way to do what I had written below
    # the key is building the lists up in reverse.
    # This removes a bunch of the edge cases around what
    # to do if one of the lists is empty.
    # Very useful to remember
    more_tail.next = None
    eq_tail.next = more_dummy.next
    less_tail.next = eq_dummy.next
    return less_dummy.next

    # head, tail = None, None
    # for (pd, pt) in [
    #     (less_dummy, less_tail),
    #     (eq_dummy, eq_tail),
    #     (more_dummy, more_tail),
    # ]:
    #     if pd.next is None:
    #         continue
    #     if head is None:
    #         head = pd.next
    #     else:
    #         tail.next = pd.next
    #     tail = pt
    # if tail:
    #     tail.next = None
    # return head


def linked_to_list(l):
    v = list()
    while l is not None:
        v.append(l.data)
        l = l.next
    return v


@enable_executor_hook
def list_pivoting_wrapper(executor, l, x):
    original = linked_to_list(l)

    l = executor.run(functools.partial(list_pivoting, l, x))

    pivoted = linked_to_list(l)
    mode = -1
    for i in pivoted:
        if mode == -1:
            if i == x:
                mode = 0
            elif i > x:
                mode = 1
        elif mode == 0:
            if i < x:
                raise TestFailure("List is not pivoted")
            elif i > x:
                mode = 1
        else:
            if i <= x:
                raise TestFailure("List is not pivoted")

    if sorted(original) != sorted(pivoted):
        raise TestFailure("Result list contains different values")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "pivot_list.py", "pivot_list.tsv", list_pivoting_wrapper
        )
    )

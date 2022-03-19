import functools
from typing import Optional

from list_node import ListNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def has_cycle(head: ListNode) -> Optional[ListNode]:
    """
    Start: 13:44
    If there is a cycle in the list, return the node that's the start of the cycle, otherwise return None.

    Example:
        1->2->3
        \<----/
        Returns the node 1

        1->2
        Returns None

        1->2->3
           \<-/
        Returns the node 2

    Should be able to use floyd's cycle finding algorithm which uses a slow and a fast pointer.

    /<----\
    3->1->2
       fs

          /<-------\
    1->2->3->4->5->6
                fs

    lc = 4

    do a loop -> count length of cycle
    count steps to repeat from start

    Can find length of cycle
    can find distance to a point in the cycle but we don't know which point

    len to start = ls
    cycle len = lc

    4 -> 4, 4+c, 4+kc

    To find the start
    create a 'stick' starting at the first node that's the length of a cycle
    check if both ends are the same value, if so, the common node is the start
    otherwise, increment both ends forward

    Pseudo code
    init two pointers at the head
    while fast is not None and fast is not equal to slow:
        move fast forward 2
        move slow forward 1
    if fast is None:
        there is no cycle
    count the length of the cycle by storing the current node then looping until we get back to it
    To find the start
    create a 'stick' starting at the first node that's the length of a cycle
    while the start node does not equal the end node:
        increment both ends forward
    the common start/end node is the start of the cycle

    O(n) time
    O(1) space

    Test
    cycle_len = 2
              s f
        1->2->3

    Finish: 14:35
    Should probably do this one again too though I feel I did pretty well.

    One note: I had to use id(node) to compare nodes otherwise it was using it's
    overridden equals method which actually traversed the whole list!
    In their program they use the is operator as in 'slow is fast'.

    I think my code is a bit tidier.  Not sure why they choose to stay in the loop forever.
    """
    slow, fast = head, head.next
    while fast is not None and id(fast) != id(slow):
        slow = slow.next
        # move fast as far forward as we can
        # as soon as fast is None, we've found the end so there is no cycle
        # this would always happen before slow so we don't need to check slow
        fast = (fast.next.next if fast.next else fast.next)
    if fast is None:
        return None
    # cycle_len is number of steps to get back to start
    # a cycle length of 1 is a 'self-cycle'
    cycle_len = 1
    slow = slow.next
    while id(slow) != id(fast):
        slow = slow.next
        cycle_len += 1
    slow = fast = head
    # roll out the stick so it's got a length of cycle_len
    for _ in range(cycle_len):
        fast = fast.next
    # keep moving the stick forward by one until we find the start
    # of the cycle where both ends of the stick will meet.
    while id(slow) != id(fast):
        slow, fast = slow.next, fast.next
    return slow



@enable_executor_hook
def has_cycle_wrapper(executor, head, cycle_idx):
    cycle_length = 0
    if cycle_idx != -1:
        if head is None:
            raise RuntimeError("Can't cycle empty list")
        cycle_start = None
        cursor = head
        while cursor.next is not None:
            if cursor.data == cycle_idx:
                cycle_start = cursor
            cursor = cursor.next
            cycle_length += 1 if cycle_start is not None else 0

        if cursor.data == cycle_idx:
            cycle_start = cursor
        if cycle_start is None:
            raise RuntimeError("Can't find a cycle start")
        cursor.next = cycle_start
        cycle_length += 1

    result = executor.run(functools.partial(has_cycle, head))

    if cycle_idx == -1:
        if result is not None:
            raise TestFailure("Found a non-existing cycle")
    else:
        if result is None:
            raise TestFailure("Existing cycle was not found")
        cursor = result
        while True:
            cursor = cursor.next
            cycle_length -= 1
            if cursor is None or cycle_length < 0:
                raise TestFailure(
                    "Returned node does not belong to the cycle or is not the closest node to the head"
                )
            if cursor is result:
                break

    if cycle_length != 0:
        raise TestFailure(
            "Returned node does not belong to the cycle or is not the closest node to the head"
        )


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_list_cyclic.py", "is_list_cyclic.tsv", has_cycle_wrapper
        )
    )

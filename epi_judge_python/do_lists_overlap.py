import functools
from typing import Optional

import do_terminated_lists_overlap
import is_list_cyclic
from list_node import ListNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def overlapping_lists(
    l0: Optional[ListNode], l1: Optional[ListNode]
) -> Optional[ListNode]:
    """
    Start: 16:30

    There are quite a few cases, at least 5 distinct cases which I drew elsewhere.

    If A does not join into B and B does not join into A, the result is None

    If they do not join, they could still have cycles.

    Notes
        if one has a cycle and the other doesn't, then they don't join
        if they both don't have a cycle, then if the end node is the same, they join, otherwise they don't
        if they both have a cycle, we can find the starting node of one of the cycles, and iterate through the other list to find it.

    determine if they have cycles
    if one has a cycle and the other doesn't return None
    if neither has a cycle, use the approach from the last question
    find the start of one of the cycles, traverse the second list until you find that node, that's the node
    when doing so, reuse the last node you found in the second list as a starting point when searching from the
    second list.  If you hit that node again without finding the start of the other cycle, there is no overlap,
    if you do find it, that's one of the answers.

    Time: 17:03
    Cool, so this one I kinda cheated on.  I just worked out all the cases then reused existing solutions.
    Made use of two previous solutions in this one.
    It's O(n+m) time and O(1) space

    In their solution they reuse both of those solutions too...
    """
    if not l0 or not l1:
        return None

    l0_cycle = is_list_cyclic.has_cycle(l0)
    l1_cycle = is_list_cyclic.has_cycle(l1)
    if bool(l0_cycle) ^ bool(l1_cycle):
        return None
    elif not l0_cycle and not l1_cycle:
        return do_terminated_lists_overlap.overlapping_no_cycle_lists(l0, l1)
    # traverse l1 from l1_cycle until we hit l0_cycle of l1_cycle again
    node = l1_cycle.next
    while node is not l0_cycle and node is not l1_cycle:
        node = node.next
    return l0_cycle if node is l0_cycle else None


@enable_executor_hook
def overlapping_lists_wrapper(executor, l0, l1, common, cycle0, cycle1):
    if common:
        if not l0:
            l0 = common
        else:
            it = l0
            while it.next:
                it = it.next
            it.next = common

        if not l1:
            l1 = common
        else:
            it = l1
            while it.next:
                it = it.next
            it.next = common

    if cycle0 != -1 and l0:
        last = l0
        while last.next:
            last = last.next
        it = l0
        for _ in range(cycle0):
            if not it:
                raise RuntimeError("Invalid input data")
            it = it.next
        last.next = it

    if cycle1 != -1 and l1:
        last = l1
        while last.next:
            last = last.next
        it = l1
        for _ in range(cycle1):
            if not it:
                raise RuntimeError("Invalid input data")
            it = it.next
        last.next = it

    common_nodes = set()
    it = common
    while it and id(it) not in common_nodes:
        common_nodes.add(id(it))
        it = it.next

    result = executor.run(functools.partial(overlapping_lists, l0, l1))

    if not (id(result) in common_nodes or (not common_nodes and not result)):
        raise TestFailure("Invalid result")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "do_lists_overlap.py", "do_lists_overlap.tsv", overlapping_lists_wrapper
        )
    )

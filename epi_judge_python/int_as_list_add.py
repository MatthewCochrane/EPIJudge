from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def add_two_numbers(
    L1: Optional[ListNode], L2: Optional[ListNode]
) -> Optional[ListNode]:
    """
    Start: 9:53
    Add the integers represented by the two linked lists.
    The first node in each LL represents the least significant digit.
    Can we have a negative number?? Assume no.

    Example:
        3->1->4  +  9->0->7

        1 1
         413
        +709
        1122

        Answer = 2->2->1->1

    Example:
        0->1 + None

        Answer = 0->1

        If one of the lists is None, return the other list.  Or should this be an error?
        If both of the lists are None, probably return 0?  Not sure what to do for this

    Example:
        1 + 1
        Answer = 2

    Example:
        0->1 + 2 (10 + 2 = 12)
        Answer = 2->1

    Test:
        L1 =
        L2 =
        res = d->0
        carry = 0
        val = 0 + 0 + 0
        return 0

    Test:
        L1 =
        L2 =
        res = d->2->2->1->1
        carry = 0
        3+9+0 = 12
        carry = 12 // 10 = 1
        1+0+1 = 2
        carry = 2//10 = 0
        4+7+0 = 11
        carry = 1
        0+0+1 = 1
        carry = 0
        return 2->2->1->1

    Algorithm:
        Would you like me to reuse bits or always return new nodes.  I feel new nodes is more useful.

        Checks upfront (eg. none)
        result_dummy = Node()
        result_tail = result_dummy
        carry = 0
        while either list still has data (tail not None) or carry is 1:
            add the two node values and the carry or zero if any value is missing
            create a new node with the new value mod 10 and connect it to result_tail
            update result_tail
            carry = value // 10
            step both lists forward (if not none)
        return result_dummy.next

    O(n) time
    O(1) space not including the result list
    Finish: 10:27
    Felt like I was distracted/daydreaming a bit.  Need to focus more.

    Had one small bug, forgot to do the mod 10 on the result.  Easy fix.

    """
    if L1 is None and L2 is None:
        return ListNode(0)
    elif L1 is None:
        return L2  # should make a copy
    elif L2 is None:
        return L1  # should make a copy

    result_dummy = result_tail = ListNode()
    carry = 0
    while L1 or L2 or carry:
        val = (L1.data if L1 else 0) + (L2.data if L2 else 0) + carry
        result_tail.next = ListNode(val % 10)
        result_tail = result_tail.next
        carry = val // 10
        L1 = L1.next if L1 else None
        L2 = L2.next if L2 else None
    return result_dummy.next


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "int_as_list_add.py", "int_as_list_add.tsv", add_two_numbers
        )
    )

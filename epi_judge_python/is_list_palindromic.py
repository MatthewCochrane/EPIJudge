from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def is_linked_list_a_palindrome(head: Optional[ListNode]) -> bool:
    """
    Start: 16:02

    Example:
        Input: a->b->a->None
        Result: True

        Input: a->b->c->None
        Result: False

    Ok, this is more tricky with a linked list than it is with an array.
    With an array we can just iterate two pointers, one from left to right
    and the other from right to left.
    With a linked list we cannot iterate backward.

    It's fairly easy to see how to do this in O(n) space, O(n) time.
    Convert it to a List (array) and then use the traditional approach.
    It's also fairly easy to see how to do this in O(1) space, O(n^2) time.
    For each item, iterate out to it's counterpart at the end of the list and check.

    But how can we do this in O(n) time and O(1) space?
    If we can modify the list, then we could do something like...
    1. reverse the second half of the list
    2. iterate from both ends until they meet, if l != t then not palindromic
    3. reverse the right side of the list again to restore it
    This is not thread-safe as we modify the input, though we do return it unmodified

    123
    1 23
    1234
    12 34

    Input: a->b->a->None
    len=3
    l = a->None
    r = a->None
    a==a
    l==r==None so answer = True
    r=a->None
    len was odd...
        r = b->a->None
    a->b->a->None
    return True

    O(n) time, O(1) space

    Pseudo code
    get the length of the list
    split the list into two at len//2
    if the length is odd:
        skip the first item in the second list
    reverse the second list
    # now there's the same number of items left to traverse in each list
    while there are nodes left:
        if l != r:
            break
    # it's a palindrome if both lists were completely consumed
    answer = l is None and r is None
    reverse the second list
    if length was odd:
        insert skipped value before the start of the second list
    point the end of the first list and the head of the second list
    return answer

    All passed first run.
    Finished at 16:45
    not too bad...

    In their solution they modified the input and did not restore it.  They also re-used reverse from a previous
    question.

    They had a neat trick for finding the middle...
    slow = fast = head
    while fast and fast.next:
        fast, slow = fast.next.next, slow.next
    start_of_second_half = slow

    That's great but not super useful if we want to put the list back together at the end.
    """

    def list_len(head: Optional[ListNode]) -> int:
        length = 0
        while head:
            length += 1
            head = head.next
        return length

    def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
        p, c = None, head
        while c:
            tmp = c.next
            c.next = p
            p, c = c, tmp
        return p

    list_length = list_len(head)
    if list_length <= 1:
        return True
    left_head = left_tail = head
    for _ in range(list_length // 2 - 1):
        left_tail = left_tail.next
    # Split list in two
    right_head = left_tail.next
    left_tail.next = None
    if list_length % 2 == 1:
        # Skip first in right side if odd length
        middle_node = right_head
        right_head = right_head.next
    right_head = reverse_list(right_head)
    l, r = left_head, right_head
    # both lists are the same size so only need to check l or r is None
    while l:
        if l.data != r.data:
            break
        l, r = l.next, r.next
    answer = l is None
    right_head = reverse_list(right_head)
    if list_length % 2 == 1:
        # middle_node is already pointed at the correct next node
        # noinspection PyUnboundLocalVariable
        right_head = middle_node
    left_tail.next = right_head
    return answer


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_list_palindromic.py",
            "is_list_palindromic.tsv",
            is_linked_list_a_palindrome,
        )
    )

from typing import List

from test_framework import generic_test


def apply_permutation(perm: List[int], A: List[int]) -> None:
    """
    [a,b,c,d] p=[1,2,3,0]
    How to apply this permutation in O(n) time and O(1) space?
    Ie how to do it in place?
    There's no easy way to know if there are circular dependencies or not

    p=[3,2,1,0]
    p=[2,3,0,1]

    We could negate the entries in perm as we move items, then reset them back at the end.
    How else can we do this in place?

    For each item in A:
        if it's already been moved, just stop
        otherwise, move it to it's destination in a loop until you get back to the start.
        every time you move an item, negate it in perm.
    re-negate all the items in perm

    a,b,c,d
    2,3,0,1

    move a to 2
    a,b,a,d t=c
    move c to 0
    c,b,a,d
    move b to 3
    c,b,a,b t=d
    move d to 1
    c,d,a,b
    skip i=3
    skip i=4
    re-negate perm

    For each item in A:
        if it's already been moved, just stop
        otherwise, move it to it's destination in a loop until you get back to the start.
        every time you move an item, negate it in perm.
    re-negate all the items in perm


    Ok had an annoying bug.  But all fixed.

    """
    # c,d,a,b
    # 0 1 2 3
    # -2,-3,-0,-1
    # a,b,c,d
    # a, 2
    # p=c
    # n=0
    for i, val in enumerate(A):
        if perm[i] < 0:
            continue
        tmp = val
        prev_idx = i
        while (next_idx := perm[prev_idx]) >= 0:
            A[next_idx], tmp = tmp, A[next_idx]
            perm[prev_idx] -= len(perm)
            prev_idx = next_idx

    # Definitely cannot do slice assignment or we'd use extra space.
    # The book does but pretty sure it's wrong.
    for i in range(len(perm)):
        perm[i] += len(perm)


def apply_permutation_wrapper(perm, A):
    apply_permutation(perm, A)
    return A


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "apply_permutation.py", "apply_permutation.tsv", apply_permutation_wrapper
        )
    )

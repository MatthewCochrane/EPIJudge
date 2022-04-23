from typing import List

from test_framework import generic_test


def intersect_two_sorted_arrays(A: List[int], B: List[int]) -> List[int]:
    """
    Find the intersection of two arrays.
    Example:
        A: 1,2,3,3,4,6,8,9,9
        B: 3,4,10,12
        Result: 3,4

    We can do this by converting each to a set then using intersection.

    That takes O(n + m) time and O(n) space.

    We can improve this by using a pointer-based approach which should be able to do it in
    O(n + m) time and O(1) space.

    If we iterate a pointer over each input list, increment the pointer with the smaller value.  If the
    values are the same then add it to the result (if it's not already the last item in the result).

        A: 1,2,3,3,4,6,8,9,9
                            |
        B: 3,4,10,12
               |

        Result: 3,4

    Pseudo code
    b_idx = 0
    result = []
    for val_a in A:
        while b_idx < len(B) and val_b < val_a:
            b_idx += 1
        if we go off the end of b:
            break
        if val_a == val_b:
            if not equal to last result (and last result exists), add to results
        # else -> val_a < val_b... do nothing, increment a_idx
    return result

    Done.
    Solution 2 takes quite a bit more time than solution 1 because it's all done in python
    whereas solution 1 does a lot in c.
    Still, solution 2 has equal time complexity to solution 1 and better space complexity.

    """
    # solution 2
    b_idx = 0
    result = []
    for val_a in A:
        while b_idx < len(B) and B[b_idx] < val_a:
            b_idx += 1
        if b_idx >= len(B):
            break
        if val_a == B[b_idx]:
            if not result or result[-1] != val_a:
                result.append(val_a)
    return result
    # solution 1
    #return list(sorted(set(A).intersection(B)))



if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('intersect_sorted_arrays.py',
                                       'intersect_sorted_arrays.tsv',
                                       intersect_two_sorted_arrays))

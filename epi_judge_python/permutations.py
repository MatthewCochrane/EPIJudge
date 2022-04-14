from typing import List

from test_framework import generic_test, test_utils


def permutations(A: List[int]) -> List[List[int]]:
    """
    Generate all permutations of an array of items.
    Example:
        permutations([1,2,3]) should return
        {
          [1,2,3]
          [1,3,2]
          [2,1,3]
          [2,3,1]
          [3,2,1]
          [3,1,2]
        }
        n! permutations so 3*2*1 = 6
        3 ways to swap the last two
        when there are two there are only two options

        permutations(A) A with two items
            result.add(A)
            swap A
            result.add(A)
            swap back

         0 1 2
        [3,2,1]
        res = [123,132,213,231,321,312]
        permutations(A, start_idx)
            for i in range(start_idx, len(A)):
                swap start_idx and i
                if start_idx == len(A) - 2:
                    add to result
                else:
                    permutations(A, start_idx + 1)
                swap start_idx and i back
        permutations(A, 0)
        return res


    One small bug with single length arrays.
    """
    result = []

    def permutations(start_idx):
        for i in range(start_idx, len(A)):
            A[start_idx], A[i] = A[i], A[start_idx]
            if start_idx == len(A) - 2:
                result.append([*A])
            else:
                permutations(start_idx + 1)
            A[i], A[start_idx] = A[start_idx], A[i]

    if len(A) == 1:
        return [[*A]]
    permutations(0)
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "permutations.py",
            "permutations.tsv",
            permutations,
            test_utils.unordered_compare,
        )
    )

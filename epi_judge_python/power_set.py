from typing import List

from test_framework import generic_test, test_utils


def generate_power_set(input_set: List[int]) -> List[List[int]]:
    """
    Start: 16:33
    Return the set of all subsets of S.
    Remember that there are 2^n subsets of a set S of length n.
    We can generate this in different ways.
    In essence every number in S is either included or not.  That gives n binary choices
    and 2^n results.
    One way to do this is to just enumerate the numbers from 0 to 2^n, then for each bit
    chose whether to include that value from S in the result set.
    We can also solve it recursively.
    We either chose to include S[0] or not, then for each of those choices we include the powerset of S[1:]

    iterative:
    for i in range(int(2**n)):
        results.append(list(filter(lambda j: (1<<j) & i, range(n))))

    recursive:
    result = []
    results = []
    def backtrack(start_idx):
        if start_idx == len(nums):
            results.append([*result])]
            return
        backtrack(start_idx + 1)
        result.append(nums[start_idx])
        backtrack(start_idx + 1)
        result.pop()
    backtrack(0)
    return result

    Finish 16:46
    """
    # 75 us
    result = []
    results = []

    def backtrack(start_idx):
        if start_idx == len(input_set):
            results.append([*result])
            return
        backtrack(start_idx + 1)
        result.append(input_set[start_idx])
        backtrack(start_idx + 1)
        result.pop()

    backtrack(0)
    return results

    # 248 ms
    n = len(input_set)
    results = []
    for i in range(int(2 ** n)):
        results.append(
            list(map(lambda x: input_set[x], filter(lambda j: (1 << j) & i, range(n))))
        )
    return results


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "power_set.py",
            "power_set.tsv",
            generate_power_set,
            test_utils.unordered_compare,
        )
    )

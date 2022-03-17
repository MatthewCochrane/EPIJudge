import functools
import random
from typing import List

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    binomial_coefficient, check_sequence_is_uniformly_random,
    compute_combination_idx, run_func_with_retries)
from test_framework.test_utils import enable_executor_hook


def random_subset(n: int, k: int) -> List[int]:
    """
    start: 16:05
    Return a random permutation of a random subset with k elements selected from 0..n-1

    example
    n = 4, k = 2
    0,1,2,3, select 2
    [a,b]
    a should have a 1/4 chance of being 0,1,2,3
    b should have a 1/4 chance of being 0,1,2,3

    Just do a random shuffle.
    permutations are equally likely.

    if all the permutations are equally likely, does that mean that all the subsets are equally likely?

    n=3, k=2
    {1,2} -> [1,2], [2,1]
    {0,1} -> [0,1], [1,0]
    {0,2} -> [0,2], [2,0]

    Can do this in O(n) time, O(n) space.

    Pseudo code
    build array of 0..n-1
    shuffle array in place
    take the first k items

    But, when we do this shuffle, once we move an item to an index, it stays there!

    So really we can shuffle just the first k items.

    O(n) time, O(n) space
    build array of 0..n-1
    shuffle the first k items
    return first k items

    when we do each shuffle we're saying, pick a number we haven't picked yet.

    if n >> k, the random selection thing would be better
    it would be O(k log k) time and O(k) space

    Finished at 16:24 but confident I don't have an optimal solution

    0,1,2,3,4, k=3
    {3:0, 0:3}  [3,1,2,0,4]
    {3:0, 0:3, 2:1, 1:2} [3,2,1,0,4]
    {3:1, 0:3, 2:0, 1:2} [3,2,0,1,4]
    """
    # O(k) space approach
    d = {}
    for i in range(k):
        j = random.randrange(i, n)
        vi = d.get(i, i)
        vj = d.get(j, j)
        d[i] = vj
        d[j] = vi
    return [d[i] for i in range(k)]

    # O(n) space approach
    # A = list(range(n))
    # for i in range(k):
    #     j = random.randrange(i, n)
    #     A[i], A[j] = A[j], A[i]
    # return A[:k]


@enable_executor_hook
def random_subset_wrapper(executor, n, k):
    def random_subset_runner(executor, n, k):
        results = executor.run(
            lambda: [random_subset(n, k) for _ in range(100000)])

        total_possible_outcomes = binomial_coefficient(n, k)
        comb_to_idx = {
            tuple(compute_combination_idx(list(range(n)), n, k, i)): i
            for i in range(binomial_coefficient(n, k))
        }
        return check_sequence_is_uniformly_random(
            [comb_to_idx.get(tuple(sorted(result)), 0) for result in results],
            total_possible_outcomes, 0.01)

    run_func_with_retries(
        functools.partial(random_subset_runner, executor, n, k))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('random_subset.py', 'random_subset.tsv',
                                       random_subset_wrapper))

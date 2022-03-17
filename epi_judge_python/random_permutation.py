import copy
import functools
import math
import random
from typing import List

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    check_sequence_is_uniformly_random,
    run_func_with_retries,
)
from test_framework.test_utils import enable_executor_hook


def compute_random_permutation(n: int) -> List[int]:
    """
    start: 15:38
    Uniformly random permutations of 0..n-1
    This is similar to a fischer-yates shuffle.

    As described in the question, the problem is that a 'naive' shuffle has
    n^n different possible states while there are only n! true permutations of n numbers.
    eg. with n=3 that's 3^3 = 27 but there are only 3! = 6 permutations.
    And we can't evenly divide 27 by 6 beaning that some of the permutations have greater
    probability than others.

    To handle this with a shuffle we swap only the remaining elements.
    eg.
    [0,1,2,3,4]
    swap 0 with anything between 0 and 4
    [1,0,2,3,4]
    swap index 1 with anything between 1 and 4
    swap index 2 with anything between 2 and 4
    so on up to 4
    This gives us
    5*4*3*2*1 different options which has the same number of options as n!
    From the first swap you can see there's an equal chance for any number to end up in position 0
    then for the second swap, there's a 1/(n-1) probability for each remaining item to end up there
    [1/n, 1/(n-1), 1/(n-2), ...]

    n = 4
    [0,1,2,3]
    swap one of the 4 numbers with index 0
    1/4 chance of each number going in index 0
    swap one of 1..4 with 1
    1/3 chance of each of the remaining numbers going in 1
    swap one of 2..4 with 2
    1/4 chance of each of the remaining numbers going in 2
    don't need to swap the last one

    1 -> 1/3 chance of being any of 1,2,3 and 1,2 and 3 each have a 1/4 chance of being 0
    3/12->1 and 1/12->0
    3/12->2 and 1/12->0
    3/12->3 and 1/12->0
    1/4 of 1,2,3, 1/4 of 0

    Pseudo code
    create an array of 0..n
    for each index in the array:
        swap that index with one >= it
    return result

    Finished: 15:54  And spent a lot of time explaining the probability stuff too
    O(n) time complexity
    O(1) space complexity
    """
    result = list(range(n))
    for i in range(n):
        j = random.randrange(i, n)
        result[i], result[j] = result[j], result[i]
    return result


@enable_executor_hook
def compute_random_permutation_wrapper(executor, n):
    def compute_random_permutation_runner(executor, n):
        def permutation_index(perm):
            p = copy.deepcopy(perm)
            idx = 0
            n = len(p)
            while p:
                a = p.pop(0)
                idx += a * math.factorial(n - 1)
                for i, b in enumerate(p):
                    if b > a:
                        p[i] -= 1
                n -= 1
            return idx

        result = executor.run(
            lambda: [compute_random_permutation(n) for _ in range(1000000)]
        )

        return check_sequence_is_uniformly_random(
            [permutation_index(perm) for perm in result], math.factorial(n), 0.01
        )

    run_func_with_retries(
        functools.partial(compute_random_permutation_runner, executor, n)
    )


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "random_permutation.py",
            "random_permutation.tsv",
            compute_random_permutation_wrapper,
        )
    )

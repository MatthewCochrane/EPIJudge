import functools
from typing import List
import random

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    binomial_coefficient, check_sequence_is_uniformly_random,
    compute_combination_idx, run_func_with_retries)
from test_framework.test_utils import enable_executor_hook


def random_sampling(k: int, A: List[int]) -> None:
    """
    Start: 11:41
    Input an algorithm that takes an array of elements and size, and returns a subset with
    the given size.  All subsets should be equally likely.  Return the modified input array.

    Example 1:
     [a,b,c,d], 1
     there are 4 valid subsets, each of which should be equally likely

    Example 2:
     [a,b,c,d], 2
     There are nCr options (4C2) = n!/(r!*(n-r)! = 4!/((4-2)!) = 4*3*2*1/4 = 6
     6 combinations
     a,b
     a,c
     a,d
     b,c
     b,d
     c,d

     pick 1/4 options
     then pick 1/3 options

     Could do an in-place shuffle, then truncate.
     Or
     pick a random number between 0 an len-1, swap with arr[0]
     pick a random number between 1 and len-1, swap with arr[1]

    for i in range(n):
       pick a random number between i and len-1, swap with arr[i]
    delete all elements after n

    similar to fischer-yates shuffle (knuth shuffle)

    0123
    3120
    3

    4*3 = 12 options
    there are 6 options.. these divide equally

    3*2 = 6
    3!/2!*1!=6/2=3

    012
    01
    02
    10
    12
    20
    21

    Even though there are multiple ways, there's still an equal probability for each subset.

    select 3 from 4
    432 4*3*2
    n choose k = 4 choose 2 = 4!/2!(4-2)! = 4!/2!*2! = 4*3*2/(2*2) = 4*3*2/4
    1/k!*(n!/(n-k)!)
         =========== we have this bit with our method
    ^^^^------------ So our bit is always a multiple of k! of (n choose k)
    Therefore the number of states will always divide evenly.

    for i in range(k):
       pick a random number between i and len-1, swap with arr[i]
    delete all elements after k
    O(k) time complexity if we don't have to delete, or O(n) if we do
    O(1) space complexity

    Passed without deleting elements after k.

    Ok, just a note that it is *super super* important to remember this n choose k formula!!
    I would have been lost without it.

    Finish at 12:18  I did eat lunch during this time too.

    """
    for i in range(k):
        j = random.randrange(i, len(A))
        A[i], A[j] = A[j], A[i]


@enable_executor_hook
def random_sampling_wrapper(executor, k, A):
    def random_sampling_runner(executor, k, A):
        result = []

        def populate_random_sampling_result():
            for _ in range(100000):
                random_sampling(k, A)
                result.append(A[:k])

        executor.run(populate_random_sampling_result)

        total_possible_outcomes = binomial_coefficient(len(A), k)
        A = sorted(A)
        comb_to_idx = {
            tuple(compute_combination_idx(A, len(A), k, i)): i
            for i in range(binomial_coefficient(len(A), k))
        }

        return check_sequence_is_uniformly_random(
            [comb_to_idx[tuple(sorted(a))] for a in result],
            total_possible_outcomes, 0.01)

    run_func_with_retries(
        functools.partial(random_sampling_runner, executor, k, A))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('offline_sampling.py',
                                       'offline_sampling.tsv',
                                       random_sampling_wrapper))

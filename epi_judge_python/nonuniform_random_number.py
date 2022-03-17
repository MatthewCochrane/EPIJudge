import collections
import functools
import math
import random
from typing import List

from test_framework import generic_test
from test_framework.random_sequence_checker import run_func_with_retries
from test_framework.test_utils import enable_executor_hook


def nonuniform_random_number_generation(
    values: List[int], probabilities: List[float]
) -> int:
    """
    Start: 17:00
    Pick one of the values weighted by the probabilities.

    Eg.
    values = 1,2,3,4
    probs  = 1,1,2,2 (all /6)

    Can't we just sum the probabilities?
    We could use a cumulative probability?
    So pick a value between 0 and 1
    if the value is less than 1/6 then use 1
    if the value is less than 1/6 + 1/6 = 2/6, use 2
    if the value is less than 2/6 + 2/6 = 4/6 use 3
    else use 4
    It could be worthwhile to sort the probabilities, so that the most likely ones come first and we can iterate
    through less of them.  However sorting takes O(n log n) time.
    If we were calling this multiple times we'd want to do that, but since we get a new probability distribution
    passed in for every call it's better just to keep working our way through the probabilities.

    My approach here is O(n) time and O(1) space.  It requires one call to rand().

    Pseudo code:
    could be worth having error checking to see that probs sums to 1.0
    and that vals and probs have the same length
    pick a random number between 0 and 1
    cumulative_sum = 0
    for each index:
        add probs[i] to cumulative sum
        if random value < cumulative sum return value[i]

    Finish: 17:14 Nice...

    They assume it's sorted and then, strangely create an array of cumulative sums then binary search it.
    That is only faster if you can re-use the cumulative sum array, which you can't in this question.
    """
    rand_val = random.random()
    cum_sum = 0.0
    for prob, val in zip(probabilities, values):
        cum_sum += prob
        if rand_val < cum_sum:
            return val


@enable_executor_hook
def nonuniform_random_number_generation_wrapper(executor, values, probabilities):
    def nonuniform_random_number_generation_runner(executor, values, probabilities):
        N = 10 ** 6
        result = executor.run(
            lambda: [
                nonuniform_random_number_generation(values, probabilities)
                for _ in range(N)
            ]
        )

        counts = collections.Counter(result)
        for v, p in zip(values, probabilities):
            if N * p < 50 or N * (1.0 - p) < 50:
                continue
            sigma = math.sqrt(N * p * (1.0 - p))
            if abs(float(counts[v]) - (p * N)) > 5 * sigma:
                return False
        return True

    run_func_with_retries(
        functools.partial(
            nonuniform_random_number_generation_runner, executor, values, probabilities
        )
    )


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "nonuniform_random_number.py",
            "nonuniform_random_number.tsv",
            nonuniform_random_number_generation_wrapper,
        )
    )

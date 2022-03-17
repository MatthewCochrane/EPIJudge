import functools
import random
from collections import Counter
from typing import Iterator, List

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    binomial_coefficient,
    check_sequence_is_uniformly_random,
    compute_combination_idx,
    run_func_with_retries,
)
from test_framework.test_utils import enable_executor_hook


# Assumption: there are at least k elements in the stream.
def online_random_sample(stream: Iterator[int], k: int) -> List[int]:
    """
    Start 13:00
    Take the size k and the stream.  Continuously maintain a uniform
    random subset of size k from the read packets.

    Clearly if k < len(stream) then we don't have k items to return.
    so len(result) = min(len(stream), k).

    Think of it like this

    stream = 0,1,2,3
    k = 2
    see 0
    res = [0]
    see 1
    res = [0, 1]
    see 2
    res should have equal probability of
    [0,1] [1,0]
    -----------
    [0,1] [1,0]
    [2,1] [2,0]
    [0,2] [1,2]

    0,1 2
    0,2 2
    1,2 2

    nCr -> 3C2 = 3 -> n!/(k!(n-k)!) = 3!/2!(1!) = 3!/2! = 3

    {2, 1}, {0, 2}, {0, 1}
    see 3
    res should have equal probability of

    nCr -> 4C2 = 3 -> n!/(k!(n-k)!) = 4!/2!(4-2)! = 4!/2!*2! = 4*3/2 = 6

    [0,1] [1,0] [2,1] [2,0] [0,2] [1,2]
    -----------------------------------
    [0,1] [1,0] [2,1] [2,0] [0,2] [1,2]
    [0,1] [1,0] [2,1] [2,0] [0,2] [1,2]
    [3,1] [3,0] [3,1] [3,0] [3,2] [3,2]
    [0,3] [1,3] [2,3] [2,3] [0,3] [1,3]

    0,1 4
    0,2 4
    0,3 4
    1,2 4
    1,3 4
    2,3 4

    1 - no swap
    1 - swap with 0
    1 - swap with 1

    50% chance of no swap
    1/k chance of swap with k
    Could do a 1-larger example...

    [0,1] [1,0] [2,1] [2,0] [0,2] [1,2] [0,1] [1,0] [2,1] [2,0] [0,2] [1,2] [3,1] [3,0] [3,1] [3,0] [3,2] [3,2] [0,3] [1,3] [2,3] [2,3] [0,3] [1,3]
    a
    b
    c


    {2, 1}, {0, 2}, {0, 1}
    ----------------------
    {2, 1}, {0, 2}, {0, 1}
    {3, 1}, {3, 2}, {3, 1}
    {2, 3}, {0, 3}, {0, 3}

    first three have equal probability
    we know there are 6 total options (nCr for 4C2 = 6)
    so how do we select equal probability of all?
    need common factor between 3 and  6
    3+6 = 9 and 9 does not divide evenly into 6
    if we double the 3 we get 6+6 = 12 and 12/2 = 6.  This only really works
    because there's an equal chance (2) of every value.

    0,1 1
    0,2 1
    0,3 2
    1,2 1
    1,3 2
    2,3 2
    not evenly distributed
    So we can't just keep picking a random index and swapping with it.

    {0, 1}, {0, 2}, {0, 3} {1, 2}, {1, 3}, {2, 3}
    ---------------------------------------------
    {0, 1}, {0, 2}, {0, 3} {1, 2}, {1, 3}, {2, 3}
    {0, 1}, {0, 2}, {0, 3} {1, 2}, {1, 3}, {2, 3}
    {0, 1}, {0, 2}, {0, 3} {1, 2}, {1, 3}, {2, 3}

    there are 3 choices -> k + 1

    if k was different, like 3...
    v v v v v
    ---------
    v v v v v Orig
    v v v v v
    v v v v v
    v v v v v
    nCr 4C3
    there will be r copies of each option

    from nCr -> n+1Cr  There are z values then there are r*z
    n!/k!(n-k)!
    (n+1)!/k!(n-k+1)!
    n/(n-k+1)

    (n-k)!/(n-k+1)!
    z!/(z+1)!
    =1/((z+1)!/z!)=1/z+1
    5,2
    3!/(3+1)!
    3!/4! = 4

    swap val with 2 n times
    swap val with n 2 times

    50% chance, then if true replace 1 of the r indices

    {1,2,3} {0,2,3} {0,1,3} {0,1,2}
    -------------------------------
    {1,2,3} {0,2,3} {0,1,3} {0,1,2}
    {1,2,3} {0,2,3} {0,1,3} {0,1,2} extra chance
    -------------------------------
    {4,2,3} {4,2,3} {4,1,3} {4,1,2}
    {1,4,3} {0,4,3} {0,4,3} {0,4,2}
    {1,2,4} {0,2,4} {0,1,4} {0,1,4}

    01 {2,3,4} 2
    02 {1,3,4} 2
    03 {1,2,4} 2
    04 {1,2,3}
    12 {0,3,4} 2
    13 {0,2,4} 2
    14 {0,2,3}
    23 {0,1,4} 2
    24 {0,1,3}
    34 {0,1,2}

    10 options
    4 already accounted for
    12 new ones -> the 6 unseen, two each.
    so we

    nCr with 4C3 = n!/k!*(n-k)! = 4!/3!*(4-3)! = 4!/3! = 4
    nCr with 5C3 = n!/k!*(n-k)! = 5!/3!*(5-3)! = 5!/3!*2 = 5*4/2 = 10

    two chances at all of the original ones
    why two chances?

    What if we go from 8->9 with 4 items?
    n choose k = n!/k!(n-k)!
    8 choose 4 = 8!/4!(8-4)! = 8!/4!*4! = 8*7*6*5/4*3*2 = 8*7*5/4 = 2*7*5 = 70
    9 choose 4 = 9!/4!(9-4)! = 9!/4!*5! = 9*8*7*6/4*3*2 = 9*8*7/4 = 9*7*2 = 63*2 = 126

    126 options
    70 already accounted for
    126-70 = 56 new ones, two each?? -> 112
    7*8

    8 options for each of the 70?
    8*70 = 560
    560 + ? = 126
    126 = (560 + 700) / 10

    ---------------- 70 options
    XXXXXXXXXXXXXXXX
    XXXXXXXXXXXXXXXX 560 options
    XXXXXXXXXXXXXXXX


    if there's 10 chances for each of the 70, then there's a 10 in (700+560) = 1/126
    if there's 10 chances for each of the 56, then there's a 10 in (700+560) = 1/126

    need to sum to a multiple of 126
    70*x + 560 = 126*y

    126*y - 560 = 70x
    (126*y - 560)/70 = x
    1260 - 560/70 = x
    (126 - 56)/7 = x
    70/7 = x = 10

    n-1 choose k = cp
    n choose k  = cn

    cn - cp = z
    n*(n-1) = zz
    zz/z
    n*(n-1)/(cn-cp) = number of times each value can appear in new results

    if we can appear 2 times in the new result then we'd need to have 2 chances at the original and
    one chance at each new result

    if we can appear 4 times in the new result then we'd need to have 4 chances at the original and
    one chance at each new result

    But that's just a 50/50 chance between the previous and the new results, regardless of where you're at.


    if < k items in result, add to result
    When we add a new number, flip a coin, if heads, do nothing
    if tails, roll an n sided die and replace that value with v

    O(1) time complexity per number you ingest so O(n) over the whole stream.

    let's say we have
    [1,2,3,4], k=1
    we've consumed 1,2,3 and have selected 2 at the moment
    when we consume 4 it's easy to see that there should be a 1/4 chance of using 4 as the result

    another example
    [1,2,3,4], k=2
    after consuming 1,2,3 and have [1,2] selected
    when we consume 4, there's a 50/50 chance it should be used in the result.

    Well I got there but it required some trial and error.....
    This is a good way to think about it.  Though I don't completely understand why it works.
    I should repeat this question!

    """
    result = []
    for n, v in enumerate(stream):
        if len(result) < k:
            result.append(v)
            continue
        if random.random() < k/(n+1):
            result[random.randrange(k)] = v
    return result

@enable_executor_hook
def online_random_sample_wrapper(executor, stream, k):
    def online_random_sample_runner(executor, stream, k):
        results = executor.run(
            lambda: [online_random_sample(iter(stream), k) for _ in range(100000)]
        )

        total_possible_outcomes = binomial_coefficient(len(stream), k)
        stream = sorted(stream)
        comb_to_idx = {
            tuple(compute_combination_idx(stream, len(stream), k, i)): i
            for i in range(binomial_coefficient(len(stream), k))
        }
        return check_sequence_is_uniformly_random(
            [comb_to_idx.get(tuple(sorted(result)), 0) for result in results],
            total_possible_outcomes,
            0.01,
        )

    run_func_with_retries(
        functools.partial(online_random_sample_runner, executor, stream, k)
    )


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "online_sampling.py", "online_sampling.tsv", online_random_sample_wrapper
        )
    )

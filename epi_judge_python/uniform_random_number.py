import functools
import random
import math

from test_framework import generic_test
from test_framework.random_sequence_checker import (
    check_sequence_is_uniformly_random,
    run_func_with_retries,
)
from test_framework.test_utils import enable_executor_hook


def zero_one_random():
    return random.randrange(2)


def uniform_random(lower_bound: int, upper_bound: int) -> int:
    """
    Start: 14:06
    Using a random number generator that can generate either 1 or 0, create
    chose a random number between lower bound and upper bound.
    The distribution should be even! That means there should be an equal
    probability of generating all values in the range.
    Both upper and lower bounds are *included*.

    Example:
        lower = 0
        upper = 1
        here we can just call zero_one_random()

    Example 2:
        lower = 0
        upper = 5
        There are 6 valid values.  Each should have an even probability
        000
        001
        010
        011
        100
        101
        110
        Tricky, we can't quite just generate three bits from zero_one_random...
        There are 8 possible values that could be produced and we can't evenly
        distribute 8 things across 6 values. (8 doesn't divide evently into 6)
        Another way could be to find the nearest power of two that the number
        of items in the range divides evenly into.
        eg. here we need 6 values.
        8 / 6 ..
        16 / 6
        32 / 6 =
        64 / 6 .. 66 is close
        128 / 6
        Actually, will 6 ever divide evenly into a power of 2?

        0b110
        We could use 8, then if we get a number more than 6 just 're-roll'.  This has bad
        worst case performance but really bad performance is very unlikely.

        Here there's a 6/8 or 3/4 chance that we get an answer on the first 'roll'
        The worst case would be if we selected a number that's just larger than a power two.
        Eg. 513 -> we'd need 10 bits, so there's about a 50% chance we don't hit a value between 0 and 513.
        Chances are that we'd hit a value within a few rolls though.
        But can we guarantee an answer every time without 're-rolling'?

        Need the distribution to 'fit'.  So if you have 10 numbers, you can only select a power of 2...
        0
        1
        2
        3
        4

        5
        6
        7
        8
        9

        if count is even...
            split in two
        if count is odd...

        3 numbers

        0
        1
        2

        2, 4, 8, 16
        2*x = 3
        x = 3/2
        Ohh, instead of 2*2*2 we want 2+2+2
        So take three numbers, a, b and c.  Sum them to get a number between 0 and 2.  Use that result.

        Ok, now what if we have a larger odd number
        5

        0 12.5
        1 12.5
        2 12.5
        3 12.5
        4 50%

        divide by 2?
        We actually can't split it in two...  Unless the ratios are right.
        2/5 and 3/5
        2*2+2
        2*2 = 4 +

        Time: 14:30 about 25 mins
        In the interest of time let's do the re-rolling one

        Pseudo code
        find the size of the range (upper - lower + 1)
        take log2 of size to find the number of bits we need ** floor and add one to log val?
        generate a number with that many bits using the 0-1 random generator
        if the generated number is >= the size, try again
        add lower to the generated number (lowest generated number should be zero)
        return the result

        test:
        lower = 5, upper = 10
        find size of range = 10 - 5 + 1 = 6
        floor(log2(6)) + 1 = 3 (2^3 = 8)
        random = 0b110
        6 >= size
        random = 0b101
        5 + 5 = 10
        return 10

    Time complexity is O(log n) where n is the range.
    Space complexity is O(1) as long as we don't included the generated bits that are the result.

    Time: 14:48
    Took 42 minutes.
    Hmm, this is ok but still a bit long.
    Also, I should probably ask beforehand, how long do you expect this to take, so I know how fast to go,
    when to search for more optimal solutions, etc.

    Ok, I had an interesting bug with the walrus operator there!
    doing `x := f() > y` is saying `x := (f(x) > y)` but I wanted `(x := f(x)) > y`.  Good one to be aware
    of!  I don't use the walrus often.  It's actually pretty helpful too!  I would have had to call the
    function in two places if I didn't use the walrus!

    Ok, now that I'm done, can I think of a way to do this without the 're-rolls'?
    Or can I prove that we can't find a number z such that 3*z = 2^z
    3 = 2^z / z
    log2(3z) = z
    """
    size = upper_bound - lower_bound + 1
    bits = math.floor(math.log2(size)) + 1

    def n_bit_random(n: int) -> int:
        result = 0
        for i in range(n):
            if zero_one_random():
                result |= 1 << i
        return result

    while (rand_num := n_bit_random(bits)) >= size:
        pass
    return rand_num + lower_bound


@enable_executor_hook
def uniform_random_wrapper(executor, lower_bound, upper_bound):
    def uniform_random_runner(executor, lower_bound, upper_bound):
        result = executor.run(
            lambda: [uniform_random(lower_bound, upper_bound) for _ in range(100000)]
        )

        return check_sequence_is_uniformly_random(
            [a - lower_bound for a in result], upper_bound - lower_bound + 1, 0.01
        )

    run_func_with_retries(
        functools.partial(uniform_random_runner, executor, lower_bound, upper_bound)
    )


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "uniform_random_number.py",
            "uniform_random_number.tsv",
            uniform_random_wrapper,
        )
    )

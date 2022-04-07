import random
from typing import Iterator

from test_framework import generic_test
from test_framework.test_failure import TestFailure


def find_missing_element(stream: Iterator[int]) -> int:
    """
    How can we find an element that was not in stream.
    the stream contains 1 billion values
    there are 32 bits -> about 4 billion values
    So how can you find one of these missing values?
    every time we see a new value we can split the space in two?
    We could use a tree
    tree represents from 0 to ffffffff

    say we have a simpler problem.  Find the missing element in a stream of 4 bit numbers

    when we start, any number is a valid return value

    then we see

    0110 (6)

    we now know that valid values are
    0->5
    7->15

    next we see 3

    Now we have

    0->2, 4->5 and 7->15

    then 5 and 4
    0->2, 7->15

    It's unlikely that we'll get numbers that are close to each other
    If we didn't get any neighbours then this would take the full 1GB worth of ram to store...

    We only have a few MB
    Remember that approx 3/4 numbers are free.
    So could we just discard half the search space every time?  NO!  that's going to lead to a very
    small search space very quickly... Or is it?
    If the next number was outside the search space then it wouldn't reduce the search space...

    Ok so what if we just keep a single range for min/max.

    see 6

    we discard from 0->6 (the smaller part)
    the new range is from 7->15
    now we see 3, we discard nothing because 3 < 7
    now we see 5 and 4, we discard nothing because they are also < 7
    On this small dataset it's possible that this could fail.  Could it fail on a large dataset too?

    Say we get 2billion, we discard from 0 to 2billion
    then we get half way between that and 4 billion
    then half way between the search space again
    keep going until you discard the whole search space...

    Fundamentally, we can't track every number that was discarded.
    We can pick say a million random numbers.  Then for each item that we see, check if that number is seen.
    If we use every number, then start again.
    O(n) space, O(n) time.  Worst case we could have to try a bunch of times but because we randomly select
    the numbers we shouldn't have to do that many times and the probability would be very low.

    create set of 10^6 random elements
    go through input until we find a value that's not in the result
    if we get to the end, start again with new random elements


    Are we able to find an answer without iterating through the whole stream?

    If we use 10^6 items then the probability of not seeing a result is 1/4?
    there are 2^^32 / 4 values = 2^^30

    If I pick 1 value, there's a 1/4 chance that it's used.
    If I pick 2 values, there's
        either we pick

    I have 2^30 values from a set of 2^32 values.  What is the probability that I select 10^6 values from them

    I have a deck of 52 cards but I remove all of the spades.  If I select N cards from a full deck, what's the
    probability of drawing a spade?
    Number of ways to choose 10^6 from 2^32 = 2^32C10^6
    There are (2^30)C10^6 ways to choose 10^6 items from the remaining 2^30 values.
    We can calculate the probability that we pick at least one of the missing values by working out the probability
    of not picking any of them and subtracting that from 1.
    If there are X ways to fail to select any missing value and Y ways to select from the full set then there is a
    X / Y probability of selecting no missing values.

    so the probability of selecting at least one missing value is 1- X/Y
    which is

    1 - (2^30C10^)/(2^32C10^) = basically 1

    if we use 1000 samples instead of 1 million, the probability of getting no values is 1- 10^-603 which is
    vanishingly small.
    I think that does make sense.  We're asking, what's the probability of randomly selecting values that have very
    very low entropy?

    I have a bag of N marbles and N/4 of them are blue, the other 3N/4 are red
    What's the probability of selecting a red marble?
    3/4
    What if you have two picks?
    3/4 + 1/4 * ((3N/4)-1)/(N/4)
    = 3/4 + ((3N/4)-1)/N
    What if you have K picks?
    = 3/4 + sum(x*((3N/4)-x)/N, from 1 to k)


    The answer said:
    Break it down into 2^16 different buckets, count the number of entries in each bucket.
    Find the first bucket that isn't full.
    Then enumerate all 2^16 values in the first non-full bucket.
    Iterate through the list again and find a bucket that

    This requires iterating the list twice, but they made a mistake.  They use Tee in the iterator
    which just makes a complete copy of the stream.  This is not allowed!

    I like my (actually Kat's!) solution way more.  It's far simpler and almost guaranteed to work in
    a single pass.  In very very rare circumstances it may require a second pass.
    Therefore I'd say it's superior to their solution.
    I don't think it would be superior if the ratios were different though.  If there was only like 1/1000000
    free values instead of 3/4 free values then this approach wouldn't work well.
    Because you'd be selecting say 1000 items from 2^32 but there's only a 1/1000000 probability of it working.
    If you randomly sampled 10^6 values, and there were 1000 free values from 2^32.  The probability of finding a
    result would be
    1-(combination(2^32-1000,10^6)/combination(2^32,10^6))
    or 0.207 so about 1/5
    If you used 10 million values the probability goes to about 90%
    If you use 100 million values the probability is 99.999999999%

    So again this approach works well because there are lots of free values, if there are very few free values
    a different approach would be better.

    """
    candidates = set([random.randrange(2 ** 32) for _ in range(1000)])
    for val in stream:
        if val in candidates:
            candidates.remove(val)
    print(len(candidates))
    if not candidates:
        raise IndexError("Couldn't find an answer")
    return candidates.pop()


def find_missing_element_wrapper(stream):
    try:
        res = find_missing_element(iter(stream))
        if res in stream:
            raise TestFailure("{} appears in stream".format(res))
    except ValueError:
        raise TestFailure("Unexpected no missing element exception")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "absent_value_array.py",
            "absent_value_array.tsv",
            find_missing_element_wrapper,
        )
    )

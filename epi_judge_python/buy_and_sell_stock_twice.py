import functools
import math
from typing import List, Tuple

from test_framework import generic_test


def buy_and_sell_stock_twice(prices: List[float]) -> float:
    """
    Start: 9:18
    Buy and sell a stock twice...

    Buy, sell, buy sell
    we can do nothing
    we can buy & sell once
    we can buy and sell twice

    Will have some prices and need to work out the best time to buy and sell...

    Use a state machine and keep track of best value

    There are only 5 states
    0 buy
    1 buy
    1 sell
    2 buy
    2 sell

    we transition between the states
    0 buy to 1 buy -> total profit = 0 - stock price at that time
    1 buy to 1 sell -> total profit = prev profit in 1 buy state + stock price at that time
    ... so on

    at each point in time we ask if we were to take this action what's the best profit we could have at this point in
    time?


            6, 8, 9, 3, 4, 7, 8, 2, 9, 1
    0 buy   0, 0, 0, 0  0, 0, 0, 0, 0, 1
    1 buy  -6,-6,-6,-3,-3,-3,-3,-2,-2,-1
    1 sell  X, 2, 3, 3, 3, 4, 5, 5, 7, 7
    2 buy   X, X,-7, 0, 0, 0, 0, 3, 3, 6
    2 sell  X, X, X,-4, 4, 7, 8, 8,12,12

    # best profit after (1 buy, 1 sell, 2 buys, 2 sells)
    state = (-inf, -inf, -inf, -inf)
    for val in A:
        state = (
            max(state[0], -val), # buying
            max(state[1], state[0] + val), # selling
            max(state[2], state[1] - val), # buying
            max(state[3], state[2] + val), # selling
        )
    return max(state)

    O(n) time
    O(1) space
    Finish: 9:39
    Not that useful I just 'knew' the answer.....


    """

    state = (-math.inf, -math.inf, -math.inf, -math.inf)
    for val in prices:
        state = (
            max(state[0], -val),  # buying
            max(state[1], state[0] + val),  # selling
            max(state[2], state[1] - val),  # buying
            max(state[3], state[2] + val),  # selling
        )
    return max(max(state), 0)


def buy_and_sell_stock_twice_second(prices: List[float]) -> float:
    """
    Start: 08:51
    Compute maximum profit from buying and selling a share at most twice.

    3 2 5 8 4 5 6 9 1 2 3

    O(n^2) options -> can enumerate all options and compare to find max profit

    high - low

    largest max after smallest min

    pseudo code:
    for buy/sell once

    min_so_far = inf
    best_profit = 0
    for val in prices:
        min_so_far = min(min_so_far, val)
        best_profit = max(best_profit, val - min_so_far)
    return best_profit

    O(n) time, O(1) space

    Now what if we want to buy and sell up to twice?

    3 2 5 8 4 5 6 9 1 2 3

    8
    6+5 = 11
    9
    9
    8
    7
    max = 11

    Split the array?
    Could split the array at every index and run the above algorithm on each half?
    O(n^2) -> O(n) n times - Time complexity
    O(1) space

    states
    start
    onebuy
    onesell
    twobuys

            3  2  5  8  4  5  6  9  1  2  3
    wait0   0  0  0  0  0  0  0  0  0  0  0
    (buy)
    hold1  -3 -2 -2 -2 -2 -2 -2 -2 -1 -1 -1
    (sell)
    wait1   X -1  3  6  6  6  6  7  7  7  7
    (buy)
    hold2   X  X -6 -5  2  2  2  2  6  6  6
    (sell)
    wait2   X  X  X  2  2  7  8  11 11 11 11

    result = max(0,-1,7,6,11)

    if we only keep prev and next
    O(1) space
    O(n) time

    Pseudo code
    # state represents max profit so far in different situations
    # (hold after 1 buy, wait after 1 sell, hold after 2 buys, wait after 2 sells)
    initialise our state = (-inf, -inf, -inf, -inf)
    def next_state(prev_state, price):
        return (
            max(prev_state[0], -price),
            max(prev_state[1], prev_state[0] + price),
            max(prev_state[2], prev_state[1] - price),
            max(prev_state[3], prev_state[2] + price),
        )
    state = functools.reduce(next_state, prices)
    return max(0, max(state))

    All tests passed.
    Finish: 9:37
    36 mins . Not too bad...

    """

    def next_state(prev_state: Tuple, price: float) -> Tuple:
        return (
            max(prev_state[0], -price),
            max(prev_state[1], prev_state[0] + price),
            max(prev_state[2], prev_state[1] - price),
            max(prev_state[3], prev_state[2] + price),
        )

    # state represents max profit so far in different situations
    # (hold after 1 buy, wait after 1 sell, hold after 2 buys, wait after 2 sells)
    final_state = functools.reduce(
        next_state, prices, (-math.inf, -math.inf, -math.inf, -math.inf)
    )
    return max(0, max(final_state))


def buy_and_sell_stock_twice_first_go(prices: List[float]) -> float:
    """
    A non-optimal O(n^2) solution...

    Pseudo code
    split prices into two at every possible point:
        search for best profit in each subarray
        add the results
        if result is better than the best so far, update it

    This passed, took 2s average run time.
    The last two tests took 571s and 626s!  Suuuuuper slow.
    """

    def max_profit(prices, start, end) -> float:
        best = 0.0
        smallest_so_far = math.inf
        for i in range(start, end):
            price = prices[i]
            best = max(best, price - smallest_so_far)
            smallest_so_far = min(smallest_so_far, price)
        return best

    best = 0.0
    for i in range(len(prices) + 1):
        profit = max_profit(prices, 0, i) + max_profit(prices, i, len(prices))
        best = max(best, profit)
    return best


def buy_and_sell_stock_twice_best(prices: List[float]) -> float:
    """
    Continuing on 16/3/2022
    Hint: What do you need to know about the first i elements when processing
          the (i+1)th element?

    Ok, the original buy and sell a stock problem worked by iterating over
    the prices, finding the max difference between the minimum value seen so far
    and this value.
    Pseudo code:
    for price in prices:
        best = max(best, price - min_so_far)
        min_so_far = min(min_so_far, price)

    So how can we extend this to being able to buy/sell a stock up to 2 times?
    The hint is 'what do we need to know about the first i elements when
    processing the i+1'th element?'

    In the single buy/sell version, we needed to know the min so far.
    In this version I suppose we need to know the minimum since the last
    sale?
    I still see this way where we do one pass to find the best, then we need to
    find the second best...

    One way to think of this is at each step we have a bunch of options...
    buy, sell, hold, wait (depending on our state)...
    I think we could use a DP approach to find the max value in each position
    depending on a bunch of different options.
    like.. What's the best profit we could have right now if we
    buy
    sell
    hold
    wait
    our constraints are:
    - we can only buy up to two times.
    - we we must finish on sell or wait

    Not sure if we can really represent it with 4 states.  Perhaps we need more
    wait0 (before first buy)
    hold1 (after first buy)
    wait1 (after first sell)
    hold2 (after second buy)
    wait2 (after second sell)

    Those are the states, the actions are 'buy, sell, wait, hold'.
    We have to end in a wait state. When we have just performed either
    a sell or a wait action.

        1, 2, 3, 4, 2, 3, 4, 5, 0, 5
    H1 -1,-1,-1,-1,-1,-1,-1,-1, 0, 0
    W1  X, 1, 2, 3, 1, 2, 3, 4, 4, 5
    H2  X, X,-2,-1, 1, 1, 1, 1, 4, 4
    W2  X, X  X  3, 3, 4, 5, 6, 1, 9
    result = max(5, 9) = 9

    We need to know:
    What's the best profit we could get on each possible state?

    O(n) time, O(1) extra space.  Pretty simple to reason about too.
    It's DP really...
    This took a while, maybe 1.5 hours in this second round.
    I did a bit of a google on this 'dynamic programming state machine' pattern
    and found this page:
    https://www.thealgorists.com/Algo/DynamicProgramming/StateMachineConcept/Fundamentals
    """

    h1, w1, h2, w2 = -math.inf, -math.inf, -math.inf, -math.inf
    for price in prices:
        if h2 > -math.inf:
            w2 = max(w2, price + h2)
        if w1 > -math.inf:
            h2 = max(h2, w1 - price)
        if h1 > -math.inf:
            w1 = max(w1, price + h1)
        h1 = max(h1, 0.0 - price)
    return max(0.0, w1, w2)


def buy_and_sell_stock_twice_failing(prices: List[float]) -> float:
    """
    Start: 7:38
    Write a program that computes the max profit that can be made by buying and selling
    a share at most twice.  The second buy must be made on a date after the first sale.

    Example
    4,5,7,3,5,9,2,4
    Could do it in two passes?
    Find the max profit from buying/selling once, also find the date of the buy/sale
    4,5,7,3,5,9,2,4
                  b s
    p=6
    bi=3
    si=5

    Then, we know the second buy/sell must be before/after this.
    We kind of have two more problems now, which are just the same problem as above...
    4,5,7,
    2,4

    So rough pseudo code for this approach.
    def find_max_profit_and_indices(array, start_idx, end_idx):
        iterate over array from start to end:
            profit is endval - startval
            if this is better than max profit:
                update max profit, buy idx and sell idx
            if profit < 0:
                move buy_idx to here

    find max profit and indices for the best sale
    if buy index > 1 (so there are at least two values)
        find max profit for trade between 0 and buy_idx (not including buy_idx)
    if sell index < len(array) - 2 (so at least two values)
        find max profit for trade between sell_idx + 1 and end of array
    or find max profit of sell and buy inside the range. (could negate the numbers?)
    return sum of first trade and the max of the three potential second trades.

    O(n) two passes
    O(1) space

    Test:
    1,2,3,4,2,3,4,5
    b             s
    max_profit, i1, i2 = 4, 0, 8
    if 0 > 1 -> False
    if 8 < 6 -> False
    if i2-i1 > 2a True
    X,-2,-3,-4,-2,-3,-4,X
             b       s
    p=2
    i1=3
    i2=4
    return 4 + 2 = 6


    Approach 2:
    Keep best and second best
    4,5,7,3,5,9,2,4
    bs


    1,2,3,4,2,3,4,5
    |             | - not best
    |     | |     | - this is the best
    you cant have two buys in a row or two sells in a row

    1,2,3,4,2,3,4,5
    b       s
    best=3
    Due to lack of time I won't explore this further.

    Time about 8:15... had 8 tests passing...
    """

    def max_profit_and_indices(A, start_idx=None, end_idx=None, negate=False):
        if start_idx is None:
            start_idx = 0
        if end_idx is None:
            end_idx = len(A)
        buy_idx = start_idx
        max_profit = 0
        max_profit_buy_idx = -1
        max_profit_sell_idx = -1
        for sell_idx in range(start_idx, end_idx):
            profit = (A[sell_idx] - A[buy_idx]) * (-1 if negate else 1)
            if profit > max_profit:
                max_profit = profit
                max_profit_buy_idx = buy_idx
                max_profit_sell_idx = sell_idx
            if profit < 0:
                buy_idx = sell_idx
        return (
            max_profit * (-1 if negate else 1),
            max_profit_buy_idx,
            max_profit_sell_idx,
        )

    max_p, buy_idx, sell_idx = max_profit_and_indices(prices)
    if buy_idx == -1 or sell_idx == -1:
        return max_p
    p2, _, _ = max_profit_and_indices(prices, 0, buy_idx)
    p3, _, _ = max_profit_and_indices(prices, sell_idx + 1)
    p4, _, _ = max_profit_and_indices(prices, buy_idx + 1, sell_idx, negate=True)
    return max_p + max(p2, p3, p4)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "buy_and_sell_stock_twice.py",
            "buy_and_sell_stock_twice.tsv",
            buy_and_sell_stock_twice,
        )
    )

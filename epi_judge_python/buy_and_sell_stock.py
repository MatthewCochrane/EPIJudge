import math
from typing import List

from test_framework import generic_test


def buy_and_sell_stock_once(prices: List[float]) -> float:
    """
    Return the maximum profit that can be made by buying and selling one share of the stock once.
    Example
    1,2,50,40,20,80,5,10
    b                 s
    ans = 79
    move b when s goes below 1? - this isn't a perfect example for that
    O(n^2) solution is trivial.
    for i, buy in array:
        for j, sell in array[i:]:
            best = max(best, sell - buy)

    Example 2:
    50,90,80,40,85,10
             b     s
    ans = 45
    when s-b < 0, move b to s, because s will be a more optimal starting point for future
    stock values.  That's because s is < b.

    O(n) time solution
    O(1) space
    best_profit starts at 0 so we don't find answers that lose us money
    s and b pointers start at 0
    for each s in the array:
        profit = s - b
        update best profit if profit > best
        if profit < 0:
            move b pointer to s

    All tests passed on first run.  Took about 20 mins.  Nice.
    One note: you ran through the edge cases only after writing the code.
    You should probably come up with edge case examples and run them through
    your pseudo code first instead!

    The way they thought about it in the book was to have a min buy price rather
    than keeping track of the index of the minimum.  This is another way to
    think about it.  Very similar, perhaps slightly better.  See updated code below.
    """
    max_profit = 0
    min_buy = math.inf
    for sell_idx, sell_price in enumerate(prices):
        profit = sell_price - min_buy
        max_profit = max(max_profit, profit)
        min_buy = min(min_buy, sell_price)
    return max_profit


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "buy_and_sell_stock.py", "buy_and_sell_stock.tsv", buy_and_sell_stock_once
        )
    )

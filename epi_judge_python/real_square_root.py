import math

from test_framework import generic_test


def square_root(x: float) -> float:
    """
    Start: 16:26
    Compute the square root of x

    Can we keep guessing?

    sqrt(2)

    numbers <= 1 need to be thought about carefully

    Let's think about this...

    if x < 1

    eg. 0.5
    0 -> 0.5
    0.25*0.25

    if x < 1 then the sqrt is between num and 1



    l=0, r=2
    guess 1
    1*1 < 2? yes, so update left side
    l=1, r=2
    1+2/2 = 1.5
    is 1.5*1.5 < 2 no, so update right side
    l=1,r=1.5
    1.25*1.25 < 2 yes so update left
    l=1.25, r=1.5
    ...
    continue until val*val == x within some tolerance
    math.isclose()


    Pseudo code
    low, high = 0.0, x
    for i in range(1000):
        guess = (low + high) / 2.0
        guess_squared = guess * guess
        if guess_squared < x:
            low = guess
        elif math.is_close(guess_squared, x):
            print(i)
            return guess
        else:
            high = guess
    return -1.0

    time complexity = O(1) because the precision of a float is fixed
    space complexity = O(1)


    Finish: 16:49
    23 mins.
    Bit of a shitshow I probably should have been a bit more careful...

    """

    if x < 0.0:
        raise ArithmeticError
    low, high = (0.0, x) if x >= 1 else (x, 1.0)
    for i in range(100000):
        guess = (low + high) / 2.0
        guess_squared = guess * guess
        if guess_squared < x:
            low = guess
        elif math.isclose(guess_squared, x, rel_tol=0.00000000001):
            print(i)
            return guess
        else:
            high = guess
    return -1


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "real_square_root.py", "real_square_root.tsv", square_root
        )
    )

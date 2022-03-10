from test_framework import generic_test


def power(x: float, y: int) -> float:
    """
    Start: 10:50
    Write a program that takes a double x and an integer y and returns pow(x, y).
    Ignore overflow and underflow.

    Example 1
    2^3 = 8

    Example 2
    3^3 = 27
    3*3 = 9*3 = 27

    Example 3
    5^2 = 25

    So we can just do repeated multiplication.
    Eg. 3^3 = 3*3*3
    This is O(y) time complexity and O(1) space complexity.  Though that assumes that the multiply instruction is O(1).

    Pseudo code
    ans = 1
    repeat y times:
        ans *= 1

    Ok, can we do something tricky here by doing ans * ans until we go over?  That would save a bunch of multiplys..
    Eg.
    Say it's 2^10
    2*2=4 (2^(2*5)) (2^1*2^1)
    4*4=16 (2^2*2^2 = 2^4)
    16*16= (2^4*2^4 = 2^8)
    Break up 10 into smallest number of 'doubles' then we may need some extra multiplies.
    10 -> 0b1010 -> 2^3
    x = x * x 2*2 = 4
    x = x * x 4*4 = 16
    x = x * x 16*16 = 256
    15 - 8 = 7

    2^8 * 2^2
    if it was 2^15 we can do
    2^8 + 2^7
    We already know the answer to 2^7! we worked it out on the way to 2^8.  No we don't
    We know 2^4 and 2^2
    Easiest way to get to 2^7 is 2^8/2
    Or we can use 2^4 + 2^2 + 2^1

    So if we need 2^15 that's
    0b1111
    We clearly need the answers to 2^1, 2^2, 2^4, 2^8

    if exponent is 0, return 1
    ans = x
    multiplies = 1
    while multiplies < exponent:
        ans *= ans
        multiplies <<= 1
    while multiplies < exponent:
        ans *= x
        multiplies += 1
    return ans

    if we had something else, like
    3^6
    3^0b110
    We need 3^4 and 3^2.
    So we want to find the values on the way up...
    so keep squaring the base...
    Every time we do we check if the exponent has a 1 in that position.
    If it does we add to the result.

    # 2 ^ 5
    result = 1 # 32
    tmp = x # 256
    exp_bit = 1 # 0b1000
    while exp_bit < exponent: # 0b1000 < 0b101
        if exp_bit is set in exponent:
            multiply result by tmp
        tmp *= tmp
        shift exp_bit left 1
    return result

    O(number of bits)
    O(1) space

    Finished: 11:43

    Had two bugs
    1. Didn't account for negative exponents.
    2. The while loop exited early, should have used <=
    """
    neg_exp = False
    if y < 0:
        y = -y
        neg_exp = True

    result = 1
    tmp = x
    exp_bit = 1
    # Break the exponent down into it's binary parts.
    # Keep squaring tmp and if that component is in
    # the exponent then multiply the result by tmp.
    # For example if the exponent is 0b101 (5) then
    # the answer is base**4 * base**1.
    # Every time we square base we have an exponent
    # that is a power of two, so we just multiply
    # that part with the rest of the result.
    # Stop when the exp_bit is more than the exponent.
    while exp_bit <= y:
        if exp_bit & y:
            result *= tmp
        tmp *= tmp
        exp_bit <<= 1
    return 1.0 / result if neg_exp else result


if __name__ == "__main__":
    exit(generic_test.generic_test_main("power_x_y.py", "power_x_y.tsv", power))

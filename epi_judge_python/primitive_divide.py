from test_framework import generic_test


def divide(x: int, y: int) -> int:
    """
    To divide two numbers using only addition, subtraction and shifting operators.
    I assume we can use binary and bitwise operators too?  Maybe not...
    We only need to find the quotient, not the remainder.

    Eg 1.
    10 / 2 = 5
    0b1010
    0b0010

    How many times does 2 go into 10?
    We can do repeated subtraction...
    while x > y:
        x -= y
        result += 1
    return result

    This has very poor time complexity O(n) where n is the value of x.  That's O(2^bits) where bits is the number of bits.

    We can probably do long division, or something similar to how we do multiplication...

    For example
    0b1010
    0b0010 /
    ======
    Because the dividend is a power of 1 we a really just doing a shift on the original
             100
    0b11 |0b1100

    So we say
    How many times does 0b11 go into 0b1 ? 0
    How many times does 0b11 go into 0b11 ? 1
    What's left over? 0

    Another
               11
    0b11 | 0b1001
               11
    0b11 goes into 1 - 0
    0b11 goes into 10 - 0
    0b11 goes into 100 - 1 with 1 remainder
    0b11 goes into 11 - 1 time with 0 remainder

    So the idea is: find the largest number we can fit into x
    try fitting y into x, try fitting 2y into x
    try 4y, try... 2^ny and find the largest y

    For example, the one above...
    0b11 does fit into 0b1001
    0b110 does fit into 0b1001
    0b1100 does not fit into 0b1001
    so we use 0b110, and subtract it from
    0b1001
    0b0110 -
    0b0011

    Then we do the same thing with the left over.
    0b0011 / 0b11

    while x:
        shift the denominator until it's larger than the numerator O(n) shifts max where n is number of bits
        shift the denominator back one
        set the bit in result corresponding to the number of times we shifted
        subtract the shifted denominator from the numerator

    The only problem with this is that we keep scanning from left to right to find the right number of shifts.
    We can improve on this by finding the largest number of shifts the first times and decreasing it instead

    shift the denominator until it's larger than the numerator
    while x:
        shift the denominator right until it's smaller than the numerator
        set the bit in result that corresponds to the number of shifts
        subtract the shifted denominator from the numerator

    Example
    0b1111 / 0b101 = 0b11 (15 / 5 = 3)

    shift the denominator until it's larger than the numerator
    0b101, 0b1010, 0b10100 (2 shifts)
    while x: (x = 0b1111)
        shift y right until smaller than x
        0b1010 (now and 1 shift overall)
        set bit in result
        result = 0b10
        subtract 0b1010 from 0b1111 (15 - 10 = 5)
        x = 0b101
    while x: (x=0b101)
        shift y right until smaller than x
        0b1010 -> 0b101 (not 0 shifts overall)
        set bit in result
        result = 0b11
        subtract 0b101 from 0b101 (5 - 5 = 0)
        x = 0
    return 0b11

    Looks good
    Since we scan from right to left then back from left to right once this is O(n) where n is the number of bits.

    """
    set_mask = 1
    result = 0
    # shift the denominator until it's larger than the numerator
    while y <= x:
        y <<= 1
        set_mask <<= 1
    while x:
        # shift the denominator right until it's smaller than the numerator
        while y > x:
            y >>= 1
            set_mask >>= 1
        # set the bit in result that corresponds to the number of shifts
        result |= set_mask
        # subtract the shifted denominator from the numerator
        x -= y
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "primitive_divide.py", "primitive_divide.tsv", divide
        )
    )

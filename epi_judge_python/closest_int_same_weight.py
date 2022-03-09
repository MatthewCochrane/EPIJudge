from test_framework import generic_test


def closest_int_same_bit_count(x: int) -> int:
    """
    Start: 16:21
    Weight is the hamming weight, or the bit count.
    Find an integer y that is as close as possible
    to x, but is not x and has the same weight as x.
    Distracted: 16:39

    Example 1:
        0b1101 -> 13, weight = 3
        0b1110 -> 14, need to flip a 1 to a zero and a zero to a 1

    Example 2:
        0b0000 -> 0, weight = 0
        There is no other number whose weight is 0

    There are
    0 numbers with a weight of 0
    n numbers with a weight of 1
    nCr numbers with a weight of r

    Example 3:
        0b1000 -> 8, weight = 1
        0b0100 -> 4

    Example 4:
        0b1100 -> 12, weight = 2
        0b1010 -> 10

    Example 5:
        0b0100 -> 4, weight = 1
        0b0010 -> 2 This is better...  Better to flip

    Example 6:
        0b0111 -> 7, weight = 3
        0b1011 -> 11

    orig = x
    if bit0 is a 1:
        bitwise not x
    create mask of lsb and next lower bit
    toggle bits in the mask
    if bit0 of x is a 1:
        bitwise not x
    return x

    Test 1:
    0b0010
    orig = 0b0010
    bit0 is a 0 so skip
    mask = 0b0011
    x ^= 0b0011 = 0b0001
    bit0 of x is 0 so skip
    return 0b0001

    Test 2:
    orig = 0b0111
    bit0 is a 1. so x = 0b1000
    mask = 0b1100
    x ^= 0b1101 = 0b0100
    not x = 0b1011
    return 0b1011

    Test 3:
    o = 0b0101
    not = 0b1010
    mask = 0b0011
    toggle = 0b1001
    not = 0b0110
    5 -> 6 nice.

    Time complexity is O(1)
    space complexity is O(1)
    Finish: 17:21
    Not too bad...
    Looks like I did the 'variant' too which is to do it in O(1) space and time.
    In the books solution they iterate over all bits.
    """
    orig = x
    if orig & 1:
        # If the LSB is a 1 then the mask below
        # wouldn't work.  We actually want to
        # perform the same operation then but
        # switching out 1's for zeros.
        # To do this we just invert twice and
        # use the same logic in the middle.
        x = ~x

    # Build a mask of LSB and next lower bit
    # We always want to flip these two bits to
    # get the next closest number with the same
    # hamming weight.
    mask = x ^ (x - 1)
    mask = (mask + 1) >> 1
    mask = mask | (mask >> 1)
    # Toggle the bits in the mask
    x ^= mask

    if orig & 1:
        x = ~x
    return x


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('closest_int_same_weight.py',
                                       'closest_int_same_weight.tsv',
                                       closest_int_same_bit_count))

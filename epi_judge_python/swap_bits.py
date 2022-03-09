from test_framework import generic_test


def swap_bits(x, i, j):
    """
    Swap bits i and j in x.
    Eg.
    i = 2
    j = 4
    x=0b100101
         j i
      0b010001

    i = 1
    j = 4
    x=0b100101
         j  i
      0b000101

    Note that if i and j are the same value then we do nothing.
    If I and j are different then we toggle both i and j.

    Pseudo code
    if bit(i) == bit(j) return x
    otherwise
    toggle bit i
    toggle bit j
    return result

    What if i == j?
    x = 0b0101
    i = 1
    j = 1
    swap 0 with 0, so it's the same value, it has to be.  So do nothing.
    Test pseudo code
    x = 0b0110
    i = 2
    j = 3
    result = 0b1010
    """
    i_mask = 1 << i
    j_mask = 1 << j
    if bool(x & i_mask) == bool(x & j_mask):
        # When the ith and jth bits are the same, swapping them has
        # no effect on the input.
        return x
    # When the ith and jth bits differ, swapping them is equivalent
    # to toggling each bit individually.
    return x ^ (i_mask | j_mask)


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('swap_bits.py', 'swap_bits.tsv',
                                       swap_bits))

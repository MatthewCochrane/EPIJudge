from test_framework import generic_test

bitmasks = [
    0b0101010101010101010101010101010101010101010101010101010101010101,
    0b0011001100110011001100110011001100110011001100110011001100110011,
    0b0000111100001111000011110000111100001111000011110000111100001111,
    0b0000000011111111000000001111111100000000111111110000000011111111,
    0b0000000000000000111111111111111100000000000000001111111111111111,
    0b0000000000000000000000000000000011111111111111111111111111111111,
]

def reverse_bits(x: int) -> int:
    """
    Reverse the bits in x.
    Example:
        x = 0b1101
        res: 0b1011
    Example 2:
        x = 0b0000
        res: 0b0000
    Example 3:
        x = 0b1001
        res: 0b1001
    Example 4:
        x = 0b1100
        res: 0b0011

    mirrors it around the middle.

    Simple approach to do this in O(num bits)
    shift bits out of first and into second
    for i in bits(x):
        set bit bits(x)-i in y to the LSB in x
        left shift a bit out of x

    What other options do we have?
    Is there a divide and conquer approach?
    Like split in half
    0b1101 0100
      11 01  01 00
      1 1  0 1  0 1  0 0
      11  10  10  00
      1011  0010
      00101011
    Something like:
    swap pairs
    swap groups of 2
    swap groups of 4
    etc.
    Each swap takes O(1).  There are n/2 swaps then n/4 then n/8
    sum(n/2 + n/4 + n/8 + ... 1)
    16 -> 8 + 4 + 2 + 1 = 15 ~ n
    So this is still O(number of bits)
    Is there a way to do each of these steps in one operation?
    In that middle step, instead of doing n/2 swaps, can we just do one op?

    swap all pairs of bits in
    0b 11 01 01 00
    build a bitmask like
    0b 00 11 11 00 and xor
    0b11010100
    0b01101010 shift right
    0b10111110 xor
    0b01010101 bitmask
    0b00010100 and
    0b00101000 shift left
    0b00111100 and
    Awesome...  Not too hard.
    The trick is that when we need to do 4's and 8's it's going to be more work.  We would
    have to left shift that many times.  Which means that we go back to O(n) overall.
    Maybe it's different for those ones? It's still pairs, but the pairs aren't next to
    eachother

    0b11 10 10 00
    0b10 11 00 10
    0b11 10
      ab ab
    a = a
    b != b
    0b0101 xor mask that we want to build
    0b1110 1000
    0b0011 1010 shift right (by 2)
    0b1101 0010 xor
    0b0011 0011 bitmask
    0b0001 0010 and
    0b0100 1000 shift left (by 2)
    0b0101 1010 and
    0b1011 0010 xor with original

    Overall pseudo code:
    if > 64 bits raise error
    swapsize = 1
    while swapsize < 64:
        swap swapsize
        double the swapsize

    to swap:
        shift right by swapsize
        xor with orig
        create bitmask based on swapsize (eg. 010101 for swapsize 1, 001100110011 for swapsize 2, etc.)
        and with bitmask
        shift left by swapsize
        or with previous
        xor the mask with the original

    Simple example
    0b1011 -> 0b1101

    while swapsize < 4 (only a 4 bit number not 64 bit)
        x = swap(x, 1)...
            1011 orig
            0101 shift right
            1110 xor
            0101 bitmask
            0100 and
            1000 shift left
            1100 or
            0111 xor with orig
        ...
        x = swap(x, 2)
            0111 orig
            0001 shift right (by 2)
            0110 xor
            0011 bitmask
            0010 and
            1000 shift left by 2
            1010 or
            1101 xor with original
        return x == 1101
    Each iteration is O(1) work.  So overall we have O(log n).  Really, for 64 bits you can see that this takes
    a similar amount of time as the shifting approach.  We can analyse the number of instructions.  Or look at
    the hardware and see if there are ways to optimise or pipeline.

    Cool to try a couple of different approaches here.  One interesting note is that
    there are a lot of ways to do this.  I only considered two. My search went something like

    State the question. (about a minute)
    Draw up a bunch of different examples and calculate their result.
    (a few mins)
    Explain, and pseudo code for naive solution. (a few mins)


    """
    # Naive approach.  9us average running time 8us median.
    # ans = 0
    # for i in range(64):
    #     if x & 1:
    #         ans |= (1 << (64 - i - 1))
    #     x >>= 1
    # return ans

    # This approach takes 3us running time, and 3us median.
    # So three times faster than the naive approach above.
    if x > 1 << 63:
        raise ArithmeticError
    swap_size = 1
    log2_swap_size = 0
    while swap_size < 64:
        # Swap every swap_size'th bit with each other.
        # Eg. if swap_size is 1, swap each bit with it's neighbour
        #     or if sway_size is 2, swap each bit with the bit two to it's right
        tmp = x >> swap_size
        tmp ^= x
        bitmask = bitmasks[log2_swap_size]
        tmp &= bitmask
        # select both bits in each pair that requires a swap
        tmp |= tmp << swap_size
        x ^= tmp

        swap_size *= 2
        log2_swap_size += 1
    return x


if __name__ == "__main__":
    # print(reverse_bits(0b1101))
    # exit()
    exit(
        generic_test.generic_test_main(
            "reverse_bits.py", "reverse_bits.tsv", reverse_bits
        )
    )

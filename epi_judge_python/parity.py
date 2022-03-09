import sys

from test_framework import generic_test


def parity(x: int) -> int:
    """
    Usually we say that data has an even parity or an odd parity.
    Even parity is represented as false and represents the number of set bits being even.
    Odd parity is represented as true and represents the number of set bits being odd.
    To calculate this we can count the number of 1's then return the result modulo 2.
    This would take O(number of bits) time and O(log number of bits) space.  In reality it's O(1) space and O(1) time
    for fixed sized integers.

    Pseudo code...

    count number of bits
    return count modulo 2 as a boolean

    Example
    0b110
    2%2 = 0 -> false -> even

    In python...
    This has a time complexity of O(number of bits)
    Has a space complexity of O(log number of bits)
    It may be useful to think of fixed sized integers even though that's not the case in python.
    In that case we have O(1) time and O(1) space.

    Is that even true?  If there's not a fixed integer size, then what happens to an algo that does a shift
    every time the shift is done?  Probably it's O(n) space to do the shift.  Actually, even worse than that
    it's probably O(n) time to do the shift.  If you have a massive number that only fits into 10^6 bits, then
    if you wanted to do a shift right it would take O(n) time, ie the number of operations is proportional to the
    number of bits.  For fixed size integers we have O(1) time operations because they're built in hardware, but
    fundamentally, if you want to do an operation on an unbound input size, it will take time proportional to that
    size.
    So technically this is O(n^2) where n is the number of bits.
    That's because we do something like:
    for each bit:
        if LSB, increment count
        shift right by 1

    the shift is O(n), and we do it for each bit, so O(n^2) total time complexity.

    Which again leads me to thinking that the best way to think about this is as if the integers were of a fixed
    size, even if that's not necessarily true.  By 'this' I mean these bit manipulation questions.

    Can we improve on this?
    We can't really improve the time complexity.  Perhaps we could do O(number of set bits)
    Should we bother improving it otherwise?
    For large integers, which is very uncommon, we could improve the time complexity by
    breaking it up into smaller integers and counting the number of bits in each.  That
    would make the result O(n) time where n is the number of bits because we avoid the O(n) right shift operator.

    If we think of it as operating on fixed sized integers then we can't improve the time complexity because it's
    already O(1).  But we can make it noticeably faster.  Honestly, you'd get a better speed up calling to some c
    code to do something like count bits.

    Another approach is to 'fold' the count down with xors.  When we calculate the parity we only care about if it's
    0 or 1.  So we just effectively want to xor all the bits together.  We can do up to n/2 bits in parallel.
    eg.
    0b1110
       |
    xor
    0b11
    0b10
    0b01

    Then we split that and xor
    0b0
    0b1
    0b1
    so the overall parity is 1 -> odd

    Pseudo code for this:
    Do until we have one bit left
        split in two
        shift the left bits to the right by the width in each part
        xor the two parts
    return the LSB

    References:
        I'd like to read through this... Only 6000 lines xD
        https://github.com/python/cpython/blob/main/Objects/longobject.c
        This would be worth watching too
        https://www.youtube.com/watch?v=zhvnyGd0n8Q
        Difference between logical, arithmetic and rotate shifts:
        https://stackoverflow.com/a/44695162/988717
    """
    # 0b0000|0101
    # 0b000001|01
    # 0b0000000|0 -> 0
    assert x < sys.maxsize
    x ^= x >> 32
    x ^= x >> 16
    x ^= x >> 8
    x ^= x >> 4
    x ^= x >> 2
    x ^= x >> 1
    return bool(x & 1)


if __name__ == '__main__':
    exit(generic_test.generic_test_main('parity.py', 'parity.tsv', parity))

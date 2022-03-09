from test_framework import generic_test


def count_bits(x: int) -> int:
    """
    Count the set bits in x.
    eg. 1001 has 2 set bits
    Keep shifting and testing
    This has a time complexity of O(num bits)
    This has a space complexity of O(1)
    How could we improve this?
    There could be an instruction to count the bits.  How could we use that in python?
    That would be O(1) time.  But probably isn't portable.  And I don't even know how you'd do that in python.
    If we were talking about C, C++ or some lower level language and had some specific hardware architecture in
    mind then I would think more about this.
    We can use the bit hack that flips the LSB.  Repeat that until we have zero.
    That would be O(num set bits) time

    The pseudo code for the improved approach with the bit hack is:
    while x:
        Add 1 to result
        flip the LSB
    return result

    What's the bit hack?
    Remember that if we take x and subtract 1, we clear the LSB and set all lower bits.
    eg.
    110010100000 - 1
    110010011111
    Conversely, adding 1 to this would flip all the 1's back to 0's and set the next bit.
    Now, if we and them together
    110010100000 - 1
    110010011111
    110010000000

    x = x & (x-1)

    0b110
    0b101 - 1
    0b100 &
    0b011 - 1
    0b000
    """
    result = 0
    while x:
        result += 1
        x = x & (x - 1)
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('count_bits.py', 'count_bits.tsv',
                                       count_bits))

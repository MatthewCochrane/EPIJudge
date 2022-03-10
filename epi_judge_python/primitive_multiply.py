from test_framework import generic_test


def multiply(x: int, y: int) -> int:
    """
    Start: 20:45
    Write a function to multiply two numbers.
    Allowed instructions:
    assignment
    >>, <<, |, &, ~, ^
    ==
    So you can't use addition, subtraction, multiplication, etc.
    You can use loops.  But how can you use loops if you can't use addition or lt / gt?

    How do we multiply two numbers?

    Example 1
    3*4 = 12
    0b0011
    0b0100
    ======
    0b1100

    Example 2
    3*2 = 6
    0b0011
    0b0010
    ======
    0b0110

    So multiplying by a power of two is a shift of the original number

    Example 3
    3 * 3 = 9
    0b0011
    0b0011
    ======
    0b1001

    Intuitively this is

    0b0011
    0b0001 *
    ------
    0b0011
    Plus
    0b0011
    0b0010 *
    ------
    0b0110

    so
    0b0011
    0b0110 +
    ======
    0b1001

    Ok.  But we're not allowed to use addition!
    Which means we need to implement addition in bitwise operators as well!

    Let's summarise this part, then we can build an adder.

    to multiply a * b
    result = 0
    while b:
        if b & 1:
            result = add(result, a)
        a <<= 1
        b >>= 1
    return result

    This is O(bits in b * complexity of add)

    Adder:
    To add two numbers

    Ex 1
    3 + 4 = 7
    0b011
    0b100 +
    0b111

    Ex 2
    7 + 7 = 14
    0b0111
    0b0111 +
    0b1110

    You can't really do addition in less than O(n)

    Carry is true if 2 or more are 1
    a b c res
    0 0 0 0
    0 0 1 0
    0 1 0 0
    0 1 1 1
    1 0 0 0
    1 0 1 1
    1 1 0 1
    1 1 1 1

    if (a & b) | (b & c) | (a & c)

    Basically
    a + b
    mask = 1
    result = 0
    carry = 0
    while a | b | carry:
        # boolean operators
        result |= (a & mask) ^ (b & mask) ^ carry
        carry = (a & b) | (b & c) | (a & c)
        a >>= 1
        b >>= 1
        mask <<= 1
    return result



    Overall time complexity is O(n^2)
    Overall space complexity is O(1)
    Can we improve on this?
    Yes, if we can use a hardware adder.  It would drop to O(n).

    Passed all tests at 21:27

    """
    def add(a: int, b: int) -> int:
        mask = 1
        result = 0
        carry = 0
        while a or b or carry:
            a_bit = bool(a & 1)
            b_bit = bool(b & 1)
            bit = a_bit ^ b_bit ^ carry
            if bit:
                result |= mask
            carry = (a_bit and b_bit) or (a_bit and carry) or (b_bit and carry)
            a >>= 1
            b >>= 1
            mask <<= 1
        return result

    result = 0
    while y:
        if y & 1:
            result = add(result, x)
        x <<= 1
        y >>= 1
    return result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('primitive_multiply.py',
                                       'primitive_multiply.tsv', multiply))

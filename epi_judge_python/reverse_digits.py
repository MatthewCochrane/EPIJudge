from test_framework import generic_test


def reverse(x: int) -> int:
    """
    Start: 12:20
    Returns the integer corresponding to the digits in reverse order.

    Example 1:
    123 -> 321

    Example 2:
    -12 -> -21

    Example 3:
    100 -> 1

    We can convert to a string, then reverse, then convert to an int.
    they didn't say anything about not using strings...

    pseudo code:
    if negative, remember and negate
    convert x to string
    reverse string
    convert string to int
    if original was negative, negate

    O(digits) time
    O(digits) space

    Time: 12:27
    """
    tmp = -x if x < 0 else x
    result = int(str(tmp)[::-1])
    return -result if x < 0 else result


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('reverse_digits.py',
                                       'reverse_digits.tsv', reverse))

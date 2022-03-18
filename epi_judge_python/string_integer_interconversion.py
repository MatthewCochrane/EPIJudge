from test_framework import generic_test
from test_framework.test_failure import TestFailure

# Start time: 11:14
# End time: 11:37
# A reasonable amount in this question though it's not that hard...
# Need to remember ord and chr functions a little better, I think the IDE helped me with these
# Also, they had a '+' prepended to some values, not sure why they didn't mention that in the question...
# There could have been a heap of other error cases to check.


def int_to_string(x: int) -> str:
    """
    Examples:
        123 -> "123"
        -22 -> "-22"

    Pseudo code
    check if negative and take abs, store sign
    keep 'shifting' and taking the least significant digit appending it as a character to a list
    if negative, push the negative sign to the list
    reverse the list
    join list into string and return
    O(digits) time
    O(digits) space -> can't really do better because the result is immutable we can't update it only set it once.
    """
    if x == 0:
        return "0"
    is_negative = x < 0
    x = abs(x)
    converted = []
    while x:
        digit = x % 10
        x //= 10
        converted.append(chr(ord("0") + digit))
    if is_negative:
        converted.append("-")
    converted.reverse()
    return "".join(converted)


def string_to_int(s: str) -> int:
    """
    Examples
        "123" -> 123
        "-82" -> -82
        "0" -> 0
        "" -> error

    Pseudo code
    multiplier = 1
    result = 0
    from right to left:
        if val = '-':
            result *= -1
        result += multiplier * get_digit(val)
        multiplier *= 10
    return result
    O(digits) time -> O(log n) time
    O(1) space

    They're solution is pretty nice.  Instead of going from right to left they go from left to right
    """
    # The left to right approach which is a bit simpler
    # result = 0
    # for i in range(len(s)):
    #     if s[i] == "+":
    #         continue
    #     if s[i] == "-":
    #         continue
    #     digit = ord(s[i]) - ord("0")
    #     result = result * 10 + digit
    # return result * (-1 if s[0] == "-" else 1)

    multiplier = 1
    result = 0
    for i in reversed(range(len(s))):
        # check that s[i] is - or 0->9
        if s[i] == "+":
            break
        if s[i] == "-":
            result *= -1
            break
        digit = ord(s[i]) - ord("0")
        result += multiplier * digit
        multiplier *= 10
    return result


def wrapper(x, s):
    if int(int_to_string(x)) != x:
        raise TestFailure("Int to string conversion failed")
    if string_to_int(s) != x:
        raise TestFailure("String to int conversion failed")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "string_integer_interconversion.py",
            "string_integer_interconversion.tsv",
            wrapper,
        )
    )

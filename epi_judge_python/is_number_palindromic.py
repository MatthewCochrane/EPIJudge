from test_framework import generic_test


def is_palindrome_number(x: int) -> bool:
    """
    Start: 12:32
    Can we do this without converting to a string?

    Example 1:
    0 -> true

    Example 2:
    -1 -> false

    Example 3:
    12321 -> true

    Example 4:
    1221 -> true

    Example 5:
    -431 -> false

    Example 6:
    100 -> false

    Looks like all negative numbers are not palindromes because of the negative sign.

    So we can determine what the digits are by dividing by 10 and taking the remainder.
    1221 % 10 = 1
    1221 // 10 = 122
    122 % 10 = 2
    122 // 10 = 12
    12 % 10 = 2
    12 // 10 = 1
    1 % 10 = 1
    1 // 10 = 0

    That's good but it requires O(n) space and it's really just converting it into a string
    ourselves.
    How can we do this from both sides at the same time?
    Like, how can we determine the most significant digit?

    1221 % 1000 = 221
    (1221 - 221) / 1000
    221 % 100 = 21
    (221 - 21) / 100 = 2
    21 % 10 = 1
    (21 - 1) / 10 = 2

    But how do we know what the most significant digit is?
    1221 // 10 = 100 * 10 = 1000

    1000 // 10 = 100 * 10 = 1000

    Ok, so lets try that

    find the starting modulo
    while the modulo > 0:
        determine left remainder and left digit
        l_digit = (l_rem - (l_rem % modulo)) / modulo
        l_rem = l_rem % modulo
        modulo //= 10
        determine right remainder and right digit
        r_digit = x % 10
        x = x // 10
        if left and right digits are not equal, return False
    return True

    212
    modulo = 1
    while modulo <= x: 1000 < 212
        modulo *= 10
    modulo //= 10 100
    l_rem = x
    while modulo > 0... 100 > 0
        l_digit = (212 - (212 % 100)) / 100 = 212-12/100 = 200 / 100 = 2
        l_rem = 212 % 100 = 12
        modulo //= 10 = 10
        r_digit = 212 % 10 = 2
        x //= 10 = 21
        l_digit == rdigit (2 == 2)
    while modulo > 0... 10 > 0
        l_digit = (12 - (12 % 10)) / 10 = 1
        l_rem = 12 % 10 = 2
        modulo //= 10 = 1
        r_digit = 21 % 10 = 1
        x //= 10 = 2
        l_digit == r_digit (1 == 1)
    Would be nice to exit now...

    change the modulo thing...
    iterations = 1
    modulo = 1
    while modulo <= x: # 1000 <= 212, its = 4
        modulo *= 10
        iterations += 1
    modulo //= 10
    # ensure we always check for overlap on the middle character
    # if we have an odd length by not subtracting 1 from its here.
    its //= 2
    while iterations:
        determine left remainder and left digit
        l_digit = (l_rem - (l_rem % modulo)) / modulo
        l_rem = l_rem % modulo
        modulo //= 10
        determine right remainder and right digit
        r_digit = x % 10
        x = x // 10
        if left and right digits are not equal, return False
        iterations -= 1

    Time complexity: O(n) where n is number of digits
    Space complexity: O(1)

    Finish time: 13:09 ~ 37 mins.  Still too slow...
    But again, good work, everything worked!
    Ok, actually had a bug.  I forgot to add a line of code to 'shift' the modulo.
    Finish: 13:15

    Notes from reading the answer:
    Maybe I could have just used log.  I didn't because I felt in these problems they don't want you to use
    shortcut functions.  That makes no sense when I think about it though.  They never said not to use certain
    functions.
    """
    if x < 0:
        return False
    if x == 0:
        return True
    iterations = 1
    modulo = 1
    while modulo <= x: # 100000 <= 74447, its = 6
        modulo *= 10
        iterations += 1
    modulo //= 10 # 10000
    # ensure we always check for overlap on the middle character
    # if we have an odd length by not subtracting 1 from its here.
    iterations //= 2 # 6//2 = 3
    left_remainder = x
    while iterations:
        left_digit = (left_remainder - (left_remainder % modulo)) // modulo
        left_remainder %= modulo
        modulo //= 10
        right_digit = x % 10
        x //= 10
        if left_digit != right_digit:
            return False
        iterations -= 1
    return True


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_number_palindromic.py",
            "is_number_palindromic.tsv",
            is_palindrome_number,
        )
    )

from typing import List

from test_framework import generic_test


def plus_one(A: List[int]) -> List[int]:
    """
    Start: 15:30
    Array of digits encoding a non-negative decimal integer and updates the array to
    represent D + 1

    Example
        in: [1,2,9]
        out: [1,3,0]

    Example
        [1]
        [2]

    Example
        [9]
        [1,0]

    Example
        [9,9,9]
        [1,0,0,0]

    This is really just building a decimal adder.
    We can do this in O(n) time and O(1) space.
    result = copy of input reversed
    for each index in result
        increment the digit
        set result value to new value mod 10
        if the digit is < 10 we break, plus set a flag
    if not flag:
        add a '1' to the result
    return reversed result
    O(n) time
    O(1) space unless we reverse with a copy...

    Finished: 15:52
    Pretty good...  Very easy question.

    Had one bug.  I didn't reverse the result I just copied it.  Weird, don't know why I did that.
    Also, I learned that you can reverse in place with array.reverse()
    """
    result = A[::-1]
    final_carry = True
    for i, val in enumerate(result):
        incremented = val + 1
        result[i] = incremented % 10
        if incremented < 10:
            final_carry = False
            break
    if final_carry:
        result.append(1)
    result.reverse()
    return result



if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('int_as_array_increment.py',
                                       'int_as_array_increment.tsv', plus_one))

from typing import List

from test_framework import generic_test


def multiply(num1: List[int], num2: List[int]) -> List[int]:
    """
    Start: 16:00
    Multiply the digits in two arrays

    Example
        [3], [4]
        result: [1,2]

    Example
        [1,2,3], [2,3,4]
        result:
          2
        1 2 3
        2 3 4 x
        -------
            2
        4 * 123 + 30 * 123 + 200 * 123
        Result:
        4*3 + 4*20 + 4*100
        30*3 + 30*20 + 30*100
        200*3 + 200*20 + 200*100

        4e0*3e0 + 4e0*2e1 + 4e0*1e2
        3e1*3e0 + 3e1*2e1 + 3e1*1e2
        2e2*3e0 + 2e2*2e1 + 2e2*1e2

        4*3 = 12, esum = 0 so we update result starting at index 0
        [2, 1]
        4*2 = 8, esum = 1 so we update result at idx 1
        [2, 9]
        4*1 = 4, esum = 2 so update result at idx 2
        [2,9,4]
        3*3 = 9, esum = 1
        [2,8,5]
        3*2 = 6, esum = 2
        [2,8,7]
        3*1 = 3, esum = 3
        [2,8,7,3]
        2*3 = 6, esum = 2
        [2,8,3,4]
        2*2 = 4, esum = 3
        [2,8,3,8]
        2*1 = 2, esum = 4
        [2,8,3,8,2]
        reverse = [2,8,3,8,2]

        it can overflow.  so we need to carry here
        need to build the 'add' function too then

        O(n*m*(n+m))

        Keep track of negative numbers separately..  Strip them out then add back at end

        Pseudo code:
        result is negative if only one number is negative
        strip out negatives
        result = []
        for i, digit1 in num1:
            for j, digit2 in num2:
                prod = digit1*digit2
                add(result, prod, i+j)
        reverse result
        return result

        [1,2,7,9,9]
        add(x, 11, 2)
        [1,2,7+11,9,9]
        [1,2,18,9,9]
        [1,2,8,10,9]
        [1,2,8,0,10,9]
        [1,2,8,0,0,1]

        [1]
        add(x, 5, 5)
        [1,0,0,0,0,5]

        add_to_reversed(rev_num: List[int], val: int, offset: int) -> None:
            "Updates num in place."
            if offset is past array len, pad with zeros up to offset
            add val at offset
            while value at offset > 10
                update to mod 10
                if value > 10:
                    offset += 1
                    add zero to array if off end of array
                    add value // 10 to value at new offset
    Finished: 17:01
    I had a bug: i passed i + j into add_reversed, but that was their
    array offset, not their number of zeros.  I needed len-i-1 instead.
    Also missed some edge cases around zeros.  I should have
    drawn up more cases around that.  I didn't in the interest of time.

    """
    # [8]
    # [1,5]
    result_negative = (num1[0] < 0) ^ (num2[0] < 0)
    num1[0], num2[0] = abs(num1[0]), abs(num2[0])

    def add_to_reversed_array(rev_num: List[int], val: int, offset: int) -> None:
        """
        Updates rev_num in place.
        rev_num is an array representing a reversed number
        """
        if val == 0:
            return
        while len(rev_num) <= offset:
            rev_num.append(0)
        rev_num[offset] += val
        while (last_val := rev_num[offset]) >= 10:
            rev_num[offset] %= 10
            offset += 1
            if offset >= len(rev_num):
                rev_num.append(0)
            rev_num[offset] += last_val // 10

    result = [0]
    for i, digit1 in enumerate(num1):
        for j, digit2 in enumerate(num2):
            add_to_reversed_array(
                result, digit1 * digit2, (len(num1) - i - 1) + (len(num2) - j - 1)
            )
    result.reverse()
    if result_negative and result:
        result[0] *= -1
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "int_as_array_multiply.py", "int_as_array_multiply.tsv", multiply
        )
    )

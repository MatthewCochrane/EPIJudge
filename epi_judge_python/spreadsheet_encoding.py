import functools

from test_framework import generic_test


def ss_decode_col_id(col: str) -> int:
    """
    Start: 13:10
    Convert the spreadsheet column id into an integer.

    Examples
        A  -> 1
        B  -> 2
        Z  -> 26
        AA -> 27

    It's like base 26 but there's no 0?

    AA -> 1*26 + 1 = 27
    BA -> 2*26 + 1
    Z = 26

    Testing...
    generate the first 100 or 1000 column ids then convert them back
    generating:

    Wrote test code

    AAA
    26*26*1 + 26*1 + 1
    ZZ
    26*26 + 26

    Pseudo code
    result = 0
    for each item:
        multiply by 26
        add char number
    return result

    O(n) time where n is length of string
    O(1) space

    What a weird problem.  This number system confuses me a lot!

    """
    # After seeing their solution I rewrote it with reduce.
    return functools.reduce(lambda p, c: p * 26 + (ord(c) - ord("A") + 1), col, 0)
    # My solution
    # result = 0
    # for c in col:
    #     result *= 26
    #     result += ord(c.upper()) - ord("A") + 1
    # return result


def gen_codes(n):
    digits = [0]
    for i in range(n):
        j = 0
        digits[j] += 1
        while digits[j] > 26:
            digits[j] = 1
            j += 1
            if j == len(digits):
                digits.append(0)
            digits[j] += 1
        yield "".join(chr(ord("A") + c - 1) for c in reversed(digits))


if __name__ == "__main__":
    # for ii, code in enumerate(gen_codes(3000)):
    #     assert ii + 1 == ss_decode_col_id(
    #         code
    #     ), f"{ii+1} != {ss_decode_col_id(code)} for '{code}'"
    # exit()

    exit(
        generic_test.generic_test_main(
            "spreadsheet_encoding.py", "spreadsheet_encoding.tsv", ss_decode_col_id
        )
    )

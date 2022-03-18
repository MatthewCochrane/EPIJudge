import itertools

from test_framework import generic_test
from test_framework.test_failure import TestFailure

# Start: 21:15
# Finish: 21:26
# Not too difficult, similar to some other questions.


def decoding(s: str) -> str:
    """
    while not end:
        read number
        read letter
        append n of letter
    join result
    """
    res = []
    num = 0
    for c in s:
        if c.isnumeric():
            num *= 10
            num += int(c)
        else:
            res.append(c * num)
            num = 0
    return "".join(res)


def encoding(s: str) -> str:
    """
    aaaabcccaa
    4a1b3c2a

    aaaaaaaaaaabb
    11a2b

    count in each group and add
    for c, it groupby(s):
        res.append(len(it))
        res.append(c)
    to string
    """
    res = []
    for c, group in itertools.groupby(s):
        res.append(str(len(list(group))) + c)
    return "".join(res)


def rle_tester(encoded, decoded):
    if decoding(encoded) != decoded:
        raise TestFailure("Decoding failed")
    if encoding(decoded) != encoded:
        raise TestFailure("Encoding failed")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "run_length_compression.py", "run_length_compression.tsv", rle_tester
        )
    )

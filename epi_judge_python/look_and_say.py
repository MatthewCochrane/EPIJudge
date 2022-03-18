import itertools

from test_framework import generic_test


def look_and_say(n: int) -> str:
    """
    start: 17:02

    1
    11
    21
    1211
    111221
    312211
    13112221
    1113213211
    31131211131221
    13211311123113112211

    One approach is what I'm doing here...
    start with "1" then transition from that to the next look and see answer n-1 times.
    we can group the digits at each step
    The time complexity is very hard to understand, it's O(n^2)?

    Pseudo code
    def next_look_and_say(seq: str) -> str:
        iterate over seq in groups of the same character
        append the qty and the character to the result
    seq = "1"
    for i in range(n-1):
        seq = next_look_and_say(seq)
    return seq

    """

    def next_look_and_say(seq: str) -> str:
        # Or a very nice way to write this function using groupby
        # return "".join(str(len(list(group))) + c for c, group in itertools.groupby(seq))
        res = []
        for c in seq:
            if not res or res[-1][1] != c:
                res.append([0, c])
            res[-1][0] += 1
        return "".join(str(v) for group in res for v in group)

    seq = "1"
    for _ in range(n - 1):
        seq = next_look_and_say(seq)
    return seq


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "look_and_say.py", "look_and_say.tsv", look_and_say
        )
    )

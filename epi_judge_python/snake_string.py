from test_framework import generic_test


def snake_string(s: str) -> str:
    """
    phase = +1, period = 4
    mid is period 2, phase 0
    lower is period 4, phase 3

    start at 1, step 4 while we are still in the string
        add char to result
    start at 0, step 2, while we are still in the string
        add char to result
    start at 3, step 4, while still in the string
        add char to result

    Very easy question
    """
    # Better solution using slices.  Nice.
    # return s[1::4] + s[::2] + s[3::4]
    result = []
    for i in range(1, len(s), 4):
        result.append(s[i])
    for i in range(0, len(s), 2):
        result.append(s[i])
    for i in range(3, len(s), 4):
        result.append(s[i])
    return "".join(result)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "snake_string.py", "snake_string.tsv", snake_string
        )
    )

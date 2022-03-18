from typing import List

from test_framework import generic_test


def generate_pascal_triangle(n: int) -> List[List[int]]:
    """
    Start: 10:45
    Calculate the first n rows of pascal's triangle.  I believe these are also binomial coefficients.
    So the formula n choose k = n!/k!(n-k)! gives the value of any element in the triangle (row/col)

    1
    1 1
    1 2 1
    1 3 3 1
    1 4 5 6 1

    to compute the next row
    each value in row n is that value and the one before it in row n-1
    if the index is < 0 or > n-1 then use a 0

    O(n^2) O(sum(1->n)) = O(n(n+1)/2) = O(n^2)
    O(1) space (not including the result, otherwise O(n^2) space)

    pseudo code
    return empty array if n < 1
    add first row to result [1]
    for each row from 1 up to n:
        build a row
        for each value up to the row number
            prev_val = prev_row[index - 1] if index > 0 else 0
            cur_val = prev_row[index] if index < len(prev_row) else 0
            append(prev_val + cur_val)
    return result

    Finished: 10:58 - about 15 mins.  Pretty easy question.
    The way they did it in the answer was:
    set all values to 1
    only compute the middle values.
    """

    # Second approach
    # result = [[1] * (i + 1) for i in range(n)]
    # for r in range(1, n):
    #     for c in range(1, r):
    #         result[r][c] = result[r - 1][c - 1] + result[r - 1][c]
    # return result

    if n < 1:
        return []
    result = [[1]]
    for r in range(1, n):
        row = []
        prev_row = result[-1]
        for i in range(r + 1):
            prev_val = prev_row[i - 1] if i > 0 else 0
            cur_val = prev_row[i] if i < len(prev_row) else 0
            row.append(prev_val + cur_val)
        result.append(row)
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "pascal_triangle.py", "pascal_triangle.tsv", generate_pascal_triangle
        )
    )

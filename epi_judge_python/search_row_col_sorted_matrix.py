from typing import List

from test_framework import generic_test


def matrix_search(A: List[List[int]], x: int) -> bool:
    """
    sqrt(n^2+m^2)*(log m*n)
    m*log2m
    can do it O(m+n)

    I tried thinking about this for like 40 mins and got nowhere.
    I was pretty sure I remembered an O(n+m) solution but I couldn't see it.

    Turns out there is one but I kept shooting myself in the foot.

    The problem is to do it in n + m you have to start in a corner that's the minimum in one
    dimension and the maximum in the other.
    If you start in the other two corners where it's the min/max in both dimensions then you
    can't eliminate either row or column...

    If you start in a corner that's min in one and max in the other dimension then you can eliminate
    a whole row or column every step.

    In a way that's because all items in the row (say to the right) are > the value
    and all items in the column (say above) are < the value
    If you flatten that out you can only move in one direction, toward smaller or larger numbers.
    Every time you do you eliminate a row or column.
    I the worst case you traverse half the perimeter.

    pseudo code

    rows, cols = len(A), len(A[0])
    r, c = rows-1, 0
    while r >= 0 and c < cols: and
        if A[r][c] < x:
            # everything above is also < x -> step to the right
            c += 1
        elif A[r][c] == x:
            return True
        else:
            r -= 1
    return False

    All

    """
    rows, cols = len(A), len(A[0])
    r, c = rows - 1, 0
    while r >= 0 and c < cols:
        if A[r][c] == x:
            return True
        elif A[r][c] < x:
            # everything above is also < x -> step to the right
            c += 1
        else:
            # everything to the right is also > x -> step up
            r -= 1
    return False


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "search_row_col_sorted_matrix.py",
            "search_row_col_sorted_matrix.tsv",
            matrix_search,
        )
    )

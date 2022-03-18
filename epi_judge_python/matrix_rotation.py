from typing import List

from test_framework import generic_test


def rotate_matrix(square_matrix: List[List[int]]) -> None:
    """
    Start: 10:14
    Rotation

    1 2 3  ->  7 4 1
    4 5 6  ->  8 5 2
    7 8 9  ->  9 6 3

    Can do in O(n) space, O(n) time if we just read columns into rows.

    Matrix operations

    transpose then flip

    1 2 3 -> 1 4 7 -> 7 4 1
    4 5 6 -> 2 5 8 -> 8 5 2
    7 8 9 -> 3 6 9 -> 9 6 3

    O(1) space, O(n) time though two passes...

    Pseudo code
    transpose in place
    flip/mirror in place

    def transpose in place:
        for r in range rows:
            for c in range(r, cols):
                swap [r][c] and [c][r]

      l   r
    # 7 4 1
    def flip:
        cl, cr = 0, len-1
        while cl < cr:
            for every row as r:
                swap [r][cl] with [r][cr]
            increment cl, decrement cr

    All tests passed on first go.
    Finish: 10:36 about 20 mins.  Nice :)  Helps when you've seen the question before haha.
    """

    def transpose(mat: List[List[int]]) -> None:
        "Transpose square matrix in place"
        n = len(mat)
        for r in range(n):
            for c in range(r, n):
                mat[r][c], mat[c][r] = mat[c][r], mat[r][c]

    def mirror(mat: List[List[int]]) -> None:
        "Mirror square matrix in place"
        n = len(mat)
        col_l, col_r = 0, n - 1
        while col_l < col_r:
            for row in mat:
                row[col_l], row[col_r] = row[col_r], row[col_l]
            col_l += 1
            col_r -= 1

    transpose(square_matrix)
    mirror(square_matrix)


def rotate_matrix_wrapper(square_matrix):
    rotate_matrix(square_matrix)
    return square_matrix


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "matrix_rotation.py", "matrix_rotation.tsv", rotate_matrix_wrapper
        )
    )

from typing import List

from test_framework import generic_test


def n_queens(n: int) -> List[List[int]]:
    """
    Start: 6:45

    Place n queens on a chessboard so that no to queens can
    attack eachother.

    Return the board positions like
    [".Q..", "...Q", "Q...", "..Q."]


    Examples
    N = 1
        Q

    N = 2
        ..
        ..
        There is no solution.  Two queens placed anywhere could attack.

    N = 3
        ...
        ...
        ...
        There is no solution
    N = 4
        ..Q.
        Q...
        ...Q
        .Q..

        .Q..
        ...Q
        Q...
        ..Q.
        Two solutions

    N = 5
        Q....
        ...Q.
        .....
        .....
        .....

    Things we know:
    - there can only be one queen per row
    - there can only be one queen per column
    - there can only be one queen per diagonal

    We probably want a fast way to lookup if there's a queen in a column
    or diagonal!

    row constraint is easy, just try one queen per row...



    diags
    0123
    1234
    2345
    3456
    easy way to determin the diag we're on?
    if we were in row 0 col 2, answer is 2
    if we were in row 2 col 3, answer is 5
    so it's just `row + col`.
    diag = row + col

    anti-diags
      0123

    0 3456
    1 2345
    2 1234
    3 0123

    adiag = row + n-col
    row 1, col 2
    1 + 4-1 = 1 + 3 = 4
    solutions: List[List[str]] = []
    solution: List[str] = []
    cols_with_queen = [False] * n
    diags_with_queen = [False] * (2*n - 1)
    adiags_with_queen = [False] * (2*n - 1)
    def find_solutions(row_idx):
        for each of the columns in that row:
            diag = row + col
            adiag = row + n - col

            if there is no queen in that column yet and no ldiag and no rdiag:
                solution.append("Q....")
                if len(solution) == n:
                    copy solution to solutions
                else:
                    cols_with_queen[col] = True
                    diags.add(ldiag)
                    adiags.add(rdiag)
                    find_solutions(row_idx + 1)
                    adiags.remove(rdiag)
                    diags.remove(ldiag)
                    cols_with_queen[col] = False
                solution.pop()
    find_solutions(0)

    Time complexity is
    O(n^n) time
    O(n) space

    Finish 7:37
    Nice!
    """
    solutions = []
    solution = []
    cols_with_queen = [False] * n
    diags_with_queen = [False] * (n * 2 - 1)
    # anti-diagonals
    adiags_with_queen = [False] * (n * 2)

    def find_solutions(row_idx):
        for col_idx in range(n):
            diag = row_idx + col_idx
            adiag = row_idx + n - col_idx
            if (
                cols_with_queen[col_idx]
                or diags_with_queen[diag]
                or adiags_with_queen[adiag]
            ):
                # Can't place a queen here due to the constraints
                continue
            solution.append(col_idx)
            if len(solution) == n:
                solutions.append([*solution])
            else:
                cols_with_queen[col_idx] = True
                diags_with_queen[diag] = True
                adiags_with_queen[adiag] = True
                find_solutions(row_idx + 1)
                adiags_with_queen[adiag] = False
                diags_with_queen[diag] = False
                cols_with_queen[col_idx] = False
            solution.pop()

    find_solutions(0)
    return solutions


def comp(a, b):
    return sorted(a) == sorted(b)


if __name__ == "__main__":
    exit(generic_test.generic_test_main("n_queens.py", "n_queens.tsv", n_queens, comp))

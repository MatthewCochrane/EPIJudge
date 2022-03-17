from typing import List, Iterator

from test_framework import generic_test


# Check if a partially filled matrix has any conflicts.
def is_valid_sudoku(partial_assignment: List[List[int]]) -> bool:
    """
    Start: 17:23
    Checking if a sudoku is valid involves checking that
    - there are no repeated elements in each row, and there are no values outside the range(0, 10)
    - there are no repeated elements in each col, and there are no values outside the range(0, 10)
    - there are no repeated elements in each 3x3 grid and no values outside range.
    0's may be repeated as they represent a blank cell.

    They are all 9x9 sudoku's.

    Pseudo code:
    check all values are in range(0, 10)
    for each row check for duplicates using a set, ignore 0's
    for each col check for duplicates using a set, ignore 0's
    for each 3x3 grid check for duplicates

    could be helpful to have a check_for_duplicates(iterator) function

    This is O(n*m) time, O(n) space
    We could probably do it in less space but we've specified that it's a 9x9 grid so really it's O(1) time O(1) space.
    There are some optimisations we could do to make it a little more efficient but probably not worth the readability
    loss.

    Finished: 17:47, had a 5 min break too.
    could tidy this code up a bit
    """

    def check_for_duplicates(vals: Iterator[int]) -> bool:
        seen = set()
        for v in vals:
            if v == 0:
                continue
            if v in seen:
                return True
            seen.add(v)
        return False

    rows, cols = len(partial_assignment), len(partial_assignment[0])
    assert (rows, cols) == (9, 9)
    # Don't need to check if values are in 0-9 because the question states they are.

    if any(check_for_duplicates(row) for row in partial_assignment):
        return False

    for col in range(cols):
        if check_for_duplicates((partial_assignment[i][col] for i in range(rows))):
            return False

    for subgrid_i in range(3):
        for subgrid_j in range(3):
            if check_for_duplicates(
                partial_assignment[subgrid_i * 3 + i][subgrid_j * 3 + j]
                for i in range(3)
                for j in range(3)
            ):
                return False

    return True


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_valid_sudoku.py", "is_valid_sudoku.tsv", is_valid_sudoku
        )
    )

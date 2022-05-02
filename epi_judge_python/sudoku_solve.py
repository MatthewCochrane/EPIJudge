import copy
import functools
import math
from typing import List, Tuple

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def solve_sudoku(partial_assignment: List[List[int]]) -> bool:
    """
    Time: 13:40
    Implement a sudoku solver.

    To solve a sudoku we need
        - every row to contain the numbers 1-9
        - every column to contain the numbers 1-9
        - every 3x3 square to contain the numbers 1-9

    We can probably take a trial-and-error approach.  We know this problem isn't trivial.

    example
    145|x2x|x3x
    xxx|xxx|xxx
    xxx|x5x|x4x
    ---+---+---
    xxx|x1x|xxx
    x8x|xxx|xxx
    xxx|xxx|xxx
    ---+---+---
    xxx|xxx|xxx
    x2x|x3x|xxx
    xxx|xxx|xxx

    [3][3] = 3 //3 = 1, 3//3 = 1
    [3][1] = 1, 1//3 = 0 = [1][0]
    def is_valid_option(pos: Tuple[int], value: int):
        pass

    def set_cell_val(pos: Tuple[int], value: int):
        pass

    def clear_cell_val(pos: Tuple[int]):
        pass

    def solve(start_pos = (0,0)):
        find the first unfilled cell
        if there is no unfilled cell
            return True
        for each number 1-9:
            if is_valid_option(pos, num):
                set_cell_value(pos, num)
                solve updated
                if solve(pos):
                    return True
                clear_cell_value(pos)
    solve()

    Finish at 14:40... took too long.
    Spent too much time debugging.
    I got tricked up with building col_sets.

    I didn't talk about the time/space complexity either...
    """
    rows = len(partial_assignment)
    cols = len(partial_assignment[0])
    row_sets = [set(row) for row in partial_assignment]
    col_sets = [
        set([partial_assignment[r][c] for r in range(rows)]) for c in range(cols)
    ]
    # print(row_sets)
    # print(col_sets)
    subgrids = [
        [
            set(
                [
                    partial_assignment[sr * 3 + r][sc * 3 + c]
                    for c in range(3)
                    for r in range(3)
                ]
            )
            for sc in range(3)
        ]
        for sr in range(3)
    ]

    def is_valid_option(pos: Tuple[int, int], value: int) -> bool:
        if value in row_sets[pos[0]]:
            return False
        if value in col_sets[pos[1]]:
            return False
        if value in subgrids[pos[0] // 3][pos[1] // 3]:
            return False
        return True

    def set_cell_value(pos: Tuple[int, int], value: int):
        partial_assignment[pos[0]][pos[1]] = value
        row_sets[pos[0]].add(value)
        col_sets[pos[1]].add(value)
        subgrids[pos[0] // 3][pos[1] // 3].add(value)
        # print('set', pos)
        # print(' ', partial_assignment)
        # print(' ', subgrids)

    def clear_cell_value(pos: Tuple[int, int]):
        value = partial_assignment[pos[0]][pos[1]]
        partial_assignment[pos[0]][pos[1]] = 0
        row_sets[pos[0]].remove(value)
        col_sets[pos[1]].remove(value)
        subgrids[pos[0] // 3][pos[1] // 3].remove(value)
        # print('clear', pos)
        # print(' ', partial_assignment)
        # print(' ', subgrids)

    def solve(pos: Tuple[int, int] = (0, 0)) -> bool:
        while pos[0] < 9 and partial_assignment[pos[0]][pos[1]]:
            pos = (pos[0], pos[1] + 1)
            if pos[1] >= 9:
                pos = (pos[0] + 1, 0)
        if pos[0] >= 9:
            # All cells are filled!
            return True
        for num in range(1, 10):
            if is_valid_option(pos, num):
                set_cell_value(pos, num)
                if solve(pos):
                    return True
                clear_cell_value(pos)
        return False

    return solve()


def assert_unique_seq(seq):
    seen = set()
    for x in seq:
        if x == 0:
            raise TestFailure("Cell left uninitialized")
        if x < 0 or x > len(seq):
            raise TestFailure("Cell value out of range")
        if x in seen:
            raise TestFailure("Duplicate value in section")
        seen.add(x)


def gather_square_block(data, block_size, n):
    block_x = (n % block_size) * block_size
    block_y = (n // block_size) * block_size

    return [
        data[block_x + i][block_y + j]
        for j in range(block_size)
        for i in range(block_size)
    ]


@enable_executor_hook
def solve_sudoku_wrapper(executor, partial_assignment):
    solved = copy.deepcopy(partial_assignment)

    executor.run(functools.partial(solve_sudoku, solved))

    if len(partial_assignment) != len(solved):
        raise TestFailure("Initial cell assignment has been changed")

    for (br, sr) in zip(partial_assignment, solved):
        if len(br) != len(sr):
            raise TestFailure("Initial cell assignment has been changed")
        for (bcell, scell) in zip(br, sr):
            if bcell != 0 and bcell != scell:
                raise TestFailure("Initial cell assignment has been changed")

    block_size = int(math.sqrt(len(solved)))
    for i, solved_row in enumerate(solved):
        assert_unique_seq(solved_row)
        assert_unique_seq([row[i] for row in solved])
        assert_unique_seq(gather_square_block(solved, block_size, i))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sudoku_solve.py", "sudoku_solve.tsv", solve_sudoku_wrapper
        )
    )

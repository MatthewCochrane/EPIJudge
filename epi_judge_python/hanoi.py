import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

NUM_PEGS = 3


def compute_tower_hanoi(num_rings: int) -> List[List[int]]:
    """
    Result is dict [from_peg, to_peg]
    We need to return a list of actions

    eg. 1
    1
    2
    -------
    1  2  3 Peg number


    2     1
    -------
    1  2  3 Peg number
    move 1 to 3

       2  1
    -------
    1  2  3 Peg number
    move 1 to 2

       1
       2
    -------
    1  2  3 Peg number
    move 3 to 1

    eg 2.
    1
    2
    3
    -------
    1  2  3 Peg number
    Perform the steps from eg. 1

       1
    3  2
    -------
    1  2  3 Peg number

    Now move 1 to 3
       1
       2  3
    -------
    1  2  3 Peg number

    Now move everything in 2 to 3


    So if we consider a recursive algorithm we can see it looks something like

    def move_m_from_x_to_y(x, y, m):
        if m == 0:
            return
        # z is not x and not y.  3 = 0 + 1 + 2, then the missing one bust be sum - x - y.
        z = 3 - x - y
        move_m_from_x_to_y(x, z, m-1)
        move x to y -> single movement...
        move_m_from_x_to_y(z, y, m-1)

    3 - -
    0 1 2
    move(0,2,3)
        move(0, 1, 2)
            move(0, 2, 1)
                move(0, 1, 0) - returns immediately because we're moving 0
                move 0 to 2
                  2-1
                move(1, 2, 0) - returns immediately because there are 0 on peg 1
            move 0 to 1
                111
            move(2, 1)
                12-
        move 0 to 2
        - 2 1
        move(1, 2, 0)
            move(1, 0, 1)
                move(1, 2, 2) - returns immediately
                move 1 to 0
                1 1 1
                move(

    All tests passed first go!  But I still should have been more detailed!

    It was a lot easier to think about moving m rings from x to y.
    Originally I was thinking 'move all but 1 from x to y'  and that works but
    it only works for the first part, as you get deeper that breaks and you need
    to move chunks of m..
    """
    moves = []

    def move_m_from_x_to_y(x, y, m):
        # z is not x and not y.  3 = 0 + 1 + 2, then the missing one bust be sum - x - y.
        z = 3 - x - y
        if m > 1:
            move_m_from_x_to_y(x, z, m - 1)
        moves.append([x, y])
        if m > 1:
            move_m_from_x_to_y(z, y, m - 1)

    move_m_from_x_to_y(0, 1, num_rings)
    return moves


@enable_executor_hook
def compute_tower_hanoi_wrapper(executor, num_rings):
    pegs = [list(reversed(range(1, num_rings + 1)))] + [[] for _ in range(1, NUM_PEGS)]

    result = executor.run(functools.partial(compute_tower_hanoi, num_rings))

    for from_peg, to_peg in result:
        if pegs[to_peg] and pegs[from_peg][-1] >= pegs[to_peg][-1]:
            raise TestFailure(
                "Illegal move from {} to {}".format(
                    pegs[from_peg][-1], pegs[to_peg][-1]
                )
            )
        pegs[to_peg].append(pegs[from_peg].pop())
    expected_pegs1 = [[], [], list(reversed(range(1, num_rings + 1)))]
    expected_pegs2 = [[], list(reversed(range(1, num_rings + 1))), []]
    if pegs not in (expected_pegs1, expected_pegs2):
        raise TestFailure("Pegs doesn't place in the right configuration")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "hanoi.py", "hanoi.tsv", compute_tower_hanoi_wrapper
        )
    )

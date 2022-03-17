from operator import add
from typing import List

from test_framework import generic_test


def matrix_in_spiral_order(square_matrix: List[List[int]]) -> List[int]:
    """
    Start: 8:20
    Compute the spiral order of the matrix

    eg.
    1 2 3
    4 5 6
    7 8 9
    gives 1 2 3 6 9 8 7 4 5
    ie 0-0, 0-1, 0-2, 1-2, 2-2, 1-0, 1,1

    square_matrix is square

    roughly we do
    go right until we hit the end, increment top
    go down until we hit the end, decrement right
    go left until we hit the end, decrement bottom
    go up until we hit the end, increment left

     1  2  3  4
     5  6  7  8
     9 10 11 12
    13 14 15 16

    top = 0, left = 0
    right = 4, bottom = 4 (len)
    go right until we hit right -> 1, 2, 3, 4
    top = 1
    go down until we hit bottom -> 8, 12, 16
    right -= 1 = 3
    go left until we hit left -> 15, 14, 13
    bottom -= 1 = 3
    go up until we hit top -> 9, 5
    left += 1 = 1
    go right until we hit right -> 6, 7
    top += 1 = 2
    go down until we hit bottom -> 11
    right -= 1
    go left until we hit left -> 10
    go up until we hit top -> can't move -> done

    We could use an array of moves
    dirs = (dr, dc)
    We could store this as a dict.
    key = dir, val = end

    Pseudo code
    directions = [right, down, left, up]
    updates = [top, right, down, left]
    while True:
        for each direction:
            if we can move in that direction:
                add val at position to result
                move one step in that direction
            if result length hasn't changed:
                add val at position to result (need to add last value)
                return
            update the top/right/down/left var

    Time complexity = O(m*n)
    Space complexity = O(1)
    Finish: 9:30
    Took too long.....  Maybe there are some ways to improve the pseudo code to make the actual
    code easier?

    Had a couple of small bugs.  Didn't consider the empty matrix approach which had an index error in my
    implementation.
    Also I thought that Tuple + Tuple did a elementwise addition, but instead it appends them.  Should check if
    there's a way to do element-wise addition of tuples.

    """
    if len(square_matrix) == 0:
        return []
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)
    directions = [RIGHT, DOWN, LEFT, UP]
    edges = {UP: 0, RIGHT: len(square_matrix), DOWN: len(square_matrix), LEFT: 0}
    pos = (0, 0)
    result = []
    while True:
        for dir_idx, direction in enumerate(directions):
            next_pos = tuple(map(add, pos, direction))
            result_len = len(result)
            while (
                edges[UP] <= next_pos[0] < edges[DOWN]
                and edges[LEFT] <= next_pos[1] < edges[RIGHT]
            ):
                result.append(square_matrix[pos[0]][pos[1]])
                pos = next_pos
                next_pos = tuple(map(add, pos, direction))
            if result_len == len(result):
                # Couldn't step in that direction so we must be done
                result.append(square_matrix[pos[0]][pos[1]])
                return result
            prev_direction = directions[dir_idx - 1]
            # Move the edge in the opposite direction to it's direction
            # eg. we should increment up so sum(-1, 0) = -1 and we say up edge -= -1 so edge += 1
            edges[prev_direction] -= sum(prev_direction)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "spiral_ordering.py", "spiral_ordering.tsv", matrix_in_spiral_order
        )
    )

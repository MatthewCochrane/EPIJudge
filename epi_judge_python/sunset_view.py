from typing import Iterator, List

from test_framework import generic_test


def examine_buildings_with_sunset(sequence: Iterator[int]) -> List[int]:
    """
    Start: 15:00
    Buildings have windows facing west
    Any building to the east of a building of greater or equal height cannot view the sunset.
    west          east
          x
        x x
    x   x x
    x x x x
    0 1 2 3
    buildings 2, 3 and 4 can view the sunset
    return the heights of the buildings that can view the sun (ie each building is specified by it's height)

    Pseudo code
    result = stack
    for each building:
        if stack is empty or building can see over others (building height > result[-1]):
            add to result stack
    return result stack

    O(n) time, O(1) space if you don't include the result array


    Ok, two mistakes.
    1. it said buildings are 'processed' in east-to-west order, I had it backwards.
    2. It wants the index not the height.  That's annoying because the question said 'each building is specified
       by it's height'  Anyway, that's fine.  Let's fix this up.

    west          east
          x
        x x
    x   x x
    x x x x
    3 2 1 0
    buildings 3, 1 and 0 can view the sunset
    return the building indices
            x
    x     x x
    x   x x x
    x x x x x
    4 3 2 1 0
    4, 1, and 0 can view the sunset

    4,3,2,1,3
            |
    [(4,0),(3,4)]

    Still O(n)
    We can push items onto the stack, ensuring the stack is monotonically decreasing.
    If we get a larger number, we pop values off the stack until we can insert it and have it be decreasing
    In this way we only push/pop items once, it's still O(n)

    Pseudo code:
    init result stack
    for building in sequence:
        while stack is not empty or building height <= last building height
            pop an item off the stack and discard it
        push this item onto the stack (height, index)
    return

    Finish: 15:28
    Don't like this question...

    The question says that the second way I wrote this out is better because it uses O(1) space in the best case
    while the approach I implemented uses O(n) space all the time, in the worst and best cases..
    Fair enough..
    """
    max_height = 0
    result = []
    sequence = list(sequence)
    for i in reversed(range(len(sequence))):
        height = sequence[i]
        if height > max_height:
            max_height = height
            result.append(i)
    return result


def examine_buildings_with_sunset_wrapper(sequence):
    return examine_buildings_with_sunset(iter(sequence))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sunset_view.py", "sunset_view.tsv", examine_buildings_with_sunset
        )
    )

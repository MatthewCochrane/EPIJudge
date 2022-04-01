import functools
import heapq
import math
from itertools import islice
from typing import Iterator, List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


class Star:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z

    @property
    def distance(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __lt__(self, rhs: "Star") -> bool:
        return self.distance < rhs.distance

    def __repr__(self):
        return str(self.distance)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, rhs):
        return math.isclose(self.distance, rhs.distance)


def find_closest_k_stars(stars: Iterator[Star], k: int) -> List[Star]:
    """
    Start: 10:01
    Find the k closest in three dimensional space

    We only care about stars that have a smaller distance.
    Find the k starts with the minimum distance from the point (0,0,0)
    Not really any different to finding k smallest integers in a list?
    Has < operator so we can put the stars themselves in a heap.

    for star in islice(iterator, k):
        push (-dist, star) to heap

    for each star:
        if dist < -(max distance in heap - heap[0]):
            pop largest heap item
            push this item (-dist, Star)
    return list(v[1] for v in heap)

    Python only gives a min heap.
    Store the -'ve values
    push (-dist, Star)

    1 2 3 4 5 6 1 2 2
    (-2,S) -1 -1

    O(n log k)
    O(n) best case
    O(k) space

    Finished 10:18
    Time: 17 mins.
    Honestly too slow.. Maybe.....

    """
    # Another way to do it, kinda cheating...
    # Strangely this is about 6 times slower than my approach below...
    # return heapq.nsmallest(k, stars)

    heap = []
    for star in islice(stars, k):
        heapq.heappush(heap, (-star.distance, star))
    for star in stars:
        if star.distance < -heap[0][0]:
            heapq.heappushpop(heap, (-star.distance, star))
    return list(item[1] for item in heap)


def comp(expected_output, output):
    if len(output) != len(expected_output):
        return False
    return all(
        math.isclose(s.distance, d) for s, d in zip(sorted(output), expected_output)
    )


@enable_executor_hook
def find_closest_k_stars_wrapper(executor, stars, k):
    stars = [Star(*a) for a in stars]
    return executor.run(functools.partial(find_closest_k_stars, iter(stars), k))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "k_closest_stars.py",
            "k_closest_stars.tsv",
            find_closest_k_stars_wrapper,
            comp,
        )
    )

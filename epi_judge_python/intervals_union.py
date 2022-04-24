import collections
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook

Endpoint = collections.namedtuple("Endpoint", ("is_closed", "val"))

Interval = collections.namedtuple("Interval", ("left", "right"))


def union_of_intervals(intervals: List[Interval]) -> List[Interval]:
    """
    endpoint is open before closed.  Only merge if at least one is closed.
    Annoying detail that me and the book disagreed on.
    I think that two intervals should only count as overlapping if they
    touch.  I say that if one interval finishes at x and another starts
    at x then for them to be 'overlapping' they must *both* be closed.
    The book says that if either is closed then they are overlapping.
    """

    def first_overlaps_second(i1: Interval, i2: Interval) -> bool:
        """
        Checks if i2 overlaps i1.  I1 is assumed to start before
        or at the same time as I2.
        ---c
           c---
        """
        return (i2.left.val < i1.right.val) or (
            # I disagree, I think this should be an and -------vv
            i2.left.val == i1.right.val and (i2.left.is_closed or i1.right.is_closed)
        )

    def larger_endpoint(e1: Endpoint, e2: Endpoint) -> Endpoint:
        if e1.val == e2.val:
            return Endpoint(e1.is_closed or e2.is_closed, e1.val)
        return e1 if e1.val > e2.val else e2

    result: List[Interval] = []
    for interval in sorted(intervals, key=lambda i: (i.left.val, not i.left.is_closed)):
        if not result or not first_overlaps_second(result[-1], interval):
            result.append(interval)
        else:
            result[-1] = Interval(
                result[-1].left, larger_endpoint(result[-1].right, interval.right)
            )
    return result


@enable_executor_hook
def union_of_intervals_wrapper(executor, intervals):
    intervals = [
        Interval(Endpoint(x[1], x[0]), Endpoint(x[3], x[2])) for x in intervals
    ]

    result = executor.run(functools.partial(union_of_intervals, intervals))

    return [
        (i.left.val, i.left.is_closed, i.right.val, i.right.is_closed) for i in result
    ]


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "intervals_union.py", "intervals_union.tsv", union_of_intervals_wrapper
        )
    )

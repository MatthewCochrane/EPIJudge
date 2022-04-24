import collections
import functools
import heapq
import itertools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import PropertyName
from test_framework.test_utils import enable_executor_hook

Interval = collections.namedtuple("Interval", ("left", "right"))


def add_interval(
    disjoint_intervals: List[Interval], new_interval: Interval
) -> List[Interval]:
    """
    We have a set of intervals
    and we want to add a new interval
    when we add the new interval we should merge any overlapping intervals
    return a *new* list

    Example:
        aaa bbb cc dddd eee
          nnnnnnn

        result:
        aaaaaaaaaa dddd eee

    Example:
        aaa bbb
           n
        result:
        aaaaaaa

    Example:
        aaaaa       bbb
              nnn
        result:
        aaaaa bbb   ccc


    Iterate through events including new event ordered by start time
        if the result has no events or this event starts after the end of the last event:
            append this event as a new event to result
        else:
            merge this event into the last event
                - set last event end time to max(last_end, curr_end)
    O(n) time
    O(1) space
    """
    merged_intervals = []
    # for event in sorted(itertools.chain(disjoint_intervals, [new_interval])): # 218, 14 O(n) space
    for event in heapq.merge(disjoint_intervals, [new_interval]):  # about the same average, slightly worse median (20us) O(1) space
        if not merged_intervals or event.left > merged_intervals[-1].right:
            merged_intervals.append(event)
        else:
            merged_intervals[-1] = Interval(merged_intervals[-1].left, max(merged_intervals[-1].right, event.right))
    return merged_intervals


@enable_executor_hook
def add_interval_wrapper(executor, disjoint_intervals, new_interval):
    disjoint_intervals = [Interval(*x) for x in disjoint_intervals]
    return executor.run(
        functools.partial(add_interval, disjoint_intervals, Interval(*new_interval))
    )


def res_printer(prop, value):
    def fmt(x):
        return [[e[0], e[1]] for e in x] if x else None

    if prop in (PropertyName.EXPECTED, PropertyName.RESULT):
        return fmt(value)
    else:
        return value


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "interval_add.py",
            "interval_add.tsv",
            add_interval_wrapper,
            res_printer=res_printer,
        )
    )

import collections
import functools
import heapq
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook

# Event is a tuple (start_time, end_time)
Event = collections.namedtuple("Event", ("start", "finish"))


def find_max_simultaneous_events(A: List[Event]) -> int:
    """
    Start: 10:32
    What's the maximum number of concurrent events in A?

    Example
             ddd
       aaa ccc
         bbbbbbbb
       There are three concurrent events above

    Example
        aaa
            bbb

    Example
        aaaaa  cc
         bb

    Naive way:
    - for each time, check how many intervals are within time.

    Better way:
    Sort events by start time
    max_concurrent = 0
    for each event:
        if any end times are before the start time:
            pop them off heap
        add end time to heap
        update max_concurrent based on heap len

    O(n log n) time
    O(n) space for the sort O(max_concurrent) space for the heap
    It's a calendar, so there shouldn't be millions of concurrent events...

        Example
             ddd
       aaa ccc
         bbbbbbbb
       0123456789
       There are three concurrent events above

       mc = 3
       h = 7,9,10

    A good way to think about this that I didn't really see is to think that each endpoint is a start or stop
    so every time we see a start, we increment the number of concurrent events and every time we see a stop
    we decrement the number of concurrent events.  In this way all we need is a full list of all endpoints
    that are sorted instead of trying to keep them together.

    create list of endpoints, start/stop pairs eg. (time, 0) for start and (time, 1) for stop.
    this will ensure that start endpoints come before stop endpoints
    for each endpoint
        if start:
            increment concurrent
        if end:
            decrement concurrent
        max_concurrent = max(max_concurrent, concurrent)
    return max_concurrent

    The time complexity if both approaches should be the same, both dominated by the sort.
    The space complexity is also the same, though the second approach will almost always use more space because
    it reallocates the endpoints array which has 2 tuples per event.
    """
    # Approach 2 - list of endpoints. 401us avg, 9us median
    START = 0
    END = 1
    # After looking at the answer, here's a slightly nicer way to write the 6 lines below.
    endpoints = [(event[0], START) for event in A] + [(event[1], END) for event in A]
    # endpoints = []
    # for event in A:
    #     # Start
    #     endpoints.append((event[0], START))
    #     # End
    #     endpoints.append((event[1], END))
    concurrent_events = 0
    max_concurrent = 0
    for time, endpoint_type in sorted(endpoints):
        if endpoint_type == START:
            concurrent_events += 1
            # Moving this line in here instead of down below improves the performance slightly
            max_concurrent = max(max_concurrent, concurrent_events)
        else:  # if
            concurrent_events -= 1
        # max_concurrent = max(max_concurrent, concurrent_events)
    return max_concurrent

    # Approach 1 - heap.  370us avg, 9us median
    # running_event_end_times_heap = []
    # max_concurrent = 0
    # for event in sorted(A):
    #     while running_event_end_times_heap and running_event_end_times_heap[0] < event[0]:
    #         heapq.heappop(running_event_end_times_heap)
    #     heapq.heappush(running_event_end_times_heap, event[1])
    #     max_concurrent = max(max_concurrent, len(running_event_end_times_heap))
    # return max_concurrent


@enable_executor_hook
def find_max_simultaneous_events_wrapper(executor, events):
    events = [Event(*x) for x in events]
    return executor.run(functools.partial(find_max_simultaneous_events, events))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "calendar_rendering.py",
            "calendar_rendering.tsv",
            find_max_simultaneous_events_wrapper,
        )
    )

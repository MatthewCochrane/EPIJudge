import heapq
from typing import Iterator, List

from test_framework import generic_test


def online_median(sequence: Iterator[int]) -> List[float]:
    """
    Start: 10:26

    What is the median?
    'middle' number in the sorted sequence
    if there are two middle numbers it's the average of them or half way between them.

    1 2   3 4   5
    1 1.5 2 2.5 3

    If sorted, look back half the distance and pick that number or numbers.
    may need up to O(n) space...

    1 5 2 4 8 9 3 1 8 5

    1.. o
    1 -> 1

    5.. e
    1 5 -> 3

    2.. o
    2 5 -> 2

    4.. e
    2 4 5 -> 3

    8.. o
    4 5 8 -> 4

    9.. e
    4 5 8 9 -> 4.5

    3.. o
    3 4 5 8 -> 3


    1.. 1 -> 1

    5.. 1 5 -> 1 + 5 / 2 = 3
         |

    2.. 1 2 5 -> 2
          |

    4.. 1 2 4 5 -> 2 + 4 / 2 = 3
           |

    8.. 1 2 4 5 8 -> 4
            |

    9.. 1 2 4 5 8 9 -> 4.5
             |

    3.. 1 2 3 4 5 8 9 -> 4
              |

    1.. 1 1 2 3 4 5 8 9 -> 3.5
               |

    8.. 1 1 2 3 4 5 8 8 9 -> 4
                |

    5.. 1 1 2 3 4 5 5 8 8 9 -> 4.5
                 |

    O(n) space
    O(n) time per item = O(n^2) time

    sort -> O(n log n) time and O(n) space

    How to find median of unsorted list?

    What if we use two heaps?
    ->>><<<-

    Aim to balance the size of the two heaps
    one is a min heap (larger items) and one is a max heap (smaller items)

    # lower = -4, -2, -1
    # upper = 5, 8

    first = next(it, None)
    if first is None:
        return []
    push first to left heap
    append first to result
    when we get a new value:
        if val < -(small max):
            val = -replace in small heap (negated)
        elif large heap is not empty and val > large min:
            val = replace in large heap
        if len(small_heap) <= len(large_heap):
            push to small heap (negated)
        else:
            push to large heap
        if len(small) == len(large):
            return (large_min  + -(small max)) / 2
        else:
            # smaller heap is always the longer one
            return -(small max)
    return list

    O(n) space
    O(n * log n) time

    Finding the median requires access to every previous number!  Unless you constrict your bound as you go..
    You can keep a summary, say 'n numbers above x' and that's find but if your median ever went above x
    you would no longer be able to calculate it.

    One small bug, didn't add first_item to result
    Finished: 11:41
    1 hour 20 mins
    Obviously too long but good work you got there!

    The same approach as in their solution.  Why did it take me so long to reason about the median?
    I spent like 30 mins thinking about whether we could do it in less time.  It wasn't immediately obvious
    that a 'running median' will require storing all previous elements.

    I should repeat this question!
    """
    first_item = next(sequence, None)
    if first_item is None:
        return []
    result = [first_item]
    # lower_heap is a max heap and upper_heap is a min heap
    # we aim to keep these heaps the same length
    lower_heap, upper_heap = [-first_item], []
    for val in sequence:
        if val < -lower_heap[0]:
            val = -heapq.heappushpop(lower_heap, -val)
        elif upper_heap and val > upper_heap[0]:
            val = heapq.heappushpop(upper_heap, val)
        if len(lower_heap) <= len(upper_heap):
            heapq.heappush(lower_heap, -val)
        else:
            heapq.heappush(upper_heap, val)
        if len(lower_heap) == len(upper_heap):
            result.append((upper_heap[0] + -lower_heap[0]) / 2)
        else:
            # Lower heap is always the longer one because of the <= above
            result.append(-lower_heap[0])
    return result


def online_median_wrapper(sequence):
    return online_median(iter(sequence))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "online_median.py", "online_median.tsv", online_median_wrapper
        )
    )

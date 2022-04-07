import collections
from typing import List

from test_framework import generic_test
from test_framework.test_failure import PropertyName

MinMax = collections.namedtuple('MinMax', ('smallest', 'largest'))


def find_min_max(A: List[int]) -> MinMax:
    """
    Start: 13:02
    Can we compute the min and max with less than 2(n-1) comparisons?

    So the 'naive' way to do this would be to find the min and max separately

    for num in A:
        smallest = min(smallest, num)
        largest = max(largest, num)

    How can we optimise this algorithm?

    min, max = first
    for num in A:
        if num < smallest:
            smallest = num
        elif num > largest:
            largest = num

    This isn't much different to the other one in most situations.  It's faster if we have a decreasing sequence.

    Is there a way to check > and < at the same time?
    bitwise operators?
    Is there a way to update both the min and max at the same time?
    ranges?

    add and subtract
    xor
    comparator for both min and max

    3 4 2 5 1
    3 7 9 14 15

    if not min or max, xor

    > >= < <= == !=

    a < b and b < c implies a < c

    hmmm...
    Book has a very different answer.

    """

    # iterator = iter(A)
    # smallest = largest = next(iterator, None)
    # for num in iterator:
    #     if num < smallest:
    #         smallest = num
    #     elif num > largest:
    #         largest = num
    # return MinMax(smallest, largest)


def res_printer(prop, value):
    def fmt(x):
        return 'min: {}, max: {}'.format(x[0], x[1]) if x else None

    if prop in (PropertyName.EXPECTED, PropertyName.RESULT):
        return fmt(value)
    return value


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_for_min_max_in_array.py',
                                       'search_for_min_max_in_array.tsv',
                                       find_min_max,
                                       res_printer=res_printer))

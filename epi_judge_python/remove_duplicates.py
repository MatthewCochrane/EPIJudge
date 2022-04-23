import functools
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


class Name:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name, self.last_name = first_name, last_name

    def __lt__(self, other) -> bool:
        return (self.first_name < other.first_name
                if self.first_name != other.first_name else
                self.last_name < other.last_name)


def eliminate_duplicate(A: List[Name]) -> None:
    """
    Start: 9:37
    we have a list of names (First, Last)
    remove the items from A that have duplicate first names.

    If this was about ints like remove duplicates from an int list we'd just do
    set(A)

    Ok, so in general, we can do this in O(n) time if we use O(n) extra space for a set/dict.
    If we want to do this with less than O(n) space we would need to sort the array and could do it in O(n log n) time.



    """
    first_names = set()
    result = []
    for name in A:
        if name.first_name not in first_names:
            first_names.add(name.first_name)
            result.append(name)
    A[:] = result



@enable_executor_hook
def eliminate_duplicate_wrapper(executor, names):
    names = [Name(*x) for x in names]

    executor.run(functools.partial(eliminate_duplicate, names))

    return names


def comp(expected, result):
    return all([
        e == r.first_name for (e, r) in zip(sorted(expected), sorted(result))
    ])


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('remove_duplicates.py',
                                       'remove_duplicates.tsv',
                                       eliminate_duplicate_wrapper, comp))

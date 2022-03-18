import functools
from typing import List

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def replace_and_remove(size: int, s: List[str]) -> int:
    """
    Start: 13:56
    Replace and remove
    replace each 'a' with two 'd's
    delete each entry containing a 'b'

    The list is large enough to fit the result already.
    Only apply the formula to the first n entries.

    Examples:
        a,c,d,b,b,c,a
        a,c,d,x,x,c,a
        a,c,d,c,a
        d,d,c,d,c,d,d

    pass 1
    walk through array, move each item to new location skipping b's
    pass 2
    work out where the last char goes
    walk backward, moving each char into it's new location

    a,c,d,b,b,c,a
    a,c,d,c,a,c,a - end of array is 5
              | |
    a,c,d,c,a,c,a - end of array is 5
    count the a's -> 2 a's in the array (before index 5)
    total new length = 5 + num_a's = 7
    d,d,c,d,c,d,d - end of array is 5
    start with to_ptr = calculated end (7) - 1 = 6
           and from_ptr = end_of_array = 5 - 1 = 4
    if the char is not 'a', copy it to end, increment both
    if the char is 'a', copy two d's to the end, increment 'to' twice and 'from' once
    O(n) time - a few passes
    O(1) space

    Pseudo code:
    to_ptr = 0
    for from_ptr in range(size):
        if from_ptr val is a b, continue
        move from_ptr to to_ptr
        increment to_ptr
    current length = to_ptr
    to_ptr = count the a's and add to current_length - 1
    ret_val = to_ptr + 1
    for from_ptr in reversed(range(current_length)):
        if the char is 'a':
            # use a slice?
            copy d to to_ptr
            decrement to_ptr
            copy d to to_ptr
            decrement_to_ptr
        else if char is not 'a':
            copy it to the end
            decrement to_ptr
    return ret_val


    All tests pass, first run.
    Time: 14:36 - about 40 mins.
    """
    to_ptr = 0
    for from_ptr in range(size):
        if s[from_ptr] == "b":
            continue
        s[to_ptr] = s[from_ptr]
        to_ptr += 1
    current_len = to_ptr
    a_count = functools.reduce(
        lambda p, c: p + int(c == "a"), (s[i] for i in range(current_len)), 0
    )  # 2
    final_len = current_len + a_count
    to_ptr = final_len - 1
    for from_ptr in reversed(range(current_len)):
        if s[from_ptr] == "a":
            s[to_ptr - 1 : to_ptr + 1] = ["d", "d"]
            to_ptr -= 2
        else:
            s[to_ptr] = s[from_ptr]
            to_ptr -= 1
    return final_len


@enable_executor_hook
def replace_and_remove_wrapper(executor, size, s):
    res_size = executor.run(functools.partial(replace_and_remove, size, s))
    return s[:res_size]


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "replace_and_remove.py",
            "replace_and_remove.tsv",
            replace_and_remove_wrapper,
        )
    )

import functools

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


# Assume s is a list of strings, each of which is of length 1, e.g.,
# ['r', 'a', 'm', ' ', 'i', 's', ' ', 'c', 'o', 's', 't', 'l', 'y'].
def reverse_words(s):
    """
    Start: 14:58
    Reverse words in place.

    Example
        'alice likes bob' -> 'bob likes alice'
        'is an elephant' -> 'elephant an is'
        'elephant an is'
        'si na tnahpele'
        'is an elephant'
         012345678901234
        'is an elephants'
         11 11
         34 01 012345678


    Naive -> split, reverse, join.  O(n) extra space required.

    some thinking..........

    reverse the array then reverse the words?
    That works! O(n) time and O(1) space!  Good problem solving!

    Pseudo code
    reverse the array in place
    while True:
        find the end of this word
        reverse the word
        find the start of the next word

    All tests pass first attempt.
    Time: 15:27
    That took 30 mins, and I had a 'real' problem solving insight!!  Cool :)
    """
    s.reverse()
    word_start = 0
    # skip leading spaces
    while word_start < len(s) and str.isspace(s[word_start]):
        word_start += 1
    while word_start < len(s):
        # find the end of the word
        word_end = word_start
        while word_end + 1 < len(s) and not str.isspace(s[word_end + 1]):
            word_end += 1
        # reverse the word
        l, r = word_start, word_end
        while l < r:
            s[l], s[r] = s[r], s[l]
            l, r = l + 1, r - 1
        # find the start of the next word
        word_start = word_end + 1
        while word_start < len(s) and str.isspace(s[word_start]):
            word_start += 1


@enable_executor_hook
def reverse_words_wrapper(executor, s):
    s_copy = list(s)

    executor.run(functools.partial(reverse_words, s_copy))

    return "".join(s_copy)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "reverse_words.py", "reverse_words.tsv", reverse_words_wrapper
        )
    )

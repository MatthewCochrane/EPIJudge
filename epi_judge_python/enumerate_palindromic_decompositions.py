from typing import List

from test_framework import generic_test


def palindrome_decompositions(text: str) -> List[List[str]]:
    """
    Compute all palindromic decompositions of text.

    "01234"
    return [["0", "1", "2", "3", "4"]]

    "010123"
    [0, 1, 0, 1, 2, 3], [010, 1, 2, 3], [0, 101, 2, 3]

    "010111"
    [0 1 0 1 1 1], [010, 111], [010, 11, 1], [010, 1, 11], [0, 101, 1, 1], [0, 101, 11]

    "010111"
    0 10111
      1 0111
        0 111
          1 11
            1 1 - 0 1 0 1 1 1
            11 - 0 1 0 1 11
          111 - 0 1 0 111
          11 1 - 0 1 0 11 1
      101 11
        1 1 - 0 101 1 1
        11 - 0 101 11
    010 111
      1 11
        1 1 - 010 1 1 1
        11 - 010 1 11
      11 1 - 010 11 1

    def find_palindromes(txt):
        find palindrome prefix's:
            if suffix is not empty:
                results = find_palindromes(bit after prefix)
            add prefix to each result or just add suffix

    prefix = []
    def find_palindromes(start_idx):
        if at end of str:
            copy prefix to results
        find palindrome prefix's:
            add prefix to prefix list as a group
            find_palindromes(new_suffix)
            pop prefix
    find_palindromes(0)




    len = 6
    "010123"
    fp(0)
        for i in range(0, 6):
            i=0
            0 == 0
            prefix = [0]
            fp(1)
            for i in range(1, 6):
                i=1
                1 == 1
                ...
            i=1
            01 != 10
            i=2
            010 == 010
            prefix = [010]
            fp(3)
            ...


    """
    result = []
    prefix = []

    def find_palindromes(start_idx):
        if start_idx >= len(text):
            result.append([*prefix])
        for i in range(start_idx, len(text)):
            slice = text[start_idx : i + 1]
            if slice == slice[::-1]:  # is palindromic
                prefix.append(slice)
                find_palindromes(i + 1)
                prefix.pop()

    find_palindromes(0)
    return result


def comp(a, b):
    return sorted(a) == sorted(b)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "enumerate_palindromic_decompositions.py",
            "enumerate_palindromic_decompositions.tsv",
            palindrome_decompositions,
            comp,
        )
    )

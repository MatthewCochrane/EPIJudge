from typing import List

from test_framework import generic_test, test_utils


def phone_mnemonic(phone_number: str) -> List[str]:
    """
    Start: 15:33
    Take an input phone number and return all possible character sequences
    that correspond to the phone number.

    O(4^logn) or O(4^(digits in n))

    example:
        23
        2 - abc
        3 - def
        ad
        ae
        af
        bd
        be
        bf
        cd
        ce
        cf

    Total results is number of options in each digit multiplied together.
    Probably cheat and use str(int) here since it's not the main part of the problem.
    I'm guessing there's an itertools function that would do this for us.

    digit 1
    set to first value
    digit 2
    set to first value
    ...
    digit n
    set to first value


    set of nested loops

    Can we do this with recursion?

    combinations of '3' -> d, e, f
    backtracking?
    use an array to show where we're up to

    [n0, n1, n2]
    if len = len of string:
        ''.join(ary)

    recursion and backtracking

    map of digit to letters
    array of letter
    result = []
    def find_mnemonics(start_idx):
        num = get digit
        result.append('')
        for val in map[num]:
            result[-1] = val
            if start_idx + 1 >= len(s):
                append to result
            else:
                find_mnemonics(start_idx + 1)
        result.pop()
    call func(0)

    O(4*4*4*4 n times) = O(4^log n) or O(4^digits)
    O(digits) space
    Actually this was wrong.  It's O(4^digits*dights) because for each of those cases, we copy a string of length digits.

    Finish: 16:05
    Pretty good, took 30 mins.

    One good idea from the book is to decrease the size of the mapping by using strings instead of arrays.
    Potentially also using a tuple instead of a dictionary.  eg.
    letters_mapping = ('0', '1', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz')

    Also not here that because the final length is fixed (which I wasn't aware of ahead of time, thought 0 and 1 were
    mapping to empty strings), we can pre-declare the letters array and don't have to push/pop just set the appropriate
    index.

    Also note that they call into the last level of the helper where as I returned before the call which should make
    mine faster.  That's something the coach was helping me with.
    """
    letters_map = {
        "0": ["0"],
        "1": ["1"],
        "2": ["a", "b", "c"],
        "3": ["d", "e", "f"],
        "4": ["g", "h", "i"],
        "5": ["j", "k", "l"],
        "6": ["m", "n", "o"],
        "7": ["p", "q", "r", "s"],
        "8": ["t", "u", "v"],
        "9": ["w", "x", "y", "z"],
    }
    letters = []
    result = []

    def find_mnemonics(idx: int) -> None:
        digit = phone_number[idx]
        letters.append("")
        for c in letters_map[digit]:
            letters[-1] = c.upper()
            if idx + 1 >= len(phone_number):
                result.append("".join(letters))
            else:
                find_mnemonics(idx + 1)
        letters.pop()

    find_mnemonics(0)
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "phone_number_mnemonic.py",
            "phone_number_mnemonic.tsv",
            phone_mnemonic,
            comparator=test_utils.unordered_compare,
        )
    )

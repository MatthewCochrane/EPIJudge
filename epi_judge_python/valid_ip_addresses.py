from typing import List

from test_framework import generic_test


def get_valid_ip_address(s: str) -> List[str]:
    """
    Start: 19:37
    Return a list of all valid ip addresses that can be made by inserting periods to s.

    Example:
        19216811
        Answers
        1.92.168.11
        192.16.81.1
        192.16.81.1
        192.168.1.1
        192.16.81.1

    from the start, find all valid first parts
        1, 19 192
        find valid second parts:
            1 -> 9, 92
            19 -> 2, 21, 216
            192 -> 1, 16, 168
            find valid third part
                9 -> 2, 21, 216
                92 -> 1, 16, 168
                2 -> 1, 16, 168
                21 -> 6, 68, 681
                216 -> 8, 81, (811) -invalid, not enough spots left
                1 -> 6, 68, 681
                16 -> 8, 81, (811) -invalid, not enough spots left
                168 -> 1, (11) - invalid, not enough spots left
                find fourth part
                    remaining...
                    add to result

    Pseudo code:
    19216801
    1
    1
     2
     92
       3
       168
         4
         801

    def recurse(start_idx, decimals_left):
        if decimals_left == 0:
            if start_idx != len(s):
                return
            append to result
            return
        num = 0
        for i in range(start_idx, len(s)):
            if i > start_idx and num == 0:
                # parts that start with a 0 and have len > 1 are invalid.
                # eg. 05 is invalid
                break
            take a character and add it to num -> num *= 10 ; num += int(char)
            if num < 256 and (len(s) - i) > decimals_left:
                recurse(i + 1, decimals_left - 1)
            else
                break
    time complexity:
    4 choices in  n-1
    n-1 choose 4 -> (n-1)!/4!(n-1-4)! = (n-1)!/4!(n-5)! n-1->n-5/24 n-1*n-2*n-3*n-4 = n^4
    O(n^4) time
    O(n) space
    Finished at 20:25
    """
    result = []
    parts = []

    def recurse(start_idx, parts_left):
        if parts_left == 0:
            if start_idx != len(s):
                return
            result.append(".".join(parts))
            return
        num = 0
        for i in range(start_idx, len(s)):
            if i > start_idx and num == 0:
                # parts that start with a 0 and have len > 1 are invalid.
                # eg. 05 is invalid
                break
            num *= 10
            num += int(s[i])
            if num < 256 and (len(s) - i) >= parts_left:
                parts.append(str(num))
                recurse(i + 1, parts_left - 1)
                parts.pop()
            else:
                break

    recurse(0, 4)
    return result


def comp(a, b):
    return sorted(a) == sorted(b)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "valid_ip_addresses.py",
            "valid_ip_addresses.tsv",
            get_valid_ip_address,
            comparator=comp,
        )
    )

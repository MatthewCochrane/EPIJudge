from test_framework import generic_test


def is_palindrome(s: str) -> bool:
    """
    Start: 14:42
    Return true if s is palindromic when punctuation is ignored.  It should also ignore case.

    "race Car!"
        |
    we don't know when to stop... Trick just don't stop...  The alternative would be to do another pass to count
    the punctuation which would take the same amount of time anyway!  Actually that wouldn't even work.
    Ok, start without worrying about the extra time of traversing the whole string instead of stopping in the middle.

    Can just stop when l >= r


    Pseudo code
    l and r pointers
    while l < r:
        if not str.isalnum(l):
            l += 1
            continue
        if not str.isalnum(r):
            r -= 1
            continue
        if lower(l) != lower(r)
            return False
        l += 1
        r -= 1
    return True
    O(n) time
    O(1) space

    time: 14:52 -> 10 mins
    """
    # abCcba!
    #   ||
    l, r = 0, len(s) - 1
    while l < r:
        if not str.isalnum(s[l]):
            l += 1
            continue
        if not str.isalnum(s[r]):
            r -= 1
            continue
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_string_palindromic_punctuation.py",
            "is_string_palindromic_punctuation.tsv",
            is_palindrome,
        )
    )

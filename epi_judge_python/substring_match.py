import functools

from test_framework import generic_test


def rabin_karp(t: str, s: str) -> int:
    """
    Similar to leetcode #28

    find s within t

    abcdef -> cd
    can do this in O(m*n) pretty easily, just search for t from each index in s

    Can do in O(n) as well if we use a rolling hash.
    I don't know rabin karp

    if len(t) < len(s) return -1
    calculate hash of s
    add the first len(s) chars of t to the hash
    for i from len(s) to len(t)
        remove i-len(s) from hash
        add i to hash
        if hash == hash_of_s and s[i-len(s):i+1] == t:
            return i
    return -1

    O(m + n) time
    O(m) space because of the way I did the slicing.  Could do O(1) easily in a few more lines of code

    """

    def update_hash(hash: int, c) -> int:
        return hash ^ ord(c)

    if len(t) < len(s):
        return -1
    if t == s:
        return 0

    s_hash = functools.reduce(lambda p, c: update_hash(p, c), s, 0)
    hash = functools.reduce(lambda p, c: update_hash(p, c), t[: len(s)], 0)
    for i in range(len(s), len(t)):
        if hash == s_hash and t[i - len(s) : i] == s:
            return i - len(s)
        hash = update_hash(hash, t[i - len(s)])
        hash = update_hash(hash, t[i])
    if hash == s_hash and t[-len(s) :] == s:
        return len(t) - len(s)
    return -1


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "substring_match.py", "substring_match.tsv", rabin_karp
        )
    )

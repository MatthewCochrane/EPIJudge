from bisect import bisect_right

from test_framework import generic_test


def square_root(k: int) -> int:
    """
    Start: 16:04
    Find the largest int whose square is less than or equal to k.

    Example
    16 -> return 4
    300 -> return 17 since 17^2 is 289 and 18^2 is 324

    We're searching for a number between 0 and k where num**2 < k

    Can do this with binary search

    FFFFFFFFTTTTTTT

    Use bisect_left to find first item where num**2 > k
    or the last item where num**2 <= k .. closer to the question

            lr
          F T T   T
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17

    def map_to_new_seq(num):
        num ** 2 > k

    bisect_right(new_sequence, False, 0, k) - 1

    O(log k) time
    O(1) space

    Finish: 16:23
    19 mins
    Be careful with edge cases!!!!
    You missed the k=0 case!
    """

    if k == 0:
        return 0

    class Helper:
        def __getitem__(self, num):
            return (num ** 2) > k

    # Helper maps our 'true' sequence into the sequence we want to binary search over.
    return bisect_right(Helper(), False, 0, k+1) - 1


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "int_square_root.py", "int_square_root.tsv", square_root
        )
    )

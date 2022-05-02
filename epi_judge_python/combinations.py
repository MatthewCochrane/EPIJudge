from typing import List

from test_framework import generic_test, test_utils


def combinations(n: int, k: int) -> List[List[int]]:
    """
    Return all size k subsets from 1..n
    Eg.
    n = 3, k = 2
        full set is {1,2,3}
        return [{1,2}, {1,3}, {2,3}]
    there are n bits and we want all of the numbers up to 2^n that have k set bits.
    011, 101, 110
    or for a larger number
    43210
    0001?
    00011

    001??
    00101
    00110

    01???
    01001
    01010
    01100

    1????
    10001
    10010
    10100
    11000

    00111
    01011
    01101
    01110
    10011

    result = []
    def comb(n, k, num):
        if k == 0:
            add to result
        for i in range(k-1, n):
            comb(i, k-1, num | (1<< i))
    comb(n, k)
    return result


    func comb(n, k):
        if hit bottom:
            add to result
        loop over indices from k to n:
            set a bit
            recurse(subproblem of bits to the right of the set bit, k-1)
    call comb
    return results

    func comb()
        recurse()







    put a 1 somewhere, then select k-1 from the numbers to the right
    eg. c(5, 3) ->
        set bit 2, c(2, 2)
        set bit 3, c(3, 2)
        set bit 4, c(4, 2)

    def comb(n, k, num):
        if k == 0:
            add to result
        for leftmost in range(k-1, n):
            num |= (1 << leftmost)
            comb(leftmost, k-1)
            num &= ~(1 << leftmost)

    c(5, 3)
        for l in range(3-1, 5):
            comb(2, 2)
                for l in range(1, 2):
                    comb(1, 1)
                        for l in range(0, 1):
                            comb(0,0)
            comb(3, 2)
            comb(4, 2)


    """
    result = []

    def comb(n, k, num):
        if k == 0:
            result.append([i + 1 for i, v in enumerate(bin(num)[2:][::-1]) if v == '1'])
            return
        for leftmost in range(k - 1, n):
            comb(leftmost, k - 1, num | (1 << leftmost))

    comb(n, k, 0)
    return result


if __name__ == "__main__":
    # print(combinations(5, 2))
    # exit(0)
    exit(
        generic_test.generic_test_main(
            "combinations.py",
            "combinations.tsv",
            combinations,
            comparator=test_utils.unordered_compare,
        )
    )

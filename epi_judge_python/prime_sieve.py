from typing import List

from test_framework import generic_test


# Given n, return all primes up to and including n.
def generate_primes(n: int) -> List[int]:
    """
    Find all primes up to and including n.

    Primes are integers than are larger than 1 and have no divisors other than 1 and themself.

    Example:
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
        P, P, N  P  P, P  N  N   N,  P,  N, P

        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
        X  P  X  P  X  P  X  X   X   P   X   P   X   X

    One way...
    for each number from 1 up to and including sqrt(n):
        if number has not been marked off, copy it to the result
        mark off all multiples less than n

    n/2 + n/3 + n/4 + ... sqrt(n)/sqrt(n)
    n + n + n + n ... = n^2
    is this O(n) or O(n^2)?
    sqrt(n) things between n and sqrt(n)
    So time is somewhere between sqrt(n)*sqrt(n) and sqrt(n)*n
    Let's say its O(n*sqrt(n)). Though there may be a more precise version.

    2 1.4 - 1 - 3
    3 1.? - 1 - 3
    4 2
    5 2.?
    6 2.?
    7 2.?
    8 2.?
    9 3

    Passed.  Not sure of the time complexity, space is O(n)
    I think the time is O(n) but not sure...  The time is definitely O(n^2).
    The time complexity is O(n log log n), not surprising I didn't get that.
    """
    # [X,X,T,T,F,T,F]
    #  0 1 2 3 4 5 6
    #
    # [2, 3, 5]
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    result = []
    for i in range(2, n + 1):
        if not is_prime[i]:
            continue
        result.append(i)
        multiple = 2 * i
        while multiple <= n:
            is_prime[multiple] = False
            multiple += i
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "prime_sieve.py", "prime_sieve.tsv", generate_primes
        )
    )

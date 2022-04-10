from test_framework import generic_test


def gcd(x: int, y: int) -> int:
    """
    Greatest common divisor
    what's the largest number that both x and y are divisible by
    example 10 and 5
    GCD is 5
    example
      9, 33
    9/3 33/3

    largest number that
    - x/ number is a whole number
    - y / number is a whole number

    find the largest number that satisfies
    x % number == 0 and y % number == 0

    """
    return 0


if __name__ == '__main__':
    exit(generic_test.generic_test_main('euclidean_gcd.py', 'gcd.tsv', gcd))

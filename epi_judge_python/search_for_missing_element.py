import collections
import functools
import itertools
from operator import xor
from typing import List

from test_framework import generic_test
from test_framework.test_failure import PropertyName

DuplicateAndMissing = collections.namedtuple(
    "DuplicateAndMissing", ("duplicate", "missing")
)


def find_duplicate_missing(A: List[int]) -> DuplicateAndMissing:
    """
    Start: 15:45
    Find the duplicated and the missing number.

    We have an array like

    [0,1,2,3,4] -> 5 numbers from 0 to n-1
    one number is missing and one number is duplicated
    example

    [2,3,1,4,1]
    I notice that the duplicate number is 1.  That's just because I see multiple 1's.
    If it was a really long list, how would I find a duplicate?
    - I could search the array for each number to see if it appears again O(n^2) time, O(1) space
    - I could sort the numbers O(n log n) time, O(n) space
    - I could store the numbers O(n) time, O(n) space
    - If there were exactly N numbers then we could find the duplicate with pigeonhole principle in O(n) time, O(1) space

    Can we do anything useful with xor or diff?
    in the case above
    0,1,2,3,4
    1,1,2,3,4

    expected xor values = 0 xor 1 = 1

        missing
    xor extra
        0b0001

    [2,3,1,4,1]
     3,2,0,5,0

    What if we sort the list into order
    if not in correct place, move it to correct place, if in correct place, skip...

    0,2,3,1,3

    0,1,2,3,4
    0,1,2,3,2
    O(n) time and O(1) space

    0,1,2,3,4
    0,3,4,2,2

    0,1,2,3,4
    0 2 3 2 1
    0 2 2 3 1

    10 - 8 = 2


    0,3,2,3,4
    cur_idx = 2

    only move each item once -> move it to it's true position.
    We might look at each number twice if we re-jig the entire array with the first index then iterate through all
    further indices before finding the result at the end.

    n(n-1)/2 - sum(vals) = missing - duplicate
    calc_value = calc n(n-1)/2 - sum(vals)
    For each index in the array:
        cur_idx = orig_idx
        while the A[cur_idx] does not match cur_idx:
            move the value to it's desired index and update current value with the value in that location
        # if cur_idx != orig_idx:
        #     curr_idx is the duplicate!
        #     missing = calc_val + duplicate
        set original index to the current value (same as the index)

    1,3,1
    1,3
    xor'd we'll get 1

      2,4
    0,2,4
    xor gives 0

    this will give either the missing or extra
    scan through array, if it's in the array it's the extra, otherwise it's the missing.

    [2,3,1,4,1]
     0 1 1 0 1

    0,1,2,3,4
    0 1 0 1 0

    duplicate is in one of the sets (0 or 1) and the missing is in the other...
    n/2 * n/2 = n^2 options...

    How many paris of numbers are there where a xor b = 1

    0001 xor 0000 = 0001
    zzz1 xor zzz0 = 0001
    as long as the z's are the same in the two numbers then there's an answer
    So there are (2^n)/2 options

    expected total - actual total = n(n-1)/2 - sum(vals)
    4+...
    2+...
    0,
    1,

    can find: missing - duplicate
    in this case 0 - 1 = -1
    -1 = missing - duplicate


    for each number
    [2,3,1,4,1]
     3,2,0,5,0

    2 xor 1 = 3 so if 2 was our duplicate the three would be missing
    we also know that -1 = missing - duplicate
    so missing = -1 + duplicate
    -1 + 2 = 1 so missing must be 1 if duplicate is 2  but 1 != 3
    So if 2 was our duplicate then one equation says missing should be 3 but the other says missing should be -1
    so 2 must not be our duplicate.

    next
    3 xor 1 = 2 so if 3 was dup then 2 would be missing
    missing = duplicate - 1
    missing = 3 - 1 = 2
    So this is our answer... but it's not!!!!  WTF?

    Not sure how many valid answers we could get... perhaps we can get n/2 still?




    Whatever is in missing
    0 and 1 -> valid
    0 and 2 ->
    0 and 3
    0 and 4
    1 and 2
    1 and 3
    1 and 4
    2 and 3 -> valid
    2 and 4 -> not valid because 2 xor 4 does not equal 1
    3 and 4 -> not valid because 3 xor 4 does not equal 1







    Neither the xor nor the sum approach works...
    We could possibly use sum and product?  But product will overflow.  And I don't know the equation for it.
    Also calculating n! probably takes O(n) space to compute...
    What is the space complexity of storing n! ?
    What's the time complexity of computing n! ?

    I note that we have two methods for finding two separate equations.  We can usually solve simultaneous equations
    but equations with xor can't be easily solved for.



    There's another way to do this though...

    If we know the xor and the diff we can

    diff = expected - actual = 10 - 11 = -1
    diff = missing - duplicate
    miss - dup = -1
    miss = -1 + dup
    miss = dup - 1
    dup = miss + 1

     0 1 2 3 4
     1 1 2 3 4
    [2,3,1,4,1]
     1,2,0,3,0  missing?
     3 1 1 7 1  dup xor missing should equal 1
    xor = 0 xor 1
    Go through and find all items where bit 0 of result != bit 0 of index
    But they're not in their correct positions.  If they were this would be
    a really easy question, could just search for an index whose value is not it's index.

     0 1 2 3 4
     0 1 0 1 0

     000
     001
     010
     011
     100
     101
     110

     xor consecutive numbers?
     001
     001
     010
     011
     100
     ===
     101
     odd number of numbers that have 4's digit
     even number of numbers that have 2's digit
     odd number of numbers that have 1's digit






















    n = 5
    first 4 numbers
    [0,1,2,3,4]
    [0,1,2,3,0]
     x x x x
    [1,-3,2,-0,0]
    3 is missing!
    one is missing and one is duplicated.

    If we sort the numbers we'll find the missing and duplicated easily by scanning through.
    eg. duplicated number appears twice in a row and missing number is preceeded by a number 2 less than it, not 1.


    sum numbers... the expected result is sum(0, n-1) = m(m+1)/2 where m=n-1
    so sum = n(n-1)/2 = 5(4)/2 = 20/2 = 10
    instead we get 7

    We could find the solution by solving two simultaneous equations.
    7 + missing - duplicate = 10
    diff = 10-7 = 3
    difference between missing and duplicate is 3

    if we xor 0->n-1 with the vals in A we will get
    missing xor duplicate = 0b100 xor 0b000 = 0b100 = 4

    missing xor duplicate = X
    missing - duplicate = Y
    missing = y - duplicate
    missing = y + duplicate

    (Y + duplicate) xor duplicate = X
    Y xor duplicate + duplicate xor duplicate = X   Can we do this???  No!!! This is not true!
    Y xor duplicate = X

    (1 + 1) xor 1 ?= 1 xor 1 + 1 xor 1
    2 xor 1 ?= 0 + 0
    3 ?= 0   FALSE


    (a-b) xor c == a xor c - b xor c

    Y xor duplicate = X
    Y xor X == duplicate

    Y xor X == duplicate
    7 xor 3 = duplicate
    0b111 xor 0b011 = 0b100 = 4
    duplicate = 4
    missing = Y + duplicate
    missing = 3 + 4 = 7

    commutivity or commutativity?
    commutativity for binary relations vs operators like + and -



    xor numbers and expected
    find index of a 1 bit in that number
    iterate through numbers again and xor numbers that have a 1 in that bit
    iterate through expected again and xor numbers that have a 1 in that bit
    the result is either missing or extra.  If it's in the list it's extra otherwise it's missing.

    """

    # My second solution...
    n = len(A)
    # represents bits that differ between the missing and duplicate numbers
    diff_bits = functools.reduce(xor, itertools.chain(A, range(n)))
    mask = ((diff_bits - 1) ^ diff_bits) & diff_bits
    missing_or_duplicate = functools.reduce(xor, (x for x in itertools.chain(A, range(n)) if x & mask))
    if missing_or_duplicate in A:
        return DuplicateAndMissing(missing_or_duplicate, missing_or_duplicate ^ diff_bits)
    else:
        return DuplicateAndMissing(missing_or_duplicate ^ diff_bits, missing_or_duplicate)





    # My first solution
    n = len(A)
    calc_value = int((n * (n - 1) / 2) - sum(A))
    for orig_idx, orig_val in enumerate(A):
        cur_idx, cur_val = orig_idx, orig_val
        while cur_idx != cur_val:
            next_val = A[cur_val]
            A[cur_val] = cur_val
            cur_idx, cur_val = cur_val, next_val
    for i in range(n):
        if A[i] != i:
            return DuplicateAndMissing(i - calc_value, i)


def res_printer(prop, value):
    def fmt(x):
        return "duplicate: {}, missing: {}".format(x[0], x[1]) if x else None

    return fmt(value) if prop in (PropertyName.EXPECTED, PropertyName.RESULT) else value


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "search_for_missing_element.py",
            "find_missing_and_duplicate.tsv",
            find_duplicate_missing,
            res_printer=res_printer,
        )
    )

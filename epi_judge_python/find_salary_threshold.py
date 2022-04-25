from typing import List

from test_framework import generic_test


def find_salary_cap(target_payroll: int, current_salaries: List[int]) -> float:
    """
    Start: 10:25
    Ok we have to find this 'salary cap'.  What's not clear is what we're trying to optimise for.
    Are we trying to find a cap such that the capped salaries equal the target payroll?
    Or are we trying to find the cap that gives the largest sum of current salaries that's less than or equal to
    the target payroll?
    My bet is that it's the second one.

    90,30,100,40,20
    t=210
    20,30,40,90,100
    20 + 4*? = 210
    (210 - 20) / 4 = 190/4 ~ 50
    20+30 = 50
    50 + 3 * ? = 210
    (210-50) / 3 = 160 / 3 = 5x
    20 + 30 + 40 = 90
    90 + 2* ? = 210
    (210-90) / 2 = 120/2 = 60

    O(n log n) for the sort then O(n) for the search
    There may be a simpler way.
    The part where I say 'check if the result is between this number and the next number' feels arbitrary and I don't
    understand it.

    50,50,100 -> sum = 200
    target = 100

    ans = 33.333

    20,20,100 -> sum = 200
    target = 100
    ans = 60

    running_sum = 0
    num_left = len(current_salaries)
    possible_cap = (target_payroll - running_sum) / num_left
    for salary in current_salaries:
        if possible_cap < salary:
            return possible_cap
        running_sum += salary
        num_left -= 1
        possible_cap = (target_payroll - running_sum) / num_left
    return possible_cap

    Finished: 10:56
    The tests suggested a slightly more detailed interface than the questions specifies.
    In the tests, if the total sum equals the target payroll, we should return the largest salary as the cap.
    In the tests, if the total sum exceeds the target payroll, we should return -1.
    In my view in both of these cases it doesn't matter what we return as long as the cap is larger than or equal
    to the largest salary.
    """
    running_sum = 0
    num_left = len(current_salaries)
    possible_cap = (target_payroll - running_sum) / num_left
    for salary in sorted(current_salaries):
        if possible_cap < salary:
            return possible_cap
        running_sum += salary
        num_left -= 1
        if num_left == 0:
            if running_sum == target_payroll:
                return salary
            else:
                return -1
        possible_cap = (target_payroll - running_sum) / num_left
    return possible_cap


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('find_salary_threshold.py',
                                       'find_salary_threshold.tsv',
                                       find_salary_cap))

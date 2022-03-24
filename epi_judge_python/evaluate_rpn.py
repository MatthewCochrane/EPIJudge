from operator import add, sub, mul

from test_framework import generic_test


def evaluate(expression: str) -> int:
    """
    Start: 11:37

    Example
        "12"
        result = 12

    Example
        "-5"
        result = 5

    Example
        ""
        result = 0 ??? not sure about this case

    Example
        "1,2,+"
        result = 3
        working
        work from right to left
        pop the +
        now we know we're doing an operation (+)
        pop the , now we're looking at the second operand
        pop the 2 -> second operand += 2 = 2
        pop the -> second operand is finalized = 2
        pop the 1 -> first operand += 1 = 1
        hit the start -> finalize first operand
        perform the operation 1 + 2 = 3 and return 3

    Example
        10,8,2,-,+
        result = 10 + ( 8 - 2 ) = 10 + 6 = 16
        stack of operations: [(+, 10, 6)] -> (operator, left, right)
        parts = str.split(',')
        parts.pop() = + -> operator.append((+, 0, 0))
            parts.pop() = - -> operator.append(-,0,0)
            parts.pop() = 2 -> right = 2
            parts.pop() = 8 -> left = 8
            return 8 - 2 = 6
        right = 6
        parts.pop = 10
        return 10 + 6 = 16

    Pseudo code
        operator_functions = {"+": add, "-": subtract, "*": multiply, "/": divide}
        def RPN(parts: List[str]) -> int:
            part1 = parts.pop() # if this failed we have invalid syntax, could raise a more useful error...
            if part is an integer (possibly negative):
                return it as an int

            rhs = RPN(parts)
            lhs = RPN(parts)
            operator = operator_functions[operator] # if this failed we have used an invalid operator
            return operator(lhs, rhs)
        parts = input.split(',')
        return RPN(parts)

    O(n) space for 'parts' array + O(n) space for the call stack
    O(n) space overall
    O(n) time -> process each character once in the split then once in the recursive calls.

    Max call stack is about 2,000
    We have a call with 200000 items.
    We need to rewrite our algorithm iteratively instead of recursively.
    Pretty easy, just push to a stack instead of the call stack.

    Pseudo code
    parts = split expression
    processing = [] # (operator, rhs) - don't need lhs
    while parts:
        p1 = parts.pop()
        if it's an operator, append a new frame to the processing stack:
        while it's a number:
            if the stack is empty:
                return the number
            elif top stack's rhs is None:
                put it there
                break
            elif the top stack lhs is None:
                put it there,
                then evaluate the expression
                pop it from stack
                then set the number to the result

    6
    ops = []

    Finish 12:41 -> about an hour.  A tad too slow.  Should repeat.

    Holy crap, in their solution they process the string from left to right instead of from right to left.
    I think right to left is easier for recursive but looks like left to right is way easier for iterative!?
    This is something to do with top down vs bottom up???
    I should come back to this later today and repeat this way!
    """
    # had a 'bug' here too, was using regular division instead of integer division but
    # we are only working with integers.
    operator_functions = {"+": add, "-": sub, "*": mul, "/": lambda x, y: x // y}
    operations = []  # lists of [operator, rhs]
    parts = expression.split(",")
    while parts:
        part = parts.pop()
        if part in operator_functions:
            operations.append([operator_functions[part], None])
        else:
            num = int(part)
            # Had a silly bug here, put while num, which obviously exits on 0
            while True:
                if not operations:
                    # the final result
                    return num
                elif operations[-1][1] is None:
                    operations[-1][1] = num
                    break
                else:
                    operator, rhs = operations.pop()
                    num = operator(num, rhs)
    # Recursive approach - got stack overflow
    # def eval_RPN(parts: List[str]) -> int:
    #     print(len(parts))
    #     part1 = parts.pop()
    #     try:
    #         return int(part1)
    #     except ValueError:
    #         pass
    #
    #     operator = operator_functions[part1]
    #     rhs = eval_RPN(parts)
    #     lhs = eval_RPN(parts)
    #     return operator(lhs, rhs)
    #
    # return eval_RPN(expression.split(","))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main("evaluate_rpn.py", "evaluate_rpn.tsv", evaluate)
    )

from test_framework import generic_test
from test_framework.test_failure import TestFailure


class Stack:
    """
    Start: 10:38
    Create a stack with a max operation

    Example:
        s = stack()
        s.push(1)
        s.push(2)
        assert s.max() == 2
        s.push(10)
        assert s.max() == 10
        s.pop()
        assert s.max() = 2

    Option 1
        We can use O(n) space for the data.  Then update the max with every push.
        When doing a pop() we need to do an O(n) search for the next largest.
        Time complexities
        push() -> O(1)
        max() -> O(1)
        pop() -> O(n)

    Option 2
        We can naively just calculate the max on every call to max
        Time complexities
        push() -> O(1)
        pop() -> O(1)
        max() -> O(n)

    Option 3
        We could use an extra max-heap along with the stack
        Extra O(n) space complexity
        push() -> O(1)
        max() -> O(1)
        pop() -> O(n log n)

    Option 4
        Store a list of maximums including equal?

        eg.
            stack = [1, 5]
            maxs = [1, 5]
            push(1)
            push(5)
            push(2)
            push(5)
            push(0)
            max() == 5 (maxs[-1])
            pop() == 0 -> 0 < maxs[-1] so don't pop from maxs
            max() == 5 (maxs[-1])
            pop() == 5 -> 0 == maxs[-1] so pop from maxs too
            max() == 5 (maxs[-1])
            push(10)
            pop() == 10
            pop() == 2
            max() == 5

        Space complexity is O(n) - if we had increasing items or equal items
        Time complexity
        push() - O(1)
        pop() - O(1)
        max() - O(1)

    What should max do if empty?
    What should pop do if empty?  Probably the same thing as a list?
    I'd like to inherit from List and use it's functionality, though we are changing it's interface a bit.
    (eg with push instead of append)

    Raise index error if empty
    no peak function

    Finish: 11:09 - 30 mins
    Had a few bugs.  I should probably repeat this question!
    """

    def __init__(self):
        self._stack = []
        self._maximums = []

    def empty(self) -> bool:
        return len(self._stack) == 0

    def max(self) -> int:
        """
        if empty:
            raise IndexError
        return _max[-1]
        """
        if self.empty():
            raise IndexError
        return self._maximums[-1]

    def pop(self) -> int:
        """
        pop from _stack (will raise indexerror if empty)
        if popped val == max():
            pop from _max
        return popped value
        """
        val = self._stack.pop()
        if val == self._maximums[-1]:
            self._maximums.pop()
        return val

    def push(self, x: int) -> None:
        """
        append to _stack
        if empty or x >= max():
            append to _max
        """
        if self.empty() or x >= self.max():
            self._maximums.append(x)
        self._stack.append(x)


def stack_tester(ops):
    try:
        s = Stack()

        for (op, arg) in ops:
            if op == "Stack":
                s = Stack()
            elif op == "push":
                s.push(arg)
            elif op == "pop":
                result = s.pop()
                if result != arg:
                    raise TestFailure(
                        "Pop: expected " + str(arg) + ", got " + str(result)
                    )
            elif op == "max":
                result = s.max()
                if result != arg:
                    raise TestFailure(
                        "Max: expected " + str(arg) + ", got " + str(result)
                    )
            elif op == "empty":
                result = int(s.empty())
                if result != arg:
                    raise TestFailure(
                        "Empty: expected " + str(arg) + ", got " + str(result)
                    )
            else:
                raise RuntimeError("Unsupported stack operation: " + op)
    except IndexError:
        raise TestFailure("Unexpected IndexError exception")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "stack_with_max.py", "stack_with_max.tsv", stack_tester
        )
    )

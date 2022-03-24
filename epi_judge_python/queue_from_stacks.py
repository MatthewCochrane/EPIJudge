from test_framework import generic_test
from test_framework.test_failure import TestFailure

"""
Start: 19:37

Implement a queue with stacks.

enq() and deq()

stack = []
stack2 = [3, 2, 1]
enq(1)
enq(2)
enq(3)
deq() == 1
enq(4)
enq(5)
deq() == 2
deq() == 3
deq() == 4


Approach
Fill stack 1 when we call enq
when we want to deq, pop from stack 2 if it's available, otherwise
pop each item from stack 1 and push it to stack 2, then pop the last item from stack 2

Every item gets pushed onto stack 1, popped off stack 1, pushed onto stack 2 and popped off stack 2.
Therefore the average time complexity of deq() operations is O(1)
Space complexity is O(n) -> we store each item in one place.
The worst case time complexity of deq is O(n) when we have to do the shuffle

All tests pass first run so that's good...
Time: 19:46
10 mins...  Nice
"""


class Queue:
    def __init__(self):
        self._in = []
        self._out = []

    def enqueue(self, x: int) -> None:
        self._in.append(x)

    def dequeue(self) -> int:
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())
        return self._out.pop()


def queue_tester(ops):
    try:
        q = Queue()

        for (op, arg) in ops:
            if op == "Queue":
                q = Queue()
            elif op == "enqueue":
                q.enqueue(arg)
            elif op == "dequeue":
                result = q.dequeue()
                if result != arg:
                    raise TestFailure(
                        "Dequeue: expected " + str(arg) + ", got " + str(result)
                    )
            else:
                raise RuntimeError("Unsupported queue operation: " + op)
    except IndexError:
        raise TestFailure("Unexpected IndexError exception")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "queue_from_stacks.py", "queue_from_stacks.tsv", queue_tester
        )
    )

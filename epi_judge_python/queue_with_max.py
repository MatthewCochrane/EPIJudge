from collections import deque

from test_framework import generic_test
from test_framework.test_failure import TestFailure

"""
Start: 19:50
Create a queue with enq, deq and max

max returns the max item in the queue

Example
    e1, e2, e3, e9, e5, e6, e0, e4, e7
  ??, m1, m2, m3, m9, m9, m9, m9, m9 
    d1, d2, d3, d9, d5, d6, d0, d4
      m9, m9, m9, m6, m6, m4, m4, ??

enqueues
maxq = [1]
maxq = [2]
maxq = [3]
maxq = [9]
maxq = [9, 5]
maxq = [9, 6]
maxq = [9, 6, 0]
maxq = [9, 6, 4]
maxq = [9, 7] 
dequeue
1 maxq = [9, 6, 4]
2 maxq = [9, 6, 4]
3 maxq = [9, 6, 4]
9 maxq = [6, 4]
5 maxq = [6, 4]
6 maxq = [4]
0 maxq = [4]
4 maxq = []

Queue for the max
if enq(x) x > max, replace it
if enx(x) < max, append it

Pause at 19:57
Resume at 20:14 - 17 mins break

Space complexity is O(n) extra for maxq.  Worst case is decreasing array.
An increasing array only stores one value!

Finish: 20:36
About 30 mins total.
Made a mistake with my logic and didn't see that we needed to keep popping the item off the queue when enqueueing.
"""


class QueueWithMax:
    def __init__(self):
        self._q = deque()
        self._maxq = deque()

    def enqueue(self, x: int) -> None:
        """
        _q.append(x)
        if maxq is empty or x < maxq tail ([-1]):
            maxq.append(x)
        else: # x >= last maxq
            replace last maxq with x
        O(n) time worst case
        O(1) average case
        """
        self._q.append(x)
        while self._maxq and x > self._maxq[-1]:
            self._maxq.pop()
        self._maxq.append(x)

    def dequeue(self) -> int:
        """
        val = _q.popleft()
        if val == head of maxq:
            pop head of maxq
        O(1) time
        """
        val = self._q.popleft()
        if val == self._maxq[0]:
            self._maxq.popleft()
        return val

    def max(self) -> int:
        return self._maxq[0]


def queue_tester(ops):

    try:
        q = QueueWithMax()

        for (op, arg) in ops:
            if op == "QueueWithMax":
                q = QueueWithMax()
            elif op == "enqueue":
                q.enqueue(arg)
            elif op == "dequeue":
                result = q.dequeue()
                if result != arg:
                    raise TestFailure(
                        "Dequeue: expected " + str(arg) + ", got " + str(result)
                    )
            elif op == "max":
                result = q.max()
                if result != arg:
                    raise TestFailure(
                        "Max: expected " + str(arg) + ", got " + str(result)
                    )
            else:
                raise RuntimeError("Unsupported queue operation: " + op)
    except IndexError:
        raise TestFailure("Unexpected IndexError exception")


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "queue_with_max.py", "queue_with_max.tsv", queue_tester
        )
    )

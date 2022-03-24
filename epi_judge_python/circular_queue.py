from itertools import islice
from typing import Optional, List

from test_framework import generic_test
from test_framework.test_failure import TestFailure

"""
Start: 16:58

We want to build a 'cicrular queue'.  It looks like a queue, it's implemented
with a circular array and some pointers for the head/tail.

The idea
start with a list with some capacity
cap = 5
8 X |2 2 1
  t h   
2 2 1 8 X X X X X
h       t
q.enq(1)
q.enq(5)
...
q.deq() == 1
q.deq() == 5
q.enq(8)

Pseudo code
enqueue:
    # If adding makes it full, resize now.  
    # Avoid the ambiguity of not knowing if full/empty because the pointers # are at the same place
    if size + 1 == cap:
        resize(cap*2)
    set value at tail
    increment tail to length mod capacity

dequeue
    if size == 0:
        error
    val = value at head
    increment head and mode with capacity
    # potentially want to dynamically resize smaller at some point?
    return val

size
    # edge case -> if size = cap this won't work, need a flag, or avoid hitting cap!
    # ((tail - head) + cap ) % cap
    res = (tail - head)
    return res + cap if res < 0 else res

resize
    create new list of new cap
    copy from head to end into new list (extend)
    copy from start up until tail into new list (extend)
    head = 0
    tail = size
    assign the temp vars to the real vars
        

enqueue -> O(1) average, O(n) worst case when resizing
dequeue -> O(1)
size -> O(1)
17:22


Ok, finished at 18:04 with a lot of debugging.  Absolutely need to redo this question!
"""


class Queue:
    def __init__(self, capacity: int) -> None:
        self._cap = capacity
        self._data: List[Optional[int]] = [None] * self._cap
        self._head_idx = 0
        self._tail_idx = 0

    def enqueue(self, x: int) -> None:
        if self.size() + 1 == self._cap:
            self._double_capacity()
        self._data[self._tail_idx] = x
        self._tail_idx += 1
        self._tail_idx %= self._cap

    def dequeue(self) -> int:
        if self.size() == 0:
            raise IndexError
        val = self._data[self._head_idx]
        # potentially want to dynamically resize smaller at some point?
        self._head_idx += 1
        self._head_idx %= self._cap
        return val

    def size(self) -> int:
        # Works because we never allow the size to equal the capacity.  We resize when we have 1 slot free.
        return ((self._tail_idx - self._head_idx) + self._cap) % self._cap

    def _double_capacity(self):
        # 0 1 2 3 4 5 cap=6
        # 1 2 X 4 5 6
        #     t h
        # X X X X X X X X X X X X
        # 4 5 6 1 2 X
        # h         t

        # X 2 3 4 X X
        #   h     t
        # 2 3 4 X X X X X X X X X
        # 0 1 2 3 4 5
        # h     t

        # 0 1 2 3
        #   |     x cap = 4

        # This is a nicer way to do it. Does the same thing as the commented out bit below.
        # The idea is:
        # Rearrange the existing data into a new list of the same size
        # Double the length by extending it with a new array of None values of the same length
        self._data = self._data[self._head_idx :] + self._data[: self._head_idx]
        self._head_idx, self._tail_idx = 0, self.size()
        self._data.extend([None] * self._cap)
        self._cap *= 2

        # new_capacity = self._cap * 2
        # new_data: List[Optional[int]] = [None] * new_capacity
        # if self._head_idx > self._tail_idx:
        #     # is slice assignment with an islice efficient???
        #     new_data[: self._cap - self._head_idx] = islice(
        #         self._data, self._head_idx, self._cap
        #     )
        #     new_data[self._cap - self._head_idx : self.size()] = islice(
        #         self._data, self._tail_idx
        #     )
        # else:
        #     new_data[: self.size()] = islice(self._data, self._head_idx, self._tail_idx)
        # self._head_idx, self._tail_idx = 0, self.size()
        # self._data, self._cap = new_data, new_capacity


def queue_tester(ops):
    q = Queue(1)

    for (op, arg) in ops:
        if op == "Queue":
            q = Queue(arg)
        elif op == "enqueue":
            q.enqueue(arg)
        elif op == "dequeue":
            result = q.dequeue()
            if result != arg:
                raise TestFailure(
                    "Dequeue: expected " + str(arg) + ", got " + str(result)
                )
        elif op == "size":
            result = q.size()
            if result != arg:
                raise TestFailure("Size: expected " + str(arg) + ", got " + str(result))
        else:
            raise RuntimeError("Unsupported queue operation: " + op)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "circular_queue.py", "circular_queue.tsv", queue_tester
        )
    )

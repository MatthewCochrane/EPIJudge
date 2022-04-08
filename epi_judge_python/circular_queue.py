from typing import Optional, List

from test_framework import generic_test
from test_framework.test_failure import TestFailure

"""
Repeating this question as it was tricky last time...
Time: 9:45

Use an array to implement a circular buffer (circular queue).
The queue should dynamically resize if we exceed the capacity.

cap = 5
0 1 2 3 4
2,3,5,7,X
h t     

enqueue at the head
dequeue from the tail

when empty we'd expect head and tail to be at the same place
interestingly this is the same when the queue is full!

def __init__(capacity)
    if cap == 0 raise error
    ary = [None] * capacity
    head = tail = 0
    size = 0
    
def enqueue(val):
    if size == capacity: raise exception -> full
    ary[head] = val
    head += 1
    head %= capacity
    size += 1

def dequeue():
    if size == 0 raise an exception IndexError
    val = ary[tail]
    tail += 1
    tail %= capacity
    size -= 1
    return val

def size()
    return size

def resize():
    if tail < head:
        move from tail to head-1 into start of array
    else: # head <= tail
        move ary[tail:] to start of array
        move ary[:h] to start after the tail bit
        ary[:size] = ary[tail:] + ary[:head]
        

add empty values to the end of the array
    
    
    
Pseudo without resizing at 9:56    

0,1,2,3,4,5,6,7,8
    h     t
5,6,7,8,0,1,2,X,X
    t h
2,3,X,X,X,X,X,X,X
    th  full
2,3,4,5,6,7,8,0,1

assume that it's not empty!
   
if tail < head:
    move from tail to head-1 into start of array
else: # head <= tail
    move ary[tail:] to start of array
    move ary[:h] to start after the tail bit

add empty values to the end of the array

All tests passed.
Finished at 10:21
36 mins


Better...

"""

def test_queue():
    q = Queue(4)
    assert q.size() == 0
    q.enqueue(1)
    assert q.size() == 1
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    print(q._ary)
    q.enqueue(5)
    q.enqueue(6)
    q.enqueue(7)
    q.enqueue(8)
    q.enqueue(9)
    print(q._ary)
    assert q.dequeue() == 5
    print("PASS")


class Queue:
    def __init__(self, capacity: int) -> None:
        if capacity == 0:
            raise ValueError()
        self._capacity = capacity
        self._ary = [0] * self._capacity
        self._head = self._tail = 0
        self._size = 0

    def enqueue(self, x: int) -> None:
        if self._size == self._capacity:
            self._resize()
        self._ary[self._head] = x
        self._head += 1
        self._head %= self._capacity
        self._size += 1

    def dequeue(self) -> int:
        if self._size == 0:
            raise IndexError()
        x = self._ary[self._tail]
        self._tail += 1
        self._tail %= self._capacity
        self._size -= 1
        return x

    def size(self) -> int:
        return self._size

    def _resize(self) -> None:
        if self._tail < self._head:
            self._ary[: self._size] = self._ary[self._tail : self._head]
        else:  # head <= tail
            self._ary[: self._size] = self._ary[self._tail :] + self._ary[: self._head]
        self._head = self._size
        self._tail = 0
        self._ary += [0] * self._capacity
        self._capacity *= 2


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


class Queue_FirstGo:
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

import functools
from typing import List, Optional, Iterator

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def reconstruct_preorder(preorder: List[int]) -> BinaryTreeNode:
    """
    Start: 7:52

    Example:
        [1, None, None]
             1
           X  X

        [1, 2, X, X, X]
           1
         2  X
        X X

        [1, None, 2]
           1
          X 2

        [1, 2, X, 4, 6, X, X, X, 3, 5, X, X, X]
               1
            2    3
          X  4  5 X
            6 XX X
           X X

    When we see a number that's not None, we know it's the next root node

    Simply, the algorithm would look like this
    It takes advantage of the fact that the order is pre-order so self, left, right.  And that
    all subtrees are terminated so we know when they end in the string.

    def make_tree(ary):
        consume an item from the start of ary
        if item is None:
            return None
        Create tree node from consumed item
        node.left = make_tree(ary) # ary was mutated before this call
        node.right = make_tree(ary) #ary was mutated...
        return node


    O(N) time, call make_tree once for each item in the tree.
    O(h) space

    All tests pass first run.
    Finish: 8:12
    20 mins

    This is a very practical question.
    I like the use of iterators and how you have to understand the difference between an iterable and an iterator
    to get this neat solution that doesn't use an index variable.
    Again, this is almost exactly the same solution from the book.
    """

    def construct_preorder(it: Iterator[Optional[int]]) -> Optional[BinaryTreeNode]:
        # Don't need to catch the exception the input list expected to be well-formed
        # otherwise we'll see a StopIteration exception.
        val = next(it)
        if val is None:
            return None
        node = BinaryTreeNode(val)
        node.left = construct_preorder(it)
        node.right = construct_preorder(it)
        return node

    return construct_preorder(iter(preorder))


@enable_executor_hook
def reconstruct_preorder_wrapper(executor, data):
    data = [None if x == "null" else int(x) for x in data]
    return executor.run(functools.partial(reconstruct_preorder, data))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_from_preorder_with_null.py",
            "tree_from_preorder_with_null.tsv",
            reconstruct_preorder_wrapper,
        )
    )

import functools
from typing import Optional

from binary_tree_with_parent_prototype import BinaryTreeNode
from test_framework import generic_test
from test_framework.binary_tree_utils import must_find_node
from test_framework.test_utils import enable_executor_hook


def find_successor(node: BinaryTreeNode) -> Optional[BinaryTreeNode]:
    """
    Start: 14:34
    The successor of a node in a bt is the node that appears immediately after the given node in an in-order traversal.
    Each node stores a parent
    Compute the successor of the node

    Example
          a
        b   c
        b's successor is a
        a's successor is c
        c's successor is None

          a
       b      c
     d          e
              f  g
    dbacfeg

    in order is left self right
    if node.right:
        node = node.right
        while node.left:
            node = node.left
        return node
    if it doesn't have a right node, look at the parent, if it doesn't have a parent return None
    while there is a parent node:
        if we're the left node of the parent, chose the parent
        node = node.parent
    return None

    O(h) time worst case
    O(1) space

    if there's any recursive parent where we're the left, go to it next.

       1
     2  3
    4 5

    Time: 15:03
    Had a pretty solid bug.  Missed a major case of what happens if we need to step up multiple parents.
    Should repeat this question, it's tricky and cool!
    Trickier question than it looks like! Seems like a really good interview question :)

    Again, almost exactly the same code as the book's solution.
    """
    if node is None:
        return None
    if node.right:
        # If there's a right node, follow it to next successor
        node = node.right
        while node.left:
            node = node.left
        return node
    while node.parent:
        if node.parent.left == node:
            # If we don't have a right and we are the left node of our parent
            return node.parent
        node = node.parent
    # Must the last node in the in order traversal
    return None


@enable_executor_hook
def find_successor_wrapper(executor, tree, node_idx):
    node = must_find_node(tree, node_idx)

    result = executor.run(functools.partial(find_successor, node))

    return result.data if result else -1


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "successor_in_tree.py", "successor_in_tree.tsv", find_successor_wrapper
        )
    )

import functools
from typing import Optional

from binary_tree_with_parent_prototype import BinaryTreeNode
from test_framework import generic_test
from test_framework.binary_tree_utils import must_find_node
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def lca(node0: BinaryTreeNode, node1: BinaryTreeNode) -> Optional[BinaryTreeNode]:
    """
    Start: 11:27
    Compute the LCA when the nodes have a parent pointer.

         a
      b    c
    d  e    h
             f
    LCA of d and f is b
    LCA of d and d is d

    if we can find f and d and also keep track of the level they are on...
    Then step the lower level one up the the same level as the other
    step the two parents together until you find a common node

    Pseudo code
    while the levels are not the same, step lower level node up one and decrement its level
    while they are not the same, step them both to their parent
    return the equal nodes
    O(h) space, O(n) time

    have the nodes already!!
    can do in O(1) space, O(h) time
    Pseudo code
    find the level of each node, keep stepping up until None
        # root node is on level 0
        level = -1
        while node:
            level += 1
            node = node.parent
    while the levels are not the same, step lower level node up one and decrement its level
    while they are not the same, step them both to their parent
    return the equal nodes

    All tests passed first run.
    Finish: 11:45
    18 mins

    One mistake I made here was not to look at the function signature.  I would have saved myself
    5-10 mins if I had of looked at it...

    This is basically exactly the same code as their solution!  Pretty interesting!
    """

    def get_level(node: Optional[BinaryTreeNode]) -> int:
        # root node is on level 0
        level = -1
        while node:
            level += 1
            node = node.parent
        return level

    level0, level1 = get_level(node0), get_level(node1)
    if level1 > level0:
        level1, level0 = level0, level1
        node1, node0 = node0, node1
    # 0 is lower (greater) than 1 or they are equal
    while level0 > level1:
        level0 -= 1
        node0 = node0.parent
    while node0 != node1:
        node0, node1 = node0.parent, node1.parent
    return node0


@enable_executor_hook
def lca_wrapper(executor, tree, node0, node1):
    result = executor.run(
        functools.partial(lca, must_find_node(tree, node0), must_find_node(tree, node1))
    )

    if result is None:
        raise TestFailure("Result can't be None")
    return result.data


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "lowest_common_ancestor_with_parent.py",
            "lowest_common_ancestor.tsv",
            lca_wrapper,
        )
    )

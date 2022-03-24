from collections import namedtuple
from typing import Tuple, Optional, NamedTuple

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def is_balanced_binary_tree(tree: BinaryTreeNode) -> bool:
    """
    Start: 20:55
    Is tree balanced.
    A tree is balanced if for each node, the difference in height of the
    left and right subtrees is at most 1.

    Examples
        1 -> True

          2
        1   1   True

          2
        1      True

          3
        2      False
      1  1

    One way is to recursively search the tree, for each node, return the height of the subtrees?
    for each node, return (height, balanced)

    Pseudo code:
    def node_balanced(node) -> Tuple[height, balanced]:
        if node is None:
            return 0, true
        if l or r is not balanced:
            return (?, false)
        return max(lheight, rheight) + 1, abs(l height - r height) <= 1
    return node_balanced(root)[1]

    O(n) time -> visit each node once
    O(height) space

    Finished: 21:13
    18 mins.  Pretty good.  Could be faster for this pretty simple problem.
    Missed test case with null tree.
    That's because normally I use a base case for null instead of the check in the leaves.
    Good one to remember...

    I was wondering if there was a way to simplify this a bit, but they used the same approach.

    I updated slightly to use a named tuple instead of a tuple.  I think I preferred the tuple honestly.
    """

    class HeightAndBalanced(NamedTuple):
        height: int
        balanced: bool

    def node_height_and_balanced(node: Optional[BinaryTreeNode]) -> HeightAndBalanced:
        l = (
            node_height_and_balanced(node.left)
            if node.left
            else HeightAndBalanced(0, True)
        )
        r = (
            node_height_and_balanced(node.right)
            if (
                node.right and l.balanced
            )  # improvement here, skip searching right subtree if left wasn't balanced!
            else HeightAndBalanced(0, True)
        )
        return HeightAndBalanced(
            max(l.height, r.height) + 1,
            l.balanced and r.balanced and abs(l.height - r.height) <= 1,
        )

    if not tree:
        return True
    return node_height_and_balanced(tree)[1]


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_tree_balanced.py", "is_tree_balanced.tsv", is_balanced_binary_tree
        )
    )

from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def preorder_traversal(tree: BinaryTreeNode) -> List[int]:
    """
    Start: 13:33
    Perform an iterative preorder traversal

        1
      2  3
    5   3 4
           6
    1, 2, 5, 3, 3, 4, 6

      1
     a 2
      a 3
       a 4

       1
     a    2
    w  z  b    3
                4
         1
        2 a
       3 b
      4 c

    preorder = self, left, right

    next_right
    stack = []
    while stack:
        node = stack.pop
        visit node
        push right and left onto stack if not none

    O(n) time
    O(h) space
    Again forgot to append node.data to result, was appending node
    Finish: 13:46
    13 mins.

    """
    if not tree:
        return []
    stack = [tree]
    result = []
    while stack:
        node = stack.pop()
        result.append(node.data)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_preorder.py", "tree_preorder.tsv", preorder_traversal
        )
    )

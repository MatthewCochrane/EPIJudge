from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def inorder_traversal(tree: BinaryTreeNode) -> List[int]:
    """
    Start: 13:01

    In order traversal without recursion.  Ie iterative.

    Example
        1
     2    3
    4    5
        6 7
    Answer = 4,2,1,6,5,7,3

    in order = left, self, right

    use a stack
    stack =
    ans = 4, 2, 1, 6, 5, 7, 3
    node = none

    stack = []
    answer = []
    node = tree
    while node or stack:
        if node:
            stack.append(node)
            node = node.left
        else:
            node = stack.pop()
            answer.append(node)
            node = node.right
    return answer
      1
    2  4

    O(n) time
    O(h) space - max stack size is height of the tree
    Finish: 13:15
    Nice. You worked that out, didn't just memorise it.
    """
    stack = []
    answer = []
    node = tree
    while node or stack:
        if node:
            stack.append(node)
            node = node.left
        else:
            node = stack.pop()
            answer.append(node.data)
            node = node.right
    return answer


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_inorder.py", "tree_inorder.tsv", inorder_traversal
        )
    )

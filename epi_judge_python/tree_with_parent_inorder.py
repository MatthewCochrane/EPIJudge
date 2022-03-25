from typing import List

from binary_tree_with_parent_prototype import BinaryTreeNode
from successor_in_tree import find_successor
from test_framework import generic_test


def inorder_traversal(tree: BinaryTreeNode) -> List[int]:
    # Kinda cheated.. Reused the previous question's answer.
    if not tree:
        return []
    result = []
    node = tree
    while node.left:
        node = node.left
    while node:
        result.append(node.data)
        node = find_successor(node)
    return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_with_parent_inorder.py",
            "tree_with_parent_inorder.tsv",
            inorder_traversal,
        )
    )

import functools
from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def create_list_of_leaves(tree: BinaryTreeNode) -> List[BinaryTreeNode]:
    """
    Start: 16:35
    Leaves to LL

    Example 1
          1
        2  3
        Answer: 2->3

    Example 2
           1
        2    3
      4  5
        Answer: 4->5->3

    Ok, we want to enumerate the leaves from left to right.
    Thinking about traversals...
    Preorder... Inorder... Post Order...  All should work...
    Eg. do a preorder traversal and when we hit a node with no children, add it to the LL.

    Test example 2:
        4->5->3

    We always visit left before right which means that the left nodes always come before the right nodes.

    Pseudo Code:

    create dummy node
    def traverse():
        if we have no children:
            append to end of ll
            return
        if left:
            traverse(left)
        if right:
            traverse(right)
    if root:
        traverse(root)

    Finish: 16:51
    16 mins and it felt a bit slow
    Pretty easy question, took me a little while to be confident that my solution was correct.
    """
    leaves = []

    def traverse(node: BinaryTreeNode) -> None:
        if node.left is None and node.right is None:
            leaves.append(node)
            return
        if node.left:
            traverse(node.left)
        if node.right:
            traverse(node.right)

    if tree:
        traverse(tree)
    return leaves


@enable_executor_hook
def create_list_of_leaves_wrapper(executor, tree):
    result = executor.run(functools.partial(create_list_of_leaves, tree))

    if any(x is None for x in result):
        raise TestFailure("Result list can't contain None")
    return [x.data for x in result]


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_connect_leaves.py",
            "tree_connect_leaves.tsv",
            create_list_of_leaves_wrapper,
        )
    )

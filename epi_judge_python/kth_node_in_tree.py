import functools
from typing import Optional

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


class BinaryTreeNode:
    def __init__(self, data=None, left=None, right=None, size=None):
        self.data = data
        self.left = left
        self.right = right
        self.size = size


def find_kth_node_binary_tree(tree: BinaryTreeNode, k: int) -> Optional[BinaryTreeNode]:
    """
    Start: 13:50
    find the kth node

             a
        b        c
     d    e   f
        g
    kth node in inorder traversal
    inorder traversal: dbgeafc
    if k = 1 answer = d
    if k = 5 answer = a

    also know the size of the tree
             a7
        b4       c2
     d1   e2  f1
        g1

    if k = 5, then look at subtree size
    left_subtree_size = tree.left.size if tree.left else 0
    if k <= left subtree size:
        go left - recurse with same k and tree.left
    elif k == left subtree size + 1:
        return this node
    elif k <= tree size:
        go right recurse with k - left subtree size - 1
    else:
        invalid k, not enough nodes

    O(depth of answer) time
    O(depth of answer) space
    O(log n) time/space if balanced

    All passed
    Finish: 14:08
    18 mins
    Again, my code is almost identical to theirs.  Interesting..
    """
    if not tree:
        return None
    left_subtree_size = tree.left.size if tree.left else 0
    if k <= left_subtree_size:
        return find_kth_node_binary_tree(tree.left, k)
    elif k == left_subtree_size + 1:
        return tree
    elif k <= tree.size:
        return find_kth_node_binary_tree(tree.right, k - left_subtree_size - 1)
    # not enough nodes, k'th node not in tree
    return None


@enable_executor_hook
def find_kth_node_binary_tree_wrapper(executor, tree, k):
    def init_size(node):
        if not node:
            return 0
        node.size = 1 + init_size(node.left) + init_size(node.right)
        return node.size

    init_size(tree)

    result = executor.run(functools.partial(find_kth_node_binary_tree, tree, k))

    if not result:
        raise TestFailure("Result can't be None")
    return result.data


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "kth_node_in_tree.py",
            "kth_node_in_tree.tsv",
            find_kth_node_binary_tree_wrapper,
        )
    )

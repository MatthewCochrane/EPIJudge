from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def has_path_sum(tree: BinaryTreeNode, target: int) -> bool:
    """
    Start: 12:45
    is there a path to a *leaf* with that integer as it's path sum

    Example

       3
     2   5
    1 2   7

    6 7   15

    Can the integer node weights be negative?  The algorithm changes substantially if so.
    Assume weights can be negative.  We could cull a lot of the tree if not though...

    Pseudo code
    def has_path_sum(node, target) -> bool:
        new_target = target - node.data
        if node has no children:
            return new_target == 0

        return true if either left or right node has path sum to new_target
        # return has_path_sum(node.left, new_target) or has_path_sum(node.right, new_target)


    Finish: 12:59
    15 mins..
    One bug with the if condition...
    Didn't write great pseudo code...
    """
    if tree is None:
        return False
    new_target = target - tree.data
    if tree.left is None and tree.right is None:
        # If this is a leaf node
        return new_target == 0
    return has_path_sum(tree.left, new_target) or has_path_sum(tree.right, new_target)


if __name__ == "__main__":
    exit(generic_test.generic_test_main("path_sum.py", "path_sum.tsv", has_path_sum))

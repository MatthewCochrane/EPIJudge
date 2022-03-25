from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def sum_root_to_leaf(tree: BinaryTreeNode) -> int:
    """
    Start: 12:20

    Examples 1:
        1 -> sum = 1

    Example 2
        1
      0
        0
    sum = 100 = 4

    Example 3
        1
      0   0
    sum = 10 + 10 = 100 = 4

    Example
          1
       0
    1    0
     1

    sum = 1011 + 100 = 1111 = 15

    add to sum when hit leaf
    sum_tree(node, prefix=0) -> int:
        node_val = prefix << 1 + node.data
        if node.left is None and node.right is None:
            return node_val
        else:
            return (sum_tree(node.left, node_val) if node.left else 0) + (sum_tree(node.right + node_val) if node.right else 0)
    if tree is None:
        return 0
    return sum_tree(tree)


                  1
        0                   1
     0     1          0         0
    0 1      1            0         0
            0           1   0
                         1



    O(n) time, O(h) space
    Assuming the sum fits into a 64 bit int

    All tests pass
    Time: 12:41 -> 21 mins.  Pretty good.
    Had two small bugs.
    1. a typo + instead of ,
    2. got operator precedence wrong.
        a << 1 + b really means a << (1 + b)
        but I wanted
        (a << 1) + b
        so I had to add the brackets
    """

    def sum_tree(node: BinaryTreeNode, prefix=0) -> int:
        node_val = (prefix << 1) + node.data
        if node.left is None and node.right is None:
            return node_val
        else:
            return (sum_tree(node.left, node_val) if node.left else 0) + (
                sum_tree(node.right, node_val) if node.right else 0
            )

    if tree is None:
        return 0
    return sum_tree(tree)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "sum_root_to_leaf.py", "sum_root_to_leaf.tsv", sum_root_to_leaf
        )
    )

import functools
from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def exterior_binary_tree(tree: BinaryTreeNode) -> List[BinaryTreeNode]:
    """
    Start: 16:58

    Example 1
       1
       result = 1

    Example 2
         1
        2 3
        result = [1,2,3]

    Example 3
           1
         2  3
             4
        result = [1,2,4,3]

    Example 3b
           1
         2  3
           6 4
        result = [1,2,6,4,3]

    Example 4
           1
        2    3
      4  5  8
        6 7
        result = [1,2,4,6,7,8,3]

    Example 5
             4
          7       -8
        4   X    X  6
      X  -11
        1   X
      X  -5

                4
          7          4
           -11     1
         -5    X     -8
           6
        Result = [4,7,-11,-5,6,-8,4]

    Ex 6

             1
         2
       3   4
             5
        result = [1,2,3,5]
    Post order traversal
    Left, Right, Self
    so the idea is
    before the first leaf node, add every node to the result, these are the left nodes
    then add all the leaf nodes in order
    Then when you hit the last leaf node (how do you know this? - all rights) start adding
    Or, do an extra O(log n) bit at the end for the right side... just recurse to bottom and add on way back up

    init result
    def traverse(node):
        if no leaves yet or is leaf:
            seen_leaf = true if leaf
            add to result
        if left: recurse left
        if right: recurse right
    if root:
        traverse(root)

    def build_right(node):
        # reverse postorder traversal
        if right: traverse right
        if left and not seen_leaf: traverse left
        if not last_in_list:
            add to result
    if root:
        build_right(root)

    I just don't understand what they want in this question.
    What they ask for would end up with duplicate nodes in the
    result.
    Ask questions upfront!!
    There's some special definition of what the left side and
    right side are but it's not captured in the problem.
    This code is disgusting.  If I was able to understand
    the actual question I could have written much nicer code.

    Took like 1.5 hours... :(
    """
    result = []
    seen_leaf = False

    def left_and_bottom(node: BinaryTreeNode) -> None:
        nonlocal seen_leaf
        if node.left is None and node.right is None:
            # Bottom
            seen_leaf = True
            if node is not tree:
                result.append(node)
        elif not seen_leaf:
            # Left side
            result.append(node)
        if node.left:
            left_and_bottom(node.left)
        if node.right:
            left_and_bottom(node.right)

    if tree:
        if not tree.left:
            seen_leaf = True
            result.append(tree)
        left_and_bottom(tree)

    def right_side(node: BinaryTreeNode) -> None:
        nonlocal seen_leaf
        if node.right:
            right_side(node.right)
        if node.left and not seen_leaf:
            right_side(node.left)
        if node.left is None and node.right is None:
            seen_leaf = True
            # Don't add the bottom right corner twice.
            return
        if node is tree:
            # Don't add the root twice
            return
        result.append(node)

    if tree and tree.right:
        # Build the right side, don't add the root.
        seen_leaf = False
        right_side(tree.right)
    return result


def create_output_list(L):
    if any(l is None for l in L):
        raise TestFailure("Resulting list contains None")
    return [l.data for l in L]


@enable_executor_hook
def create_output_list_wrapper(executor, tree):
    result = executor.run(functools.partial(exterior_binary_tree, tree))

    return create_output_list(result)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_exterior.py", "tree_exterior.tsv", create_output_list_wrapper
        )
    )

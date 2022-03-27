from typing import List, Optional

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def binary_tree_from_preorder_inorder(
    preorder: List[int], inorder: List[int]
) -> BinaryTreeNode:
    """
    Start: 16:00
    Can we reconstruct a binary tree from a preorder and inorder traversal assuming the nodes have unique values.

    Example
                  1
            2          3
         4     5         7
             6             8
                         9
    Preorder: 1,2,4,5,6,3,7,8,9
    Inorder:  4,2,6,5,1,3,7,9,8

    Preorder: 3,7,8,9
    Inorder:  3,7,9,8

    Stack 1: end = None
    consumed = 1
    build left(end=1)
            1
       2
     4   5
        6





    def build(pre, in, end):
        consume from preorder
        if consumed != first in inorder:
            left tree = build(pre, in, consumed)

        consume equal val from in order

        if next item in inorder is end, return tree
        right tree = build(pre, in, end)
        return tree

        1
         3
    Preorder: 1,3
    Inorder:  1,3

        1
       2
    Preorder: 1,2
    Inorder:  2,1

        1
       2 3
    Preorder: 1,2,3
    Inorder:  2,1,3

    first element in pre-order is the root
    the next element is one of it's children but we don't know if it's left or right
    pre order - all of the left children come before any of the right children for each node
    when you see a node in the pre-order traversal, you've already seen it's parent

    first element in in order is the 'leftmost' item in the tree.
    inorder is left, self, right
    all of the left children come before the node
    all of the left children come before any of the right children
    the node itself comes before any of the right children
    when you see a node in the in-order traversal, you've already seen all of its left children
    when you see a node in the in-order traversal, if it's a right child, you've already seen it's parent

    Bit stuck what's a bad way to do this?

    looking at a number in the inorder traversal, the next node is either a parent, or the leftmost child of the right child if there is one
    if it comes first in preorder, then it's a parent of this node, so if it doesn't come first

    prev = None

    for inode in inorder:
        node = Node(data=inode)
        node is either a parent or right node of prev
        if cur comes before prev:
            # cur is a parent of prev
            # don't know which parent though...
            prev.left = cur
        else:
            # cur must be a right child of prev
            # don't know where to connect it yet
        prev = cur



        prev = Node

            2
         4     5
             6
    pre =
    in  =

    con = 2

      2
    4   5
       6

    Finish: 17:22
    1 hour 22 mins  suuuuppperr slow!  Definitely should repeat this one!
    No bugs really.  They wanted me to handle the empty list case which is a bit silly because the typing doesn't say
    that.

    I got a bit lost in this question.  Spend at least 30 mins thinking about it from the perspective of iterating over
    the inorder list first then the preorder list.  Then looked at the hint and then it all made a lot more sense!

    Also, time complexity is O(n) we consume each item in the list once
    Space complexity is O(h) which is the height of the tree, due to the call stack.
    """
    pre_start = 0
    in_start = 0

    def build(end_val: Optional[int]) -> BinaryTreeNode:
        nonlocal pre_start
        nonlocal in_start
        # consume from preorder
        consumed = preorder[pre_start] if pre_start < len(preorder) else None
        pre_start += 1
        node = BinaryTreeNode(data=consumed)
        if consumed != inorder[in_start]:
            node.left = build(consumed)

        assert inorder[in_start] == consumed
        in_start += 1

        if (inorder[in_start] if in_start < len(inorder) else None) == end_val:
            return node
        node.right = build(end_val)
        return node

    if not inorder:
        return None
    return build(None)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_from_preorder_inorder.py",
            "tree_from_preorder_inorder.tsv",
            binary_tree_from_preorder_inorder,
        )
    )

from typing import Optional

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def is_symmetric(tree: BinaryTreeNode) -> bool:
    """
      Start: 9:38

      Check if a binary tree is symmetric.

      Examples

         1
       2   2  Yes

         1    Yes

         1
      2       No

            3
        4      4
      2   3  3   2    Yes
    1              1

            3
        4      4
      2          2    Yes

            3
        4      4
      2   3  3        No

            3
        4      4
      2   3  3   8    No

      It has to have the same nodes and the same values.  But l == r and r == l?

      Pseudo Code
      def is_mirrored(l, r) -> bool:
          if l.data != r.data:
              return False
          if l.l ^ r.r:
              return False
          if l.l and r.r and not is_mirrored(l.l, r.r):
              return False
          if l.r ^ r.l:
              return False
          if l.r and r.l and not is_mirrored(l.r, r.l):
              return False
          return True

          # Pick this as it's much easier to read.  Even though it's less performant.
          if l is None and r is None:
              return True
          elif l is None ^ r is None:
              return False
          return l.data == r.data and is_mirrored(l.l, r.r) and is_mirrored(l.r, r.l)
      is_mirrored(root, root)

      have a basic answer..
      Still want to think about
      skipping the last level of function calls into null values
      is it a lot of extra work to call is_mirrored(root, root)?

    Time complexity is O(n) we look at each node once
    space complexity is O(height) for the call stack
    Can improve a bit, we're calling is_mirrored twice for the root.
    Only need to do it once with a bit of extra code.
    finish: 10:08
    20 mins.  Included a decent amount of discussion.
    """

    def is_mirrored(
        left: Optional[BinaryTreeNode], right: Optional[BinaryTreeNode]
    ) -> bool:
        if left is None and right is None:
            return True
        elif (left is None) ^ (right is None):
            return False
        return (
            left.data == right.data
            and is_mirrored(left.left, right.right)
            and is_mirrored(left.right, right.left)
        )

    # updated approach - very slightly faster on the test, <= 1us avg time.
    # This should do about half the work though.
    if tree is None:
        return True
    return is_mirrored(tree.left, tree.right)

    # first approach
    # return is_mirrored(tree, tree)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_tree_symmetric.py", "is_tree_symmetric.tsv", is_symmetric
        )
    )

from collections import deque
from typing import List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test


def binary_tree_depth_order(tree: BinaryTreeNode) -> List[List[int]]:
    """
    Return a 'level' order traversal of a binary tree

    Example
          1
        2   3
      4  5   6
    Return [[1], [2,3], [4,5,6]]

    BFS 1, 2,3, 4,5,6

    push node, depth onto queue, when depth changes, start a new list.

    Test
        q = []
        res = [[1], [2, 3], [4, 5, 6]]
        ll = 2

    Pseudo code:
    init queue with root, level 0
    result = []
    last_level = -1
    while queue:
        item, level = queue.dequeue()
        push children onto queue (with level + 1)
        if level has changed:
            add new list to result
            last_level = level
        append item data to last list in result
    return result

    O(n) space for the queue for BFS
    O(n) time -> visit each item once

    Time: 15:52... didn't write start haha.
    One but -> didn't think about the None tree case...

    Their solution is pretty nice too.  It's the, keep two different lists, the current level and next level
    """
    if not tree:
        return []

    q = deque([(tree, 0)])
    result = []
    last_level = -1
    while q:
        item, level = q.popleft()
        if item.left:
            q.append((item.left, level + 1))
        if item.right:
            q.append((item.right, level + 1))
        if level != last_level:
            result.append([])
            last_level = level
        result[-1].append(item.data)
    return result

    # Alternative solution from the book...
    # result = []
    # nodes = [tree]
    # while nodes:
    #     result.append([n.data for n in nodes])
    #     nodes = [n for node in nodes for n in (node.left, node.right) if n]
    # return result


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_level_order.py", "tree_level_order.tsv", binary_tree_depth_order
        )
    )

import functools

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


class BinaryTreeNode:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.next = None  # Populates this field.


def construct_right_sibling(tree: BinaryTreeNode) -> None:
    """
    Start: 10:12
    Fill in the 'next' field which should point to the next field on this level.
    We can do a BFS of the tree.
    The tree is perfect so that will require O(n) space and O(n) time.
    Can we do better?
    We could perhaps do this in O(log n) space (ie O(h) space) if we do a DFS and keep track of the previous node
    on each level instead...

    prev_node_on_level = []
    def dfs(node, level = 0):
        if level not in prev_node_on_level:
            add it
        else:
            prev_node_on_level[level].next = node
            update prev_node_on_level[level]
        dfs(node.left)
        dfs(node.right)
    return dfs(tree)

    O(n) time, O(log n) space
    Finished: 10:23
    Took 11 mins.

    I like this question.  There's actually an O(1) space solution which takes advantage of the fact that the tree is
    perfect, something I wasn't.
    The idea is that we go from top to bottom and process each level at a time.
    Since the level above has already been processed, the current' level is easy to process.
    If we know a node and it's parent, we just iterate, node.left, node.right, then node = node.next which is the
    next node we set on the previous level, then we add node.left and node.right again.

    What's the pseudo code for this look like?

    while node has a left:
        build_level(node)
        node = node.left

    def build_level(node):
        while True:
            node.left.next = node.right
            if not node.next:
                break
            node.right.next = node.next.left
            node = node.next


    """

    # Updated solution with O(1) space complexity
    def construct_next_level(node: BinaryTreeNode) -> None:
        while True:
            node.left.next = node.right
            if not node.next:
                break
            node.right.next = node.next.left
            node = node.next

    while tree and tree.left:
        construct_next_level(tree)
        tree = tree.left

    # My first solution with O(h) space complexity)
    # prev_node_on_level = []
    #
    # def dfs(node: BinaryTreeNode, level=0):
    #     if len(prev_node_on_level) <= level:
    #         prev_node_on_level.append(node)
    #     else:
    #         prev_node_on_level[level].next = node
    #         prev_node_on_level[level] = node
    #     if node.left:
    #         dfs(node.left, level + 1)
    #     if node.right:
    #         dfs(node.right, level + 1)
    #
    # if tree:
    #     dfs(tree)


def traverse_next(node):
    while node:
        yield node
        node = node.next
    return


def traverse_left(node):
    while node:
        yield node
        node = node.left
    return


def clone_tree(original):
    if not original:
        return None
    cloned = BinaryTreeNode(original.data)
    cloned.left, cloned.right = clone_tree(original.left), clone_tree(original.right)
    return cloned


@enable_executor_hook
def construct_right_sibling_wrapper(executor, tree):
    cloned = clone_tree(tree)

    executor.run(functools.partial(construct_right_sibling, cloned))

    return [[n.data for n in traverse_next(level)] for level in traverse_left(cloned)]


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "tree_right_sibling.py",
            "tree_right_sibling.tsv",
            construct_right_sibling_wrapper,
        )
    )

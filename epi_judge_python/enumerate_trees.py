import functools
from typing import List, Optional

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook


def generate_all_binary_trees(num_nodes: int) -> List[Optional[BinaryTreeNode]]:
    """
    Return all binary trees with the specified number of nodes.
    Eg. num_nodes = 3
          x
         x
        x

        x
       x
        x

        x
       x x

       x
        x
       x

        x
         x
          x

    The question of 'what is the time/space complexity' is as complicated as the question itself...

    @memoize
    def gen_trees(n) -> List[Optional[BinaryTreeNode]]:
        if n == 0 return None
        result = []
        root = BinaryTreeNode()
        remaining_nodes = n - 1
        for each split of remaining nodes between left and right:
            left_nodes = gen_trees(left nodes)
            right_nodes = gen_trees(right nodes)
            for all combinations of left and right:
                root.left = left
                root.right = right
                add copy to result
        return result

    Note the similarity between this problem ant 15.6 - generate parentheses.
    Both have the same time complexity which satisfy the recurrence C(n) = sum(i=1, n)(C(n-i)*C(i-1))
    The quantity C(n) is called the nth Catalan number and es equal to (2n!)/(n!*(n+1)!).
    """

    def clone_tree(node) -> Optional[BinaryTreeNode]:
        return (
            BinaryTreeNode(node.data, clone_tree(node.left), clone_tree(node.right))
            if node
            else None
        )

    @functools.lru_cache(maxsize=None)
    def gen_trees(n) -> List[Optional[BinaryTreeNode]]:
        if n == 0:
            return [None]
        result = []
        root = BinaryTreeNode()
        for left_count in range(n):
            left_nodes = gen_trees(left_count)
            right_nodes = gen_trees(n - left_count - 1)
            for left in left_nodes:
                for right in right_nodes:
                    root.left = left
                    root.right = right
                    result.append(clone_tree(root))
        return result

    return gen_trees(num_nodes)


def serialize_structure(tree):
    result = []
    q = [tree]
    while q:
        a = q.pop(0)
        result.append(0 if not a else 1)
        if a:
            q.append(a.left)
            q.append(a.right)
    return result


@enable_executor_hook
def generate_all_binary_trees_wrapper(executor, num_nodes):
    result = executor.run(functools.partial(generate_all_binary_trees, num_nodes))

    return sorted(map(serialize_structure, result))


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "enumerate_trees.py",
            "enumerate_trees.tsv",
            generate_all_binary_trees_wrapper,
        )
    )

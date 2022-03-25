import functools
from typing import Optional, List

from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
from test_framework.binary_tree_utils import must_find_node, strip_parent_link
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def lca(
    tree: BinaryTreeNode, node0: BinaryTreeNode, node1: BinaryTreeNode
) -> Optional[BinaryTreeNode]:
    """
    Trying again, wanted to do it the way the book suggested in their answer.

    Want to find a lowest common ancestor

    Example
          a
       b     c
     d  e
       f
    LCA of f and d is b
    LCA of e and c is a
    LCA of e and e is e

    Seems like a good question to solve recursively.
    What information do we need to know at each node to know the LCA?
    Well, if both nodes are in the subtree, then this is the LCA, assuming we work up from the bottom
    Imagine returning the number of nodes in this subtree
    for the tree above, if the nodes are f and d
    nodes_found(c) = 0
    nodes_found(f) = 1
    nodes_found(e) = 1
    nodes_found(d) = 1 (the node d, not f)
    nodes_found(b) = 2 - therefore b must be the LCA!

    Ok a recursive signature

    def nodes_below(node) -> int
        if (node is None) or lca:
            # if lca is set just exit
            # node is None is base case
            return 0
        nodes = int(node0 is node) + int(node1 is node)
        nodes += nodes_below(node.left) + nodes_below(node.right)
        if nodes == 2 and not lca:
            lca = node
        return nodes
    nodes_below(tree)
    return lca

    Looks better than the other approach...
    In the book, instead of lca being in a closure, it's returned as bart of the recursive function.
    That's reasonable too...
    """
    lca = None

    def nodes_below(node: Optional[BinaryTreeNode]) -> int:
        nonlocal lca
        if node is None or lca:
            # if lca is set just exit
            # node is None is base case
            return 0
        nodes = int(node0 is node) + int(node1 is node)
        nodes += nodes_below(node.left) + nodes_below(node.right)
        if nodes == 2 and not lca:
            lca = node
        return nodes

    nodes_below(tree)
    return lca


def lca_first_attempt(
    tree: BinaryTreeNode, node0: BinaryTreeNode, node1: BinaryTreeNode
) -> Optional[BinaryTreeNode]:
    """
    Start: 10:27
    Find the lowest common ancestor

    Example
          a
       b     c
     d  e
       f
    LCA of f and d is b
    LCA of e and c is a

    Idea:
    search 'up' from the two nodes until you find a common ancestor.
    Can't do that because the tree doesn't have parent fields

    from root, are both nodes a part of this?

    or... find path to both nodes?
    then find LCA from that?
    that's O(h) extra storage and we can do it in one pass (keep the path).
    O(n) time, O(h) space

    With paths:
    abef
    abd
    ans: b

    ac
    abe
    ans: a

    Pseudo code:

    dfs over tree
        build path as going
        if we see one of the nodes, save the path
    when finished, compare the paths.  The last common node from l to r is the result

    O(n) time, O(h) space

    found_nodes = [None, None]
    path
    dfs(node: not Optional):
        path.append(node)
        if node is one onf the ones we're looking for:
            copy the path into a variable for that node
        if both nodes found:
            path.pop()
            return

        if node.left:
            dfs(node.left)
        if node.right:
            dfs(node.right)
        path.pop()
    if not root:
        return None
    dfs(root)
    if haven't found both nodes:
        return None
    LCA = None
    for each item in zip(found_nodes[0], found_nodes[1]):
        if 0 != 1:
            break
        LCA = 0
    return LCA

    Test
          a
       b     c
     d  e
       f
    LCA of f and d is b

    cur_path = a
    node_paths = [[a,b,e,f], [a,b,d]]
    lca = b

    All tests pass
    11:00
    33 mins

    A couple of small bugs
    - didn't see the case where node0 and node1 were the same node
    - zip requires you pass it iterables as multiple arguments so needed to do zip(*node_paths) not zip(node_paths)
    """
    node_paths: List[Optional[List[BinaryTreeNode]]] = [None, None]
    cur_path = []

    def find_path_to_nodes(cur_node: BinaryTreeNode) -> None:
        cur_path.append(cur_node)
        if cur_node == node0:
            node_paths[0] = [*cur_path]
        if cur_node == node1:
            node_paths[1] = [*cur_path]
        if all(node_paths):
            # Don't need to pop, dont care about cur_path any more
            return
        if cur_node.left:
            find_path_to_nodes(cur_node.left)
        if cur_node.right:
            find_path_to_nodes(cur_node.right)
        cur_path.pop()

    if tree is None:
        return None
    find_path_to_nodes(tree)
    if not all(node_paths):
        # Didn't find node0 and node1 in tree
        return None
    # last matching node in the two paths is the LCA
    lca = None
    for n0, n1 in zip(*node_paths):
        if n0 != n1:
            break
        lca = n0
    return lca


@enable_executor_hook
def lca_wrapper(executor, tree, key1, key2):
    strip_parent_link(tree)
    result = executor.run(
        functools.partial(
            lca, tree, must_find_node(tree, key1), must_find_node(tree, key2)
        )
    )

    if result is None:
        raise TestFailure("Result can't be None")
    return result.data


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "lowest_common_ancestor.py", "lowest_common_ancestor.tsv", lca_wrapper
        )
    )

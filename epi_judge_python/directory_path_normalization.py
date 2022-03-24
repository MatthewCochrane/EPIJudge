from test_framework import generic_test


def shortest_equivalent_path(path: str) -> str:
    """
    Start: 13:32
    as we go through, if we see a . then it means do nothing just don't add it
    if we see a .. then it means undo the last directory
    if the .. is at the start we can't remove the previous because it's not there

    is // a special case meaning the same thing as /./?

    Examples
        ../1  = ../1
        1/2/3/..  = 1/2
        1/././././././   = 1
        1/2/././../3  = 1/2
        ../..         = ../..
        ../../1/..    = ../..
        1/../../2/.   = ../2

    ..,2

    Pseudo code
        for part in s.split('/')
            if part is '.' or empty:
                continue
            if part is '..' and stack has at least one item and item is not '..'
                pop from stack
            else
                stack.push(part)
        if not stack:
            return '.'
        return '/'.join(stack)

    O(n) time
    O(n) space -> kinda need this in python to return a string

    Some trickery here...  Not too bad.  I missed the 'root path' concept though.  A bit silly.

    Time: 13:52 -> 20 mins
    """
    result_parts = []
    root = path and path[0] == "/"
    for part in path.split("/"):
        if part == "." or part == "":
            continue
        elif part == ".." and result_parts and result_parts[-1] != "..":
            result_parts.pop()
        else:
            result_parts.append(part)
    return f"{'/' if root else ''}{'/'.join(result_parts)}"


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "directory_path_normalization.py",
            "directory_path_normalization.tsv",
            shortest_equivalent_path,
        )
    )

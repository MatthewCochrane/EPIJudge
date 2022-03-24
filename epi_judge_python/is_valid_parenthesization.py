from test_framework import generic_test


def is_well_formed(s: str) -> bool:
    """
    Start: 13:08
    Test if a string of brackets is well formed
    (), [], {}
    for one type of bracket:
    ( is always valid
    ) is only valid if the number of open brackets is at least 1
    The string must end with 0 open brackets

    Example
     ( -> invalid.  The string ends with open brackets
     () -> valid
     ()) -> invalid, last close would take count to -1
     ()() -> valid

    For multiple brackets
     (] - invalid -> count of [] brackets goes below zero
     [(]) - invalid -> can't close the [] because ( is still open

    One simple way to handle this is to use a stack, push the brackets onto the stack

    Test:
        [((){}))]
               |
        stack = [1,()

    Pseudo code
    for char in s:
        if it's an opening bracket, push it onto the stack
        if it's a closing bracket:
            if stack is not empty and it matches the last item on the stack:
                pop last item
            else:
                result is invalid
    return valid if the stack is empty

    O(n) time
    O(n) space
    could get O(max number of differences between bracket types at depth) -> would that be useful for our application?

    All tests passed first go.
    Time: 12:28
    20 mins.  That's good.
    """
    MATCHING_BRACKETS = {"(": ")", "[": "]", "{": "}"}
    open_brackets = []
    for c in s:
        if c in MATCHING_BRACKETS:
            open_brackets.append(c)
        else:
            if len(open_brackets) == 0 or c != MATCHING_BRACKETS[open_brackets.pop()]:
                return False
    return len(open_brackets) == 0


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "is_valid_parenthesization.py",
            "is_valid_parenthesization.tsv",
            is_well_formed,
        )
    )

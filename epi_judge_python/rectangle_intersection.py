import collections

from test_framework import generic_test
from test_framework.test_failure import PropertyName

Rect = collections.namedtuple('Rect', ('x', 'y', 'width', 'height'))


def intersect_rectangle(r1: Rect, r2: Rect) -> Rect:
    """
    Start: 15:33
    Return the rectangle returned by the intersection.
    It doesn't say what to do if the intersection is empty though.  I assume return a 'zero' rectangle Rect(0,0,0,0).

    Ok, so determining intersection isn't too hard.  There must be some overlap in both dimensions.
    If we simplify this problem to a line instead of a rectangle:
    Line(x, width)
    Example 1
    l1 = [0, 3]
    l2 = [2, 4]
    012345
    |  | l1
      | | l2
      || overlap = Line(x=2, width=1)
    l1.right > l2.left so there is overlap

    Example 2
    l1 = [0,3]
    l2 = [3,5]
    012345
    |  | l1
       | | l2
    l1.right <= l2.left so no overlap

    Example 3
    l1 = [3,5]
    l2 = [0,3]
    012345
       | | l1
    |  | l2
    min(l1.left, l2.left)
    l1.right <= l2.left so no overlap

    Example 4
    l1 = [2,5]
    l2 = [0,3]
    012345
      |  | l1
    |  | l2
    overlap!

    How do we know if there's an overlap?  And how do we know what the overlap is?
    Define two ranges, and check if l1.left < l2.right or l2.left < l1.right
    There are 3 cases
    1a. partial overlap
    | |
     | |
    1b. partial overlap
     | |
    | |
    2. no overlap
    | |
       | |
    3. complete overlap
    |   |
     | |

    if l1.left is in the range l2
    or l2.left is in the range l1
    There is overlap
    overlap = max(l1.left, l2.left), min(l1.right, l2.right)

    can the lengths be negative?  Assume no for now.


    Then we just have to do this in two dimensions.

    calculate r1 and r2 top and right

    is_x_overlap = r1.x is between r2.x and r2.right or
                   r2.x is between r1.x and r1.right
    is_y_overlap = r1.y is between r2.y and r2.bottom or
                   r2.y is between r1.x and r1.bottom

    if there's x and y overlap:
        x = max(r1.x, r2.x)
        y = max(r1.y, r2.y)
        return Rect(
            x
            y
            min(r1.right, r2.right) - x,
            min(r1.top, r2.top) - y
        )
    return no overlap

    Test:
    Assuming top left corner.......  Which may be wrong...
    Rect(0, 0, 4, 3)
    Rect(1, -1, 1, 5)

    r1.top = 0+3 = 3
    r1.right = 0 + 4 = 4
    r2.top = -1+5 = 4
    r2.right = 1 + 1 = 2

    is_x_overlap = (0 between 1 and 2) or (1 between 0 and 4) = True
    is_y_overlap = (0 between -1 and 4) or ... = True

    both overlap: true
    return Rect(
        max(0, 1) = 1,
        max(0, -1) = 0,
        min(4, 2) - 1 = 1,
        min(3, 4) - 0 = 3
    )

    Time complexity = O(1)
    Space complexity = O(1)

    Finish time: 16:29

    That took way too long.
    Some annoying points in that question...
    They didn't specify where the x,y point was on the rectangle
    They didn't specify if touching rectangles are considered intersecting.

    I did ok but way too slow.  I should repeat!
    Also tricky without being able to draw it.  A whiteboard would be helpful here.
    """

    r1_top = r1.y + r1.height
    r2_top = r2.y + r2.height
    r1_right = r1.x + r1.width
    r2_right = r2.x + r2.width

    is_x_overlap = (r2.x <= r1.x <= r2_right) or (r1.x <= r2.x <= r1_right)
    is_y_overlap = (r2.y <= r1.y <= r2_top) or (r1.y <= r2.y <= r1_top)

    if is_x_overlap and is_y_overlap:
        x = max(r1.x, r2.x)
        y = max(r1.y, r2.y)
        return Rect(
            x,
            y,
            min(r1_right, r2_right) - x,
            min(r1_top, r2_top) - y
        )
    return Rect(0, 0, -1, -1)


def intersect_rectangle_wrapper(r1, r2):
    return intersect_rectangle(Rect(*r1), Rect(*r2))


def res_printer(prop, value):
    def fmt(x):
        return [x[0], x[1], x[2], x[3]] if x else None

    if prop in (PropertyName.EXPECTED, PropertyName.RESULT):
        return fmt(value)
    else:
        return value


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('rectangle_intersection.py',
                                       'rectangle_intersection.tsv',
                                       intersect_rectangle_wrapper,
                                       res_printer=res_printer))

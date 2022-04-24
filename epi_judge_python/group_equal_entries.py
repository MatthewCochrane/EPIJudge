import collections
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

Person = collections.namedtuple("Person", ("age", "name"))


def group_by_age(people: List[Person]) -> None:
    """
    start: 16:11
    Want to modify people in place.  Want to update it so that
    it becomes sorted by person age.  There are a small number of
    distinct ages compared to the number of people.

    We can count the number of people with different ages. Eg. use a
    dict.
    Then do another pass? - we don't actually have to sort the dict keys.
    The question just asks to group people with the same age together.
    work your way from the back of the array to the front?
    2133343
    2:1, 1:1, 3:4, 4:1
    2:0, 1:1, 3:2, 4:6
    2133343

    3133342
    3133342
    1333342
    1233334

    1233334

    423142334231
    ~~1:2 -> 0, 2, 2~~
    ~~2:3 -> 2, 5, 5~~
    ~~3:4 -> 5, 9, 9~~
    ~~4:3 -> 9,12,12~~

    012345678901
    423142334231
    112223333444
    423142334231
    223142334431
    322142334431
    222143334431
    012345678901
    112223333444

    Could do it in O(n*unique) which is essentially O(n) if we scan through the array
    for each section and find what lives there.  we don't worry about putting other items
    anywhere else.  We'll never put them into an already filled place because we'll go from
    left to right in the array in terms of where we're placing them.

    So how do we go from the original, with the knowledge of how many there
    are of each age, to the re-ordered list?
    We can't just iterate from one end and move the item to where it needs to go because
    that would replace a value with something.  Even if we swapped the items, we would
    then need to revisit the item...
    Perhaps that works.  Can we keep swapping the next item with the item where it should be
    placed, updating the dict as we go?  We only move on to the next item when the current
    item is in it's correct place.

    dict = {
        1: {low: 0, high: 1, next: 0}
    }
    for i in range(len(items)):
        while not in correct place - item < dict[items[i].age]["low"] or item > dict[items[i].age]["high"]:
            items[i], items[dict[items[i].age]["next"]] = items[dict[items[i].age]["next"]], items[i]
            dict[xxx]["next"] += 1

    Ok, so basically, instead of iterating over the array and moving items, let's iterate over the positions
    where they should go in the groups.
    If we move items from the head of one sub-array to the head of the subarray it belongs in then we should
    sort the list.
    It's not a cyclic sort.  What was the cyclic sort and how is this different?
    I should probably try both approaches?  I think you need an extra bit of data for cyclic sort so you know not to
    move items that you've moved previously?  Wouldn't they be in their correct position already so no need for the
    extra bit?

    What's that thing where you move items around an array kinda cyclicly.  What's that whole area of algorighms called??

    Ok, let's try this for now.

    build the dict
    build the offsets
    while there are still items in the dict
        get the next item in the dict
        get the next item in the offset in the array
        work out where to move it to
        swap the items
        update the to_location's count (-= 1) and offset
        if the count was zero, delete it from the dict

    Did very poorly at this.  Need to repeat.  Took me almost 2 hours and I had to look at the answer.
    I need to work out how to do those cyclic or in-place array rearranges.  More questions like that!
    """
    # 423142334231
    # counts = {1:2,2:3,3:4,4:3}
    # offsets = 0, 2, 5, 9
    counts = collections.Counter((p.age for p in people))
    offsets = {}
    offset = 0
    for age, count in counts.items():
        offsets[age] = offset
        offset += count

    while counts:
        # not what's there but what's supposed to be there
        from_age = next(iter(counts))
        from_idx = offsets[from_age]
        to_age = people[from_idx].age
        to_idx = offsets[to_age]
        people[from_idx], people[to_idx] = people[to_idx], people[from_idx]
        counts[to_age] -= 1
        if counts[to_age] > 0:
            offsets[to_age] += 1
        else:
            del counts[to_age]


@enable_executor_hook
def group_by_age_wrapper(executor, people):
    if not people:
        return
    people = [Person(*x) for x in people]
    values = collections.Counter()
    values.update(people)

    executor.run(functools.partial(group_by_age, people))

    if not people:
        raise TestFailure("Empty result")

    new_values = collections.Counter()
    new_values.update(people)
    if new_values != values:
        raise TestFailure("Entry set changed")

    ages = set()
    last_age = people[0].age

    for x in people:
        if x.age in ages:
            raise TestFailure("Entries are not grouped by age")
        if last_age != x.age:
            ages.add(last_age)
            last_age = x.age


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "group_equal_entries.py", "group_equal_entries.tsv", group_by_age_wrapper
        )
    )

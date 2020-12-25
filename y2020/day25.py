import pytest
import sys
from hamcrest import assert_that, is_

from lib.profiling import reporting


def compute(data, public_key_root=7):
    public_keys = set(map(int, data.strip().splitlines()))

    secret_loops = {}
    for loops, number in reporting(enumerate(transform(public_key_root)),
                                   every=1000):
        if number in public_keys:
            print(f'Found {number}')
            secret_loops[number] = loops
            if len(secret_loops) == len(public_keys):
                break

    keys = iter(public_keys)
    return transform_loops(next(keys), secret_loops[next(keys)])


DIVIDER = 20201227


def transform(subject):
    value = 1
    while True:
        yield value
        value *= subject
        value %= DIVIDER


def transform_loops(subject, loops):
    for i, val in enumerate(transform(subject)):
        if i == loops:
            return val


@pytest.mark.parametrize('subject,loop,expect', [
    (7, 8, 5764801),
    (7, 11, 17807724),
    (17807724, 8, 14897079),
    (5764801, 11, 14897079),
])
def test_transform(subject,loop, expect):
    assert_that(transform_loops(subject, loop), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("""\
5764801
17807724
""", 14897079)
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


puzzle_input = """\
1614360
7734663
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

import sys

import pytest
from hamcrest import assert_that, is_


def compute(data):
    return None


def compute2(data):
    return None


@pytest.mark.parametrize('val,expect', [
    ("""\
""",)
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("""\
""",)
])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = """\
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

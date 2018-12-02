import unittest

import sys
from hamcrest import assert_that, is_


def compute(data):
    return 0


def compute2(data):
    return 0


class DayTest(unittest.TestCase):
    def test_(self):
        assert_that(True, is_(False))


puzzle_input = ""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

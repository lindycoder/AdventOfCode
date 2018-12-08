import sys
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_


def compute(data):
    return 0


def compute2(data):
    return 0


class ProvidedTest(unittest.TestCase):
    input = dedent("""\
        """)

    def test_part_1(self):
        assert_that(compute(self.input), is_(False))

    def test_part_2(self):
        assert_that(compute2(self.input), is_(False))


puzzle_input = """\
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

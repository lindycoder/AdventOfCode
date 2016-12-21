import hashlib
import re
import sys
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_, contains_string, starts_with


def compute(data):
    discs = read_data(data)

    time = 0
    while 1:
        if all((time + 1 + i + discs[i][1]) % discs[i][0] == 0 for i in range(0, len(discs))):
            return time
        time += 1


def read_data(input):
    result = []
    for line in input.strip().split("\n"):
        match = re.match("Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+).", line)
        result.append((int(match.group(1)), int(match.group(2))))

    return result

class ReadTest(unittest.TestCase):
    def test_reading(self):
        result = read_data(dedent("""
            Disc #1 has 7 positions; at time=0, it is at position 0.
            Disc #2 has 13 positions; at time=0, it is at position 0.
            Disc #3 has 3 positions; at time=0, it is at position 2.
            Disc #4 has 5 positions; at time=0, it is at position 2.
            Disc #5 has 17 positions; at time=0, it is at position 0.
            Disc #6 has 19 positions; at time=0, it is at position 7."""))

        assert_that(result, is_([
            (7, 0),
            (13, 0),
            (3, 2),
            (5, 2),
            (17, 0),
            (19, 7)
        ]))


class ComputeTest(unittest.TestCase):
    def test_official(self):
        result = compute(dedent("""
            Disc #1 has 5 positions; at time=0, it is at position 4.
            Disc #2 has 2 positions; at time=0, it is at position 1."""))
        assert_that(result, is_(5))


if __name__ == '__main__':
    puzzle_input = dedent("""
        Disc #1 has 7 positions; at time=0, it is at position 0.
        Disc #2 has 13 positions; at time=0, it is at position 0.
        Disc #3 has 3 positions; at time=0, it is at position 2.
        Disc #4 has 5 positions; at time=0, it is at position 2.
        Disc #5 has 17 positions; at time=0, it is at position 0.
        Disc #6 has 19 positions; at time=0, it is at position 7.""")

    if sys.argv[1] == "1":
        result = compute(puzzle_input)
    else:
        result = compute(puzzle_input + "\nDisc #7 has 11 positions; at time=0, it is at position 0.")

    print("Result is {}".format(result))

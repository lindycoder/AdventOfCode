import hashlib
import re
import sys
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_, contains_string, starts_with


def compute(initial, length):
    data = initial
    while len(data) < length:
        data = generate(data)
    data = data[:length]

    result = checksum(data)
    while len(result) % 2 == 0:
        result = checksum(result)

    return result


def generate(input):
    return input + "0" + "".join(reversed(["1" if b == "0" else "0" for b in input]))


def checksum(input):
    return "".join("1" if input[i] == input[i + 1] else "0" for i in range(0, len(input), 2))



class GenerateDataTest(unittest.TestCase):
    def test_generate(self):
        assert_that(generate("1"), is_("100"))
        assert_that(generate("0"), is_("001"))
        assert_that(generate("11111"), is_("11111000000"))
        assert_that(generate("111100001010"), is_("1111000010100101011110000"))


class ChecksumTest(unittest.TestCase):
    def test_checksum(self):
        assert_that(checksum("110010110100"), is_("110101"))
        assert_that(checksum("110101"), is_("100"))


class ZComputeTest(unittest.TestCase):
    def test_official(self):
        assert_that(compute("10000", length=20), is_("01100"))


if __name__ == '__main__':
    puzzle_input = "10011111011011001"

    if sys.argv[1] == "1":
        result = compute(puzzle_input, length=272)
    else:
        result = compute(puzzle_input, length=35651584)

    print("Result is {}".format(result))

import unittest

import sys

from functools import reduce
from hamcrest import assert_that, is_


def compute(data, list_size=256):
    the_list = list(range(0, list_size))

    scrolled = 0
    skip_size = 0

    lengths = parse(data)
    the_list, scrolled, skip_size = _hash(the_list, lengths, scrolled, skip_size)

    the_list = scroll(list_size - (scrolled % list_size), the_list)

    return the_list[0] * the_list[1]


def compute2(data, list_size=256):
    return knot_hash(data, list_size)


def knot_hash(data, list_size=256):
    suffix = [17, 31, 73, 47, 23]

    the_list = list(range(0, list_size))

    scrolled = skip_size = 0

    lengths = parse2(data) + suffix
    for _ in range(0, 64):
        the_list, scrolled, skip_size = _hash(the_list, lengths, scrolled, skip_size)

    the_list = scroll(list_size - (scrolled % list_size), the_list)

    return to_hex(densify(the_list[start:start + 16]) for start in range(0, list_size, 16))


def _hash(the_list, lengths, scrolled, skip_size):
    for pinch_size in lengths:
        the_list = list(reversed(the_list[:pinch_size])) + the_list[pinch_size:]

        move = pinch_size + skip_size

        scrolled += move
        the_list = scroll(move % len(the_list), the_list)

        skip_size += 1
    return the_list, scrolled, skip_size


def scroll(offset, l):
    return l[offset:] + l[:offset]


def densify(block):
    return reduce(lambda total, element: element ^ total, block, 0)


def to_hex(l):
    return "".join("{:02x}".format(e) for e in l)


def parse(data):
    return list(int(e) for e in data.split(","))


def parse2(data):
    return list(ord(e) for e in data)


class DayTest(unittest.TestCase):
    def test_example1(self):
        input = "3"
        assert_that(compute(input, list_size=5), is_(2))

    def test_example2(self):
        input = "3,4"
        assert_that(compute(input, list_size=5), is_(12))

    def test_example3(self):
        input = "3,4,1"
        assert_that(compute(input, list_size=5), is_(12))

    def test_example4(self):
        input = "3,4,1,5"
        assert_that(compute(input, list_size=5), is_(12))


class Day2Test(unittest.TestCase):
    def test_example1(self):
        input = ""
        assert_that(compute2(input), is_("a2582a3a0e66e6e86e3812dcb672a272"))

    def test_example2(self):
        input = "AoC 2017"
        assert_that(compute2(input), is_("33efeb34ea91902bb2f59c9920caa6cd"))

    def test_example3(self):
        input = "1,2,3"
        assert_that(compute2(input), is_("3efbe78a8d82f29979031a4aa0b16a9d"))

    def test_example4(self):
        input = "1,2,4"
        assert_that(compute2(input), is_("63960835bcdc130f0b66d7ff4f6a5a8e"))


class ScrollTest(unittest.TestCase):
    def test_scroll(self):
        assert_that(scroll(2, [1, 2, 3]), is_([3, 1, 2]))


class Parse2Test(unittest.TestCase):
    def test_parse(self):
        assert_that(parse2("1,2,3"), is_([49, 44, 50, 44, 51]))


class HashTest(unittest.TestCase):
    def test_hash(self):
        assert_that(densify([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]), is_(64))


class ToHexTest(unittest.TestCase):
    def test_to_hex(self):
        assert_that(to_hex([64, 7, 255]), is_("4007ff"))


puzzle_input = "120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113"

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

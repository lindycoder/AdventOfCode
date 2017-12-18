import re
import unittest

import sys
from textwrap import dedent

from hamcrest import assert_that, is_


def compute(data, iterations=40000000):
    starts = parse(data)

    gen_a = generator(factor=16807, divider=2147483647, start=starts[0])
    gen_b = generator(factor=48271, divider=2147483647, start=starts[1])

    matches = 0
    for _ in range(0, iterations):
        if low_16_equals(next(gen_a), next(gen_b)):
            matches += 1

    return matches

def compute2(data, iterations=5000000):
    starts = parse(data)

    gen_a = peeky_generator(factor=16807, divider=2147483647, start=starts[0], multiples_of=4)
    gen_b = peeky_generator(factor=48271, divider=2147483647, start=starts[1], multiples_of=8)

    matches = 0
    for _ in range(0, iterations):
        if low_16_equals(next(gen_a), next(gen_b)):
            matches += 1

    return matches


def generator(factor, divider, start):
    num = start
    while True:
        num = (num * factor) % divider
        yield num


def peeky_generator(factor, divider, start, multiples_of):
    num = start
    while True:
        num = (num * factor) % divider
        if num % multiples_of == 0:
            yield num


def low_16_equals(a, b):
    return bin(a)[-16:] == bin(b)[-16:]
    # low_16 = 2 ** 16
    # return a - (a % low_16) == b - (b % low_16)

def parse(data):
    return tuple(int(v) for v in re.findall(".*starts with (\d+)$", data, flags=re.MULTILINE))


class DayTest(unittest.TestCase):
    def test_example_simple(self):
        input = dedent("""\
            Generator A starts with 65
            Generator B starts with 8921""")
        assert_that(compute(input, iterations=5), is_(1))

    def test_example(self):
        input = dedent("""\
            Generator A starts with 65
            Generator B starts with 8921""")
        assert_that(compute(input), is_(588))


class Day2Test(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            Generator A starts with 65
            Generator B starts with 8921""")
        assert_that(compute2(input), is_(309))


class ParseTest(unittest.TestCase):
    def test_parse(self):
        assert_that(parse(puzzle_input), is_((634, 301)))


class Low16EqualsTest(unittest.TestCase):
    def test_equals(self):
        assert_that(low_16_equals(245556042, 1431495498), is_(True))

    def test_small_numbers(self):
        assert_that(low_16_equals(0, 0), is_(True))
        assert_that(low_16_equals(1, 1), is_(True))

    def test_smallest_different_numbers(self):
        assert_that(low_16_equals(2 ** 16, 2 ** 17), is_(True))

    def test_not_equals(self):
        assert_that(low_16_equals(1092455, 430625591), is_(False))


class GeneratorTest(unittest.TestCase):
    def test_generator_a(self):
        gen = generator(factor=16807, divider=2147483647, start=65)

        assert_that(next(gen), is_(1092455))
        assert_that(next(gen), is_(1181022009))
        assert_that(next(gen), is_(245556042))
        assert_that(next(gen), is_(1744312007))
        assert_that(next(gen), is_(1352636452))

    def test_generator_b(self):
        gen = generator(factor=48271, divider=2147483647, start=8921)

        assert_that(next(gen), is_(430625591))
        assert_that(next(gen), is_(1233683848))
        assert_that(next(gen), is_(1431495498))
        assert_that(next(gen), is_(137874439))
        assert_that(next(gen), is_(285222916))

    def test_peeky_generator_a(self):
        gen = peeky_generator(factor=16807, divider=2147483647, start=65, multiples_of=4)

        assert_that(next(gen), is_(1352636452))
        assert_that(next(gen), is_(1992081072))
        assert_that(next(gen), is_(530830436))
        assert_that(next(gen), is_(1980017072))
        assert_that(next(gen), is_(740335192))

    def test_peeky_generator_b(self):
        gen = peeky_generator(factor=48271, divider=2147483647, start=8921, multiples_of=8)

        assert_that(next(gen), is_(1233683848))
        assert_that(next(gen), is_(862516352))
        assert_that(next(gen), is_(1159784568))
        assert_that(next(gen), is_(1616057672))
        assert_that(next(gen), is_(412269392))


puzzle_input = """\
Generator A starts with 634
Generator B starts with 301"""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

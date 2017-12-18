import unittest

import sys
from hamcrest import assert_that, is_


def compute(data):
    step = int(data)

    buffer = [0]
    pos = 0

    for i in range(1, 2018):
        pos = (pos + step) % len(buffer) + 1
        # print("switch at {} {} {}".format(pos, i, step))
        buffer = buffer[:pos] + [i] + buffer[pos:]

    return buffer[pos + 1]


def compute2_brute(data):
    step = int(data)

    buffer = [0]
    pos = 0

    for i in range(1, 50000001):
        pos = (pos + step) % len(buffer) + 1
        buffer = buffer[:pos] + [i] + buffer[pos:]

    return buffer[buffer.index(0) + 1]


def compute2(data):
    last = 0
    for num in generator(int(data)):
        if num > 50000000:
            return last
        last = num


class DayTest(unittest.TestCase):
    def test_example(self):
        assert_that(compute("3"), is_(638))

    def test_examplex(self):
        compute(1)
        compute(2)
        compute(3)
        compute(4)
        compute(5)
        compute(6)
        compute(7)
        compute(8)
        compute(314)

    def test_puzzle(self):
        assert_that(compute(puzzle_input), is_(355))


def generator(step):
    yield 4
    size = 5
    pos = 1
    while True:
        pos = (pos + step + 1) % size
        if pos == 0:
            pos = size
        if pos == 1:
            yield size

        size += 1


class GeneratorTest(unittest.TestCase):
    def test_example(self):
        gen = generator(314)

        assert_that(next(gen), is_(4))
        assert_that(next(gen), is_(5))
        assert_that(next(gen), is_(50))
        assert_that(next(gen), is_(54))
        assert_that(next(gen), is_(61))
        assert_that(next(gen), is_(64))
        assert_that(next(gen), is_(89))
        assert_that(next(gen), is_(131))
        assert_that(next(gen), is_(1829))


puzzle_input = "314"

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

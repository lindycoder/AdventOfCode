import hashlib
import logging
import sys
import unittest
from collections import deque
from time import time

import math
from hamcrest import assert_that, is_


def compute(number):
    elves = list(range(1, number + 1))

    while len(elves) > 1:
        elves = one_full_round(elves)

    return elves[0]


def one_full_round(elves):
    odd = len(elves) % 2 == 1
    elves = elves[::2]
    if odd:
        elves.insert(0, elves.pop())
    return elves


def compute2(number):
    elves = list(range(1, number + 1))

    while len(elves) > 1:
        elves.pop(int(len(elves) / 2))
        elves.append(elves.pop(0))

    return elves[0]


class ZComputeTest(unittest.TestCase):
    def test_official(self):
        assert_that(compute(5), is_(3))
        assert_that(compute(7), is_(7))
        assert_that(compute(9), is_(3))
        assert_that(compute(11), is_(7))

    def test_official2(self):
        assert_that(compute2(5), is_(2))
        assert_that(compute2(7), is_(5))
        assert_that(compute2(9), is_(9))
        assert_that(compute2(11), is_(2))



if __name__ == '__main__':
    puzzle_input = 3004953

    if sys.argv[1] == "1":
        result = compute(puzzle_input)
    else:
        result = compute2(puzzle_input)

    print("Result is {}".format(result))

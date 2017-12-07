import unittest

import sys
from hamcrest import assert_that, is_


def compute(data):
    states, banks = states_to_loop(data)

    return len(states)

def compute2(data):
    states, banks = states_to_loop(data)

    return len(states) - states.index(banks)


def states_to_loop(data):
    banks = parse(data)

    states = []
    while banks not in states:
        states.append(snapshot(banks))

        cursor = find_bank_with_most_blocks(banks)
        blocks = banks[cursor]
        banks[cursor] = 0

        distribute(blocks, banks, start_after=cursor)

    return states, banks

def parse(data):
    return list(int(e) for e in data.split())


def snapshot(banks):
    return banks[:]


def find_bank_with_most_blocks(banks):
    return banks.index(max(banks))

def distribute(count, banks, start_after):
    cursor = start_after
    for _ in range(0, count):
        cursor = (cursor + 1) % len(banks)
        banks[cursor] += 1
    return banks

class DayTest(unittest.TestCase):
    def test_example(self):
        assert_that(compute("0 2 7 0"), is_(5))


class Day2Test(unittest.TestCase):
    def test_example(self):
        assert_that(compute2("0 2 7 0"), is_(4))


class FindBankTest(unittest.TestCase):
    def test_1(self):
        assert_that(find_bank_with_most_blocks([1]), is_(0))

    def test_2(self):
        assert_that(find_bank_with_most_blocks([1, 3]), is_(1))

    def test_equals(self):
        assert_that(find_bank_with_most_blocks([4, 3, 4]), is_(0))


class DistrubuteTest(unittest.TestCase):
    def test_1(self):
        assert_that(distribute(1, [0], start_after=0), is_([1]))

    def test_loop_around(self):
        assert_that(distribute(3, [0, 0], start_after=1), is_([2, 1]))


puzzle_input = "4	1	15	12	0	9	9	5	5	8	7	3	14	5	12	3"

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

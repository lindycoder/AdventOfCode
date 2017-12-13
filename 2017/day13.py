import unittest

import sys
from textwrap import dedent

from hamcrest import assert_that, is_


def compute(data):
    scanners = parse(data)

    return cross_firewall(scanners)


def compute2(data):
    scanners = parse(data)

    tests = 5000000
    timings = []
    for s in scanners:
        if s.depth > 0:
            timings.append((seq(s.depth) * int(tests / s.depth))[s.layer:])

    for i in range(10, tests - 1000):
        if all(t[i] != 0 for t in timings):
            return i

    return None


def cross_firewall(scanners):
    severity = 0
    catching = []
    for scanner in scanners:
        if scanner.depth > 0 and scanner.position == 0:
            catching.append(scanner)
            severity += scanner.layer * scanner.depth

        update_scanners(scanners)

    print("Scanners catching : {}".format("-".join(str(s.layer) for s in catching)))
    return severity


class Scanner:
    def __init__(self, layer):
        self.layer = layer
        self.depth = 0
        self.position = 0
        self.direction = 1

    def dump(self):
        return "{}-{}-{}-{}".format(self.layer, self.depth, self.position, self.direction)


def update_scanners(scanners):
    for s in scanners:
        if s.depth > 0:
            s.position += s.direction
            if s.position == 0 or s.position == s.depth - 1:
                s.direction *= -1


def seq(depth):
    asc = list(range(0, depth))
    return asc + list(reversed(asc[1:-1]))


def parse(data):
    lines = data.split("\n")
    last_layer = int(lines[-1].split(": ")[0])

    layers = []
    for i in range(0, last_layer + 1):
        layers.append(Scanner(i))

    for l in lines:
        layer, depth = l.split(": ")
        layers[int(layer)].depth = int(depth)

    return layers


class DayTest(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            0: 3
            1: 2
            4: 4
            6: 4""")

        assert_that(compute(input), is_(24))

    def test_puzzle(self):
        assert_that(compute(puzzle_input), is_(1632))


class Day2Test(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            0: 3
            1: 2
            4: 4
            6: 4""")

        assert_that(compute2(input), is_(10))

    def test_puzzle(self):
        assert_that(compute2(puzzle_input), is_(3834136))


class ParseTest(unittest.TestCase):
    def test_parse(self):
        input = dedent("""\
            0: 3
            1: 2
            4: 4
            6: 4""")

        l0, l1, l2, l3, l4, l5, l6 = parse(input)

        assert_that(l0.depth, is_(3))
        assert_that(l1.depth, is_(2))
        assert_that(l2.depth, is_(0))
        assert_that(l3.depth, is_(0))
        assert_that(l4.depth, is_(4))
        assert_that(l5.depth, is_(0))
        assert_that(l6.depth, is_(4))


class MakeSequenceTest(unittest.TestCase):
    def test_seq2(self):
        assert_that(seq(2), is_([0, 1]))

    def test_seq3(self):
        assert_that(seq(3), is_([0, 1, 2, 1]))

    def test_seq4(self):
        assert_that(seq(4), is_([0, 1, 2, 3, 2, 1]))

    def test_seq5(self):
        assert_that(seq(5), is_([0, 1, 2, 3, 4, 3, 2, 1]))


puzzle_input = """\
0: 4
1: 2
2: 3
4: 5
6: 6
8: 6
10: 4
12: 8
14: 8
16: 9
18: 8
20: 6
22: 6
24: 8
26: 12
28: 12
30: 12
32: 10
34: 8
36: 8
38: 10
40: 12
42: 12
44: 12
46: 14
48: 14
50: 14
52: 14
54: 12
56: 12
58: 12
60: 12
62: 14
64: 14
66: 14
68: 14
70: 14
80: 14
82: 14
86: 14
88: 17
94: 30
98: 18"""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

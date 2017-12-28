import unittest

import sys
from textwrap import dedent

from hamcrest import assert_that, is_


def compute(data):
    chains = compute_chains(0, parse(data), [])

    return max(sum(c.i + c.o for c in chain) for chain in chains)


def remaining_components_without(component, components):
    components = components[:]
    components.remove(component)
    return components


def compute_chains(from_, remaining_components, chain):
    chains = []
    for c in remaining_components:
        if c.i == from_:
            pins = c.o
        elif c.o == from_:
            pins = c.i
        else:
            continue

        subchains = compute_chains(pins, remaining_components_without(c, remaining_components), chain + [c])
        chains.extend(subchains)

    chains.append(chain)
    return chains


def compute2(data):
    chains = compute_chains(0, parse(data), [])

    longest_length = max(len(chain) for chain in chains)
    longuest_chains = list(c for c in chains if len(c) == longest_length)

    return max(sum(c.i + c.o for c in chain) for chain in longuest_chains)


def parse(data):
    return [Component(*list(int(e) for e in line.split("/"))) for line in data.split("\n")]


class Component:
    def __init__(self, i, o):
        self.i = i
        self.o = o

    def __str__(self):
        return "<{}/{}>".format(self.i, self.o)


class DayTest(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            0/2
            2/2
            2/3
            3/4
            3/5
            0/1
            10/1
            9/10""")
        assert_that(compute(input), is_(31))


class Day2Test(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            0/2
            2/2
            2/3
            3/4
            3/5
            0/1
            10/1
            9/10""")
        assert_that(compute2(input), is_(19))


class ParseTest(unittest.TestCase):
    def test_parse(self):
        input = dedent("""\
            0/2
            2/2548""")

        c1, c2 = parse(input)
        assert_that(c1.i, is_(0))
        assert_that(c1.o, is_(2))
        assert_that(c2.i, is_(2))
        assert_that(c2.o, is_(2548))


puzzle_input = """\
14/42
2/3
6/44
4/10
23/49
35/39
46/46
5/29
13/20
33/9
24/50
0/30
9/10
41/44
35/50
44/50
5/11
21/24
7/39
46/31
38/38
22/26
8/9
16/4
23/39
26/5
40/40
29/29
5/20
3/32
42/11
16/14
27/49
36/20
18/39
49/41
16/6
24/46
44/48
36/4
6/6
13/6
42/12
29/41
39/39
9/3
30/2
25/20
15/6
15/23
28/40
8/7
26/23
48/10
28/28
2/13
48/14"""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

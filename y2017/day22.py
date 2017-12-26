import unittest

import sys
from enum import Enum
from textwrap import dedent

from hamcrest import assert_that, is_


class Grid:
    def __init__(self, default_factory=None):
        self.default_factory = default_factory or (lambda: None)
        self._offset = 0
        self._grid = [[self.default_factory()]]

    def apply(self, from_x, from_y, data):
        for y, line in enumerate(data):
            for x, e in enumerate(line):
                self(from_x + x, from_y - y, e)

    def __call__(self, x, y, value=None):
        expected_x = self._offset + x
        expected_y = (self._offset - y)

        max_expectation = max(abs(x), abs(y))
        current_radius = int(len(self._grid) / 2)
        if max_expectation > current_radius:
            for i in range(current_radius, max_expectation):
                for line in self._grid:
                    line.insert(0, self.default_factory())
                    line.append(self.default_factory())
                self._grid.insert(0, list(self.default_factory() for _ in range(0, len(self._grid) + 2)))
                self._grid.append(list(self.default_factory() for _ in range(0, len(self._grid) + 1)))
                self._offset += 1

            expected_x = self._offset + x
            expected_y = (self._offset - y)

        if value is not None:
            self._grid[expected_y][expected_x] = value

        return self._grid[expected_y][expected_x]

    def to_array(self):
        return self._grid


class Dir(Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)


X = 0
Y = 1


def compute(data, bursts=10000):
    return process_virus(data, bursts,
                         turn_table={
                             "#": {
                                 Dir.UP: Dir.RIGHT,
                                 Dir.RIGHT: Dir.DOWN,
                                 Dir.DOWN: Dir.LEFT,
                                 Dir.LEFT: Dir.UP,
                             },
                             ".": {
                                 Dir.UP: Dir.LEFT,
                                 Dir.LEFT: Dir.DOWN,
                                 Dir.DOWN: Dir.RIGHT,
                                 Dir.RIGHT: Dir.UP,
                             }
                         },
                         swap_table={
                             "#": ".",
                             ".": "#"
                         })


def compute2(data, bursts=10000000):
    return process_virus(data, bursts,
                         turn_table={
                             "#": {
                                 Dir.UP: Dir.RIGHT,
                                 Dir.RIGHT: Dir.DOWN,
                                 Dir.DOWN: Dir.LEFT,
                                 Dir.LEFT: Dir.UP,
                             },
                             ".": {
                                 Dir.UP: Dir.LEFT,
                                 Dir.LEFT: Dir.DOWN,
                                 Dir.DOWN: Dir.RIGHT,
                                 Dir.RIGHT: Dir.UP,
                             },
                             "W": {
                                 Dir.UP: Dir.UP,
                                 Dir.LEFT: Dir.LEFT,
                                 Dir.DOWN: Dir.DOWN,
                                 Dir.RIGHT: Dir.RIGHT,
                             },
                             "F": {
                                 Dir.UP: Dir.DOWN,
                                 Dir.LEFT: Dir.RIGHT,
                                 Dir.DOWN: Dir.UP,
                                 Dir.RIGHT: Dir.LEFT,
                             }
                         },
                         swap_table={
                             ".": "W",
                             "W": "#",
                             "#": "F",
                             "F": ".",
                         })


def process_virus(data, bursts, turn_table, swap_table):
    grid = parse(data)

    direction = Dir.UP
    pos = [0, 0]

    infected = 0
    for i in range(0, bursts):
        state = grid(*pos)
        direction = turn_table[state][direction]
        state = swap_table[state]
        if state == "#":
            infected += 1

        grid(*pos, state)

        x, y = direction.value
        pos[X] += x
        pos[Y] += y

    return infected


def parse(data):
    raw = [list(line) for line in data.split("\n")]
    half_size = int(len(raw) / 2)
    g = Grid(default_factory=lambda: ".")
    g.apply(-half_size, half_size, raw)

    return g


class DayTest(unittest.TestCase):
    def test_example1(self):
        input = dedent("""\
            ..#
            #..
            ...""")
        assert_that(compute(input, bursts=7), is_(5))

    def test_example2(self):
        input = dedent("""\
            ..#
            #..
            ...""")
        assert_that(compute(input, bursts=70), is_(41))

    def test_example3(self):
        input = dedent("""\
            ..#
            #..
            ...""")
        assert_that(compute(input), is_(5587))

    def test_puzzle(self):
        assert_that(compute(puzzle_input), is_(5259))


class Day2Test(unittest.TestCase):
    def test_example1(self):
        input = dedent("""\
            ..#
            #..
            ...""")
        assert_that(compute2(input, bursts=100), is_(26))


class FillMapTest(unittest.TestCase):
    def test_simple(self):
        map = parse(dedent("""\
            ..#
            #..
            ..."""))

        assert_that(map.to_array(), is_([
            ['.', '.', '#'],
            ['#', '.', '.'],
            ['.', '.', '.'],
        ]))

        assert_that(map(0, 0), is_("."))
        assert_that(map(1, 1), is_("#"))
        assert_that(map(-1, 0), is_("#"))


class GridTest(unittest.TestCase):
    def test_exansion(self):
        g = Grid(lambda: '.')
        g(-1, -1)
        assert_that(g.to_array(), is_([
            ['.', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', '.'],
        ]))

    def test_exansion2(self):
        g = Grid(lambda: '.')
        g(1, 2)
        assert_that(g.to_array(), is_([
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
        ]))

    def test_exansion3(self):
        g = Grid(lambda: '.')
        g(0, 0, "X")
        g(2, 2, "X")
        assert_that(g.to_array(), is_([
            ['.', '.', '.', '.', 'X'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', 'X', '.', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.'],
        ]))


puzzle_input = """\
......#.#....####.##.#...
##.##.#.####.##.#.#.##..#
.#.#######.#..###......#.
#####..###.##..####.#..##
.#..#.##...#.####.#....#.
#.#...#.#####.#.#####..##
..##.#..######....####.##
#.##.#....#.#.##........#
.#....#....###.#....####.
....#..##.#.#.##.#....#.#
.#.##.#.####..#..#.##..##
##.####.#..###...#.#...##
....#....#..#..####.##...
..#.#.#.#..#.###...#...##
.#..#..##..##.#.#..##.#..
####.#.#...##.#..##.###..
###.#....#...#..#..#...##
.##....##.......####.#.##
#.#.##.#.#..#.#..##..####
...#..##.#.####.....##.##
.#.##.#####.#.#....#####.
##......#..#.###..####.##
..#...#########.....#..##
##..###.##...###.#.#.#.#.
..###.###.##.#.###....#.#"""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

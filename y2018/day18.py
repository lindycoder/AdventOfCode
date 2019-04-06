import sys
import unittest
from enum import Enum
from itertools import groupby
from textwrap import dedent

from hamcrest import assert_that, is_

from y2018 import Point, group


class States(Enum):
    OPEN = "."
    LUMBERYARD = "#"
    TREES = "|"

def compute(data, iterations):
    area = parse(data)

    for i in range(0, iterations):
        if i % 10000 == 0:
            print(f"At {i / iterations * 100}%")
        area = {point: next_state(area, point)
                for point, actual in area.items()}

    states = {key: len(list(groups))
            for key, groups in groupby(sorted(area.values(), key=lambda e: e.value))}

    return states[States.TREES] * states[States.LUMBERYARD]


def parse(input):
    area = {}
    for y, line in enumerate(input.split("\n")):
        for x, state in enumerate(line):
            area[Point(x, y)] = States(state)
    return area


def next_state(area, point: Point):
    actual = area[point]
    neighbor_states = [area[n] for n in point.extended_neighbors if n in area]
    surroundings = {key: len(list(groups))
                    for key, groups in groupby(sorted(neighbor_states, key=lambda e: e.value))}

    if actual is States.OPEN and surroundings.get(States.TREES, 0) >= 3:
        return States.TREES
    elif actual is States.TREES and surroundings.get(States.LUMBERYARD, 0) >= 3:
        return States.LUMBERYARD
    elif actual is States.LUMBERYARD and (surroundings.get(States.TREES, 0) < 1 or surroundings.get(States.LUMBERYARD, 0) < 1):
        return States.OPEN

    return actual

class ParseTest(unittest.TestCase):
    def test_parse(self):
        input = dedent("""\
            .#
            .|""")

        assert_that(parse(input), {
            Point(0, 0): States.OPEN,
            Point(1, 0): States.LUMBERYARD,
            Point(0, 1): States.OPEN,
            Point(1, 1): States.TREES,
        })


class NextStateTest(unittest.TestCase):
    def test_next_state_open_stays_open(self):
        area = parse(dedent("""\
            ...
            |..
            ..|"""))

        assert_that(next_state(area, Point(1, 1)), is_(States.OPEN))

    def test_next_state_open_becomes_trees_surrounded_by_trees(self):
        area = parse(dedent("""\
            .|.
            |..
            ..|"""))

        assert_that(next_state(area, Point(1, 1)), is_(States.TREES))

    def test_next_state_trees_stays_trees(self):
        area = parse(dedent("""\
            ...
            .|#
            #.."""))

        assert_that(next_state(area, Point(1, 1)), is_(States.TREES))

    def test_next_state_trees_becomes_lumberyard_surrounded_by_lumberyards(self):
        area = parse(dedent("""\
            #..
            #|.
            #.."""))

        assert_that(next_state(area, Point(1, 1)), is_(States.LUMBERYARD))

    def test_next_state_lumberyard_stays_lumberyard_if_close_to_lumberyard_and_trees(self):
        area = parse(dedent("""\
            |..
            .#.
            ..#"""))

        assert_that(next_state(area, Point(1, 1)), is_(States.LUMBERYARD))

    def test_next_state_lumberyard_becomes_open_when_not_surrounded(self):
        area = parse(dedent("""\
            #..
            ##.
            #.."""))

        assert_that(next_state(area, Point(1, 1)), is_(States.OPEN))

    def test_next_state_lumberyard_becomes_open_when_not_surrounded2(self):
        area = parse(dedent("""\
            |..
            |#.
            |.."""))

        assert_that(next_state(area, Point(1, 1)), is_(States.OPEN))

    def test_next_state_no_neighbors_dont_count(self):
        area = parse(dedent("""\
            #"""))

        assert_that(next_state(area, Point(0, 0)), is_(States.OPEN))

class ProvidedTest(unittest.TestCase):
    input = dedent("""\
        .#.#...|#.
        .....#|##|
        .|..|...#.
        ..|#.....#
        #.#|||#|#|
        ...#.||...
        .|....|...
        ||...#|.#|
        |.||||..|.
        ...#.|..|.""")

    def test_part_1(self):
        assert_that(compute(self.input, 10), is_(1147))


puzzle_input = """\
#.|..#...|#...#...|.|....|..|...#.|...#..|.|.|.|#.
.....|.#...|....#|....||#.|###.......#.#|.##.|...|
...#|.....||..|..|||.#......#..|.#..|..|..#.....|.
..|..#.....###.#|.....|.|...##.##......|#...|##...
....###.......|...|..||...#||.##..|.|.|.#|..|.#...
|..|#......|#.|..#.#....||...|.#||....|#....#.#...
.|..#.|.|..|.#|.#|.#......#..###.|||.#.|.....#...#
..|.|.....||......|...|#....|....##.|.|..|..#.#...
.......##.#..|.|.........|...|..#|.|#.#..||#|...|.
.|###|...|.....|..#.|..|#...|.............|.......
|........##.|.#.##.|##.##..#|..#|.|..|.|....|.....
|.....#|#..#|.|..#..#|...|.#..|#.........|#....|..
..|.#........#........#..||#|.#.........#.|#||.|||
.|##...#..||.....|.|..|..|...|...|..#.....#.###|..
..#|.#|#...|#.|||#..#|#...##.|||#...#.|.|...#.|...
...|...#|..###...#.....|..|...|#..........|..|.|..
#||||.|#.##|....|..||...|##|.....|.|#||..##..||.||
.||.#..|..|||#.#.#|....#..##|#|...|.|#..||..#...#.
..#..#.||.|...|.|||.|#|..#..|.#.........|...#.#|..
|...||#.####||.......#..|#|.#|..|#..#.|....###|#|.
.|.|||.#..#..#.####.##..|#||.#..|#...|...||....|..
.....||#|...#.##........|..##...#...|..##|#.##....
..|#.|#....|##.#|#.#|..#.#......|#....###.##...#.|
..|.#....##...|||..|.#|#..|..|..||#.....#.#..#....
..|..||..##....#.......#..|......|...#.#.##...||#.
..............######|#...|###.##......#...#.|..#.|
.#..|......##..#..||###|.||....#...||..#.##.#.#.||
##.##......##.#|..|.#.#....|#|#|..|#.##|...|.||#..
|.#...##.|#|.|..|.||.|||.......##..#.#..|...##.|..
....#...#...#||.#.#..#...##.#.#...|#.#..#...|..#.|
....#....|.....||.....|.|#.|.|..||..|#........|...
..#...#...|...###.|..#.#.||||....|.....#|........|
##|#..#.#|#..|.||..||..|.||##..##|#.|.##|....#....
|.#|#||.#...#|...#...#|.##.|..##..||#.||#|......|#
|#|..|.||...#...|####...#....#|...|..#..##...|###.
....##.#.|..|......##...|#.###..#....|###.##.||##|
|..#....#..|#.........|....|....##...#....#.#..|..
.......|..|..#...#....##..#.|.#|..#..|.#.#..|||...
..##||.....#..|....|..|#.|#...#.#|....#|#..||#..|.
.#...##.#..#..#..#..|#..#.......||...#.#.|.##...|.
#..|.#.#...#.|...##|..#.#|##.......|.|..#.|#.....#
..|...#|..#|...#......#..#....|.|.#..#..|#|...#..#
.#..##.|.#.##|..##..||.....|#|.|...|..|..#.....|##
.....#...|....|..|..........##.#..|..###.||#...#|#
.#....|......#.#.#.#..#..#..|.....|..|..|.|...#..#
#|....##....###......#.|..|.#..|..|..|||.##.#....#
.|||##.||......#|.#...|......|...|...#.#..#..#..|#
|.#...#|.#|.##......##...#....|.|..|....#.||#.....
.#..|.|.|...|#..#.####|..#..###.....#.##...###.#..
.#.........|.#......|...##.#|...|.####..|...#.###|"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute(puzzle_input, 1000000000)
    else:
        result = compute(puzzle_input, 10)

    print(f"Result is {result}")

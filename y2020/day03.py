import sys
from functools import reduce, partial

import pytest
from hamcrest import assert_that, is_, has_entries

from lib.maps import Map
from lib.point import Point

TREE = '#'
def compute(data):
    field = Map.from_input(data, [TREE])

    return check_slope(field)


def check_slope(field, move_x = 3, move_y = 1):
    trees = 0
    x = 0
    for y in range(move_y, field.rect.height, move_y):
        x = (x + move_x) % field.rect.width
        if field.features.get(Point(x, y)) == TREE:
            trees += 1
    return trees


def compute2(data):
    field = Map.from_input(data, [TREE])
    return reduce((lambda x, y: x * y),
                  map(
                      lambda e: check_slope(field, e[0], e[1]), [
                          (1, 1),
                          (3, 1),
                          (5, 1),
                          (7, 1),
                          (1, 2),
                      ]))


@pytest.mark.parametrize('val,expect', [
    ("""\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""", 7)
])
def test_v(val, expect):
    assert_that(compute(val), is_(expect))

@pytest.mark.parametrize('val,expect', [
    ("""\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""", 336)
])
def test_v2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = """\
...#..............#.#....#..#..
...#..#..#..............#..#...
....#.#.......#............#...
..##.....##.........#........##
...#...........#...##.#...#.##.
..#.#...#....#.....#........#..
....##.###.....#..#.......#....
.#..##...#.....#......#..#.....
............##.#...#.#.....#.#.
..........#....#....#.#...#...#
..##....#.#.#......#.........#.
#.#.........#..............##..
....##.##......................
....##..#...........#..........
..#..#.#........##....#......#.
..............#..#....#.....#..
.............#...#.....#...#...
.#...........#..........#...#..
.#......#.......#......#.......
#..#.............#..#....##.###
........#.#...........##.#...#.
......#..#.....##......#.......
.....#.....#....#..............
#...##.#......#......#...#.....
...........................#...
...#....................#.....#
..#.....#...#.....##.....#.....
....................#......#..#
.......#.....##......##....#...
#........##...#.....##..#...#..
........#..#.#......#..###..#.#
##.....#.............#.#....#..
..#.................#....######
.#.#..#.....#.#..........#.#...
.........#....#...#............
........#..#.....#.............
............#.#.............##.
...#....#..#......#............
.##....#.....#...#.#...........
..#..............#...........##
.....#.#.##...#................
..........#..#.#..........##..#
..#....#...#...#.....######....
....#.#..#........#....#.###...
.......................#.......
..#.....#.##................#..
.....#......#..#.....#........#
.#...###.......#.#.........#..#
............#..................
..#.........##.........##......
#...........#.#.......###.#....
.#...#.....#.........###.....#.
.#............#........#..#....
...##.#......##................
........#...#...#...#..........
.......#.##......##.#..........
....##.......#..#....#....#....
......#.........###........#...
#....#....####....##......#....
......................#....#.#.
...#.#.#....#.#...#...#......#.
......#.....##.#...........###.
#........#.........##......#.#.
....##.....#.....#..#..........
......#...#...#.........#...##.
..#........#..................#
.........#..##.#..#..#...#.#..#
.....#.....#...#.....###.....##
.............#....#...#........
..........#.#.#...#..#...#....#
#...............##.......#.....
#...#.............#..#...#....#
..#...#...##...##...#..#.......
..#..#........#.#...........#..
.....#.....#..................#
....#....##....###..###...##...
..#......###.........##....#.##
.......#.##...#.......#..#.....
...#.#.#.#.....##..#..#........
................##....#.#......
..#...#...#...#.....##.#...#..#
..#..#.....#..##....#....#.....
.###...#......#........#.....##
##......#..#........#..........
....#...#..#....##..#......####
.#.....##....#..........#......
.#...#....#.........#...#....#.
.....#..#.#..#......#..##....#.
...#.##...#...#........#......#
.#..#...#.#..#.........#...#...
#....#......##.....#.......#...
..##............##..#.#.#...#..
##.......#.......##............
#......#.##........#...#...#...
.#.#.......##.........#..#.#...
.............##.#........#.....
.#..#...###...#..#.............
.....#...#..#....#.......#.....
#.#.........#.#.#...#...#.#....
.....#.......#.##.##...#....#..
.#.##..#.....#...#.#.#.#.#..#..
..........#...................#
.....#.#.#...##.........#..#..#
.#..#....##......#...#.........
.##......#......#...#........#.
.....##.#......#............#.#
.#.....##..#...........##......
.....#......#.......##....#....
..#..##..........#.#..........#
#.#.......##..#..##.#....#.....
.......#..#.#.......##......#.#
....#...##...#..............#..
.....#.........#......#...##...
#.........#........##..#.....#.
.#.#..#.....##.......#......#..
........#..#....#.....###..#...
#.#..#.#..........#............
..#......##..#....#.........#..
#..............................
.......#............#..#..#.#..
.#.....#.#....#..#.##.#........
.......#.###.#........##.#..#..
..............#....#.....##.#..
#..............#....#.###......
.#..#..#...###............#...#
.#.##...#....#..#...#...#......
......##..#..#......#..#....#..
.........#.......##............
...........##...#..#....####...
.#..................#..........
#...#..#..................#....
..............#.....##.....#...
..#.#..#...##..#.....#.....#..#
....#....#.#.........#.....#...
.#.......#...#....#...#.#..#..#
#.........##.....##.......#...#
#..#............#....#........#
..........##...#......#....#...
.......#..##...............#...
#............#.#.#.....#.......
.#........##...#...............
..##....#.....#..#.##.#......#.
.#...#.............#...#.....#.
...##....#.......#......#.#..#.
#......................#..#.##.
...#..........#..#.........#...
..#......#.......#.#....#......
....#............#...#......#..
.....#..#..##...#...#.........#
.....#......#....#....#........
.............#..#..........#...
....#..............#.....#.#...
....#.................#.#...#.#
.........#.#...........###.#.##
#...........#..##.#....#.##.#..
#.#.....#......................
##.#.........#....##.#.#..#.#..
#..........#.#.#.#.#..#..##..#.
..#...#..###.........#......#..
.....#......#..#.#............#
...........#...#.#.#.###....#..
#....#..#.......##.#.......##..
..............#.....##.#.......
.#.....#.#..#.........#.#.#..#.
..#..#..#..#................#..
...........#..#.#...#.........#
.#..#..#...#........#...#.#..#.
...#.#..#......#..#............
........#......##.....#....#...
#...#......##.#.#..............
.#........................#....
#.#.....#.##.....#..#.#........
#..........##.#.......#....#..#
#...#..#..#.....#....#....#....
#...........#..#.#....##.##....
##......#..#........#.......##.
#........#..#...#..........#...
...#...#......##....#.#........
...##..#..#.##....#...#........
#.#..#....#...#........#.......
..........#.......#..........#.
......##...#....###...#....#...
........#..#.....#......#......
....#.........##...#..##......#
....#...........#.#..#.#.#.#..#
..#......#..#......#........#.#
#..#....#.....#.............#..
............................#..
#...#.#.....#...#....#....#....
........#...#...#...#...#......
.###........#....#.##.....##.#.
.........#.....#..........#....
.#.........#....##.#.....#.....
#..#....................##.#...
..##.#.............#....#.#....
..#.#........#............##.#.
#........#...##.....#...#.....#
.........#.#..........#....#..#
...###.#..#.#......#.#.....#...
......#.....#..#...#........#..
.......#...#.....#....#....#..#
.#.#........#......##.......#..
#.................###..........
#........#.#..#....#..#........
..##....#.#...##...#...##....#.
...#.#......##...#.....#..#....
#..#........#...###....#.......
##.#....#..#.#..........#......
....#...###...#.....#........#.
..#.#........#....##.#.........
......##.##.................##.
.#....##...#.#..#.#............
.#...###........#......#.......
##..#.#......#..#..#...#.......
.......##..#....#........#....#
......#..........#.............
....##..##..#......#.#.........
.....#....................##...
...###.....#.....#...#.#.##.#..
....#.#..#.......#..#......##..
.......#.#..#.##.#...#......#..
...#.#....#.#...#..##...#...#..
#.##...#....#..#.............#.
...#...#...#.......#..........#
.#..#.............#..##.#......
....#.......#..............#.#.
..................#..#.....##.#
.#...#..#......#..........#...#
..#.#.....#..#....#....#####.#.
.......###.......#....#....#...
......#.#........#...#.........
......#..#.#.#....#.#.#....##..
.#...#.#...##.#......#.........
#....#..##....#.#.......#....#.
..##.#.....#.....#.........#...
......#......#....#....#.....#.
...##.....#....#......#......#.
......#......##............#.#.
.##.#.......#....#...#....#....
....#..#..#...##.......#..#....
....#....#...#.#........#..#...
....#.....#..........#..#......
....#....#...#.....#..##.....#.
##...#..##......#....##..#..#..
.....##.##..............##.....
#.#....#.##..#....#...##.......
..#.....##.....#.....######...#
...#.....#.#.#......#......##.#
...........##.............#....
...##......#..#......#...#.....
....#.##......#..#....#.#..#...
.#..#....#...#..#.....##.......
.....#..#.................#..#.
................#..#...#......#
...##....#.....#..#....##......
....##...............##...#....
......#..........#..##.........
.......###.......#.........#..#
......................#....#.#.
#.#.....#...##............#....
........#......##......#.....#.
...#....#....#.#..##.#..#.#.#..
..#.#....#.##...#..#.....#.#...
............#....#..#.......#..
#...#...#.#......#...##.....#.#
......#....#....#.......#......
....#.......#..........#....#..
........#####........#....#....
......#....##..............#.#.
....#....#.......#.......#.....
.##.#....##....#...............
#.....##........#..#.#...#.#...
...#......##....#..............
.#.....#.....#.......##....##..
#....#..........#.#..#.........
......##..........##.......#...
.##......##.....#.#....#......#
....#......................#...
.#...........###........#...#..
#.#..#..#..#...##.#....#.#..#..
...##...........#.#..........#.
......#.#..#....#....#.........
....#....#.#......#.........##.
.#..#...#...##....#...#......#.
#.#......#...#.#.#...........#.
##.....#..........##....##..##.
...#.#.....#..##........#......
..#........##........#..#......
.......#...............##..#...
.......#.#....#..###...........
.............#........#...#....
#.................#......#..#..
...#....#..#..............#...#
.............#....##....#..##..
#........#..........##...##...#
............#....#.....#.#....#
.....#..............##..#...#..
..#....#......###....#.#...##..
....##......#.....#....#.......
.....#...............#.....#...
.#.....#.....#..............#..
#................#..#..........
.##....#....#.....#............
#.####...#..#..#....#..........
..##........##.....##......#..#
......#.....#...##.........##..
....##..#.....#.#.........#...#
.....##..#....#....#.#...#..#..
...#............#...........#..
.......#.#..#.#.#..#........#.#
....#.#........#.#.#..#...#...#
..#....#....#..#......#........
.#...........................#.
.#..#....####........##......#.
.#.....#..#.#.................#
.#..#...........#...#....#...#.
......##..#........#..#....#...
..#.............#....#........#
#.#..........#.##.......#.#..#.
..#....#...#...............#...
..............#..........#..#..
..#.....#.#.....#...#...#..#...
.........#...###.#...#........#
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

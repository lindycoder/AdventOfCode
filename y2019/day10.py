import logging
import sys

import pytest
from hamcrest import assert_that, is_

from y2018 import Point
from y2019.lcm import lcm
from y2019.rectangle import Rectangle

ASTEROID = '#'

def compute(data):
    asteroids, w, h = parse(data)

    for asteroid in asteroids.keys():
        for other_asteroid in asteroids.keys():
            if asteroid != other_asteroid:
                if not any(p in asteroids for p in asteroid.raytrace(other_asteroid)):
                    asteroids[asteroid] += 1

    top = max(asteroids.values())

    for asteroid, val in asteroids.items():
        if val == top:
            return asteroid, val


def compute2(data, lazer=Point(20, 18), stop_at=200):  # from compute 1
    asteroids, w, h = parse(data)

    killed = []

    biggest_side = max(lazer.x,
                       w - 1 - lazer.x,
                       lazer.y,
                       h - 1 - lazer.y)

    size = lcm(*list(range(1, biggest_side + 1)))
    # lazer_map = Rectangle(
    #     left=lazer.x - lcm(*list(range(1, lazer.x + 1))),
    #     right=lazer.x + lcm(*list(range(1, w - lazer.x))),
    #     top=lazer.y - lcm(*list(range(1, lazer.y + 1))),
    #     bottom=lazer.y + lcm(*list(range(1, h - lazer.y))),
    # )
    lazer_map = Rectangle(
        left=lazer.x - size,
        right=lazer.x + size,
        top=lazer.y - size,
        bottom=lazer.y + size,
    )

    real_map = Rectangle(
        left=0,
        right=w - 1,
        top=0,
        bottom=h - 1,
    )

    while True:
        for target in lazer_map.perimeter(Point(lazer.x, lazer_map.top)):
            for step in lazer.raytrace(target):
                if step not in real_map:
                    break
                if step in asteroids:
                    asteroids.pop(step)
                    killed.append(step)
                    logging.debug(f'Destroyed {step}, killed={len(killed)}')
                    if len(killed) == stop_at:
                        return step.x * 100 + step.y
                    break

        logging.debug('Full circle done')

def parse(data):
    asteroids = {}
    w, h = 0, 0
    for y, line in enumerate(data.strip().splitlines()):
        for x, char in enumerate(line):
            if char == ASTEROID:
                asteroids[Point(x, y)] = 0
            w = x
        h = y
    return asteroids, w + 1, h + 1

@pytest.mark.parametrize('val,expect1, expect2', [
    ("""\
.#..#
.....
#####
....#
...##""", Point(3, 4), 8),
    ("""\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""", Point(5, 8), 33),
    ("""\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""", Point(1, 2), 35),
    ("""\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""", Point(6, 3), 41),
    ("""\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""", Point(11, 13), 210),
])
def test_v(val, expect1, expect2):
    assert_that(compute(val), is_((expect1, expect2)))

@pytest.mark.parametrize('val,lazer,expect, stop_at', [
#     ("""\
# .#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##""", Point(11, 13), 802, 200),
    ("""\
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""", Point(8, 3), 1403, 36),
])
def test_v2(val, lazer, expect, stop_at):
    assert_that(compute2(val, lazer=lazer, stop_at=stop_at), is_(expect))

def test_parse():
    data = """\
.#..#
.....
#####
....#
...##"""
    assert_that(parse(data), is_(({
        Point(1, 0): 0,
        Point(4, 0): 0,
        Point(0, 2): 0,
        Point(1, 2): 0,
        Point(2, 2): 0,
        Point(3, 2): 0,
        Point(4, 2): 0,
        Point(4, 3): 0,
        Point(3, 4): 0,
        Point(4, 4): 0,
    }, 5, 5)))

puzzle_input = """\
.###.#...#.#.##.#.####..
.#....#####...#.######..
#.#.###.###.#.....#.####
##.###..##..####.#.####.
###########.#######.##.#
##########.#########.##.
.#.##.########.##...###.
###.#.##.#####.#.###.###
##.#####.##..###.#.##.#.
.#.#.#####.####.#..#####
.###.#####.#..#..##.#.##
########.##.#...########
.####..##..#.###.###.#.#
....######.##.#.######.#
###.####.######.#....###
############.#.#.##.####
##...##..####.####.#..##
.###.#########.###..#.##
#.##.#.#...##...#####..#
##.#..###############.##
##.###.#####.##.######..
##.#####.#.#.##..#######
...#######.######...####
#....#.#.#.####.#.#.#.##
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

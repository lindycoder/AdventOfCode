import sys
from collections import Counter
from dataclasses import asdict
from itertools import chain

import pytest
from hamcrest import assert_that, is_

from lib.maps import Map
from lib.point_xd import PointXD, neighbors_xd


def compute(data, dimensions=3):
    features = Map.from_input(data, features=['#']).features

    new_cubes = {PointXD(p.x, p.y, *([0] * (dimensions - 2))) for p in features.keys()}

    neighbors = neighbors_xd(dimensions)

    for _ in range(6):
        active_cubes = new_cubes.copy()

        inactive_cubes = set()
        for cube in active_cubes:
            inactive_cubes.update(cube + n for n in neighbors)
        inactive_cubes -= active_cubes

        new_cubes = set()
        for cube in active_cubes:
            near = sum(1 for n in neighbors if (cube + n) in active_cubes)
            if near in (2, 3):
                new_cubes.add(cube)
        for cube in inactive_cubes:
            near = sum(1 for n in neighbors if (cube + n) in active_cubes)
            if near == 3:
                new_cubes.add(cube)

    return len(new_cubes)


def compute2(data):
    return compute(data, dimensions=4)


@pytest.mark.parametrize('val,expect', [
    ("""\
.#.
..#
###
""", 112)
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("""\
.#.
..#
###
""", 848)
])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = """\
#.##.##.
.##..#..
....#..#
.##....#
#..##...
.###..#.
..#.#..#
.....#..
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

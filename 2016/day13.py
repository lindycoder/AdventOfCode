import sys
import unittest
from copy import deepcopy

from hamcrest import assert_that, is_
from pypaths import astar


def compute_length(data, dest=(31, 39)):
    finder = astar.pathfinder(neighbors=CubicleMap(data))  # Calculate the list of neighbors for a given node

    length, path = finder((1, 1), dest)

    return length


def compute_distinct_locs(data, max_steps=50):
    cubicle_map = CubicleMap(data)

    start = (1, 1)
    paths = [[start]]
    seen = {start: 0}

    while paths:
        current_path = paths.pop(0)
        for neighbor in cubicle_map(current_path[-1]):
            new_path = deepcopy(current_path)
            new_path.append(neighbor)
            if neighbor in seen and len(new_path) >= seen[neighbor]:
                continue

            seen[neighbor] = len(new_path)

            if len(new_path) == max_steps + 1:
                continue

            paths.append(new_path)

    return len(seen)


class CubicleMap(object):
    def __init__(self, code):
        self.code = code
        self.locations = {}

    def __call__(self, coord):
        possible_neighbors = [
            (coord[0], coord[1] + 1),
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1])
        ]

        return [c for c in possible_neighbors if c[0] >= 0 and c[1] >= 0 and self._is_open(c)]

    def _is_open(self, coord):
        if coord not in self.locations:
            x, y = coord
            val = x*x + 3*x + 2*x*y + y + y*y + self.code
            on_bits = "{0:b}".format(val).count("1")
            self.locations[coord] = on_bits % 2 == 0

        return self.locations[coord]


class MapBuilderTest(unittest.TestCase):
    def test_returns_the_correct_list_of_neighbors(self):
        neighbors_list = CubicleMap(10)

        assert_that(neighbors_list((1, 1)), is_([
            (1, 2),
            (0, 1)
        ]))

    def test_returns_the_correct_list_of_neighbors2(self):
        neighbors_list = CubicleMap(10)

        assert_that(neighbors_list((5, 3)), is_([]))

    def test_returns_the_correct_list_of_neighbors3(self):
        neighbors_list = CubicleMap(10)

        assert_that(neighbors_list((3, 2)), is_([
            (3, 3),
            (3, 1),
            (4, 2),
            (2, 2)
        ]))

    def test_dont_go_negative(self):
        neighbors_list = CubicleMap(10)

        assert_that(neighbors_list((0, 0)), is_([
            (0, 1)
        ]))


"""
  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###
"""
class ComputeTest(unittest.TestCase):
    def test_official(self):
        r = compute_length(10, dest=(7, 4))
        assert_that(r, is_(11))

    def test_official2(self):
        r = compute_distinct_locs(10, max_steps=5)
        assert_that(r, is_(11))

    def test_official_official_short(self):
        r = compute_distinct_locs(10, max_steps=1)
        assert_that(r, is_(3))

    def test_official_official_short2(self):
        r = compute_distinct_locs(10, max_steps=2)
        assert_that(r, is_(5))


if __name__ == '__main__':
    puzzle_input = 1352

    if sys.argv[1] == "1":
        result = compute_length(puzzle_input)
    else:
        result = compute_distinct_locs(puzzle_input)

    print("Result is {}".format(result))

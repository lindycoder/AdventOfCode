import sys
import unittest
from functools import partial
from itertools import product, chain
from textwrap import dedent

from hamcrest import assert_that, is_

from y2018 import Point
from y2019.rectangle import Rectangle


def compute(data):
    points = parse_point_list(data)

    boundaries = get_boundaries(points)

    grid = {point: closest_point(points, point) for point in smallest_grid(boundaries)}

    infinity_points = chain(
        product(range(boundaries.left, boundaries.right + 1), [boundaries.top - 1]),
        product(range(boundaries.left, boundaries.right + 1), [boundaries.bottom + 1]),
        product([boundaries.left - 1], range(boundaries.top, boundaries.bottom + 1)),
        product([boundaries.right + 1], range(boundaries.top, boundaries.bottom + 1))
    )

    infinite_areas = list(closest_point(points, Point(*x_y)) for x_y in infinity_points)

    valid_areas = list(filter(lambda e: e not in infinite_areas, points))

    largest_area, size = max(
        ((area, len(list(p for p in grid.values() if p == area)))
         for area in valid_areas),
        key=lambda e: e[1]
    )

    return size


def compute2(data, max_sum=10000):
    points = parse_point_list(data)

    boundaries = get_boundaries(points)

    return len(list(point
                    for point in smallest_grid(boundaries)
                    if sum_all_distances(points, point) < max_sum))


def smallest_grid(boundaries):
    return map(lambda x_y: Point(*x_y), product(range(boundaries.left, boundaries.right + 1),
                                                range(boundaries.top, boundaries.bottom + 1)))


def get_boundaries(points):
    boundaries = Rectangle(
        top=min(p.y for p in points),
        bottom=max(p.y for p in points),
        left=min(p.x for p in points),
        right=max(p.x for p in points)
    )
    return boundaries


def closest_point(points, target):
    distances = list(sorted(
        ((point, point.manhattan_dist(target)) for point in points),
        key=lambda e: e[1]
    ))

    closest, distance = distances[0]
    second_closest, second_distance = distances[1]

    if distance == second_distance:
        return None

    return closest

def sum_all_distances(points, target):
    return sum(point.manhattan_dist(target)
               for point in points)


def parse_point_list(data):
    return [parse_point_line(line) for line in data.split("\n")]

def parse_point_line(line):
    x, y = line.split(", ")
    return Point(x=int(x), y=int(y))


class PointTest(unittest.TestCase):
    def test_manhattan_dist(self):
        assert_that(Point(0, 0).manhattan_dist(Point(0, 0)), is_(0))
        assert_that(Point(0, 0).manhattan_dist(Point(-1, -1)), is_(2))
        assert_that(Point(1, 0).manhattan_dist(Point(-1, -1)), is_(3))
        assert_that(Point(1, 1).manhattan_dist(Point(-1, -1)), is_(4))

    def test_parse(self):
        point1, point2 = parse_point_list("""\
            1, 1
            800, 900""")

        assert_that(point1, is_(Point(x=1, y=1)))
        assert_that(point2, is_(Point(x=800, y=900)))


class ClosestPointTest(unittest.TestCase):
    def setUp(self):
        self.call = partial(closest_point, [Point(0, 0), Point(4, 0)])

    def test_on_a_point_is_itself(self):
        assert_that(self.call(Point(0, 0)), is_(Point(0, 0)))

    def test_near_a_point_returns_that_point(self):
        assert_that(self.call(Point(1, 0)), is_(Point(0, 0)))
        assert_that(self.call(Point(3, 0)), is_(Point(4, 0)))

    def test_close_to_2_points_is_invalid(self):
        assert_that(self.call(Point(2, 0)), is_(None))


class AllDistancesTest(unittest.TestCase):
    def setUp(self):
        self.call = partial(sum_all_distances, [Point(0, 0), Point(4, 0)])

    def test_on_a_point_is_itself(self):
        assert_that(self.call(Point(0, 0)), is_(0 + 4))
        assert_that(self.call(Point(1, 0)), is_(1 + 3))
        assert_that(self.call(Point(3, 0)), is_(3 + 1))


class DayTest(unittest.TestCase):
    def test_provided(self):
        input = dedent("""\
            1, 1
            1, 6
            8, 3
            3, 4
            5, 5
            8, 9""")
        assert_that(compute(input), is_(17))

    def test_provided2(self):
        input = dedent("""\
            1, 1
            1, 6
            8, 3
            3, 4
            5, 5
            8, 9""")
        assert_that(compute2(input, max_sum=32), is_(16))


puzzle_input = """\
194, 200
299, 244
269, 329
292, 55
211, 63
123, 311
212, 90
292, 169
359, 177
354, 95
101, 47
95, 79
95, 287
294, 126
81, 267
330, 78
202, 165
225, 178
266, 272
351, 326
180, 62
102, 178
151, 101
343, 145
205, 312
74, 193
221, 56
89, 89
242, 172
59, 138
83, 179
223, 88
297, 234
147, 351
226, 320
358, 338
321, 172
54, 122
263, 165
126, 341
64, 132
264, 306
72, 202
98, 49
238, 67
310, 303
277, 281
222, 318
357, 169
123, 225"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

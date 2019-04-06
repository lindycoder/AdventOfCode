import unittest

from hamcrest import assert_that, is_

from y2018 import Point, Directions


class PointTest(unittest.TestCase):
    def test_direction_to(self):
        assert_that(Point(2, 2).direction_to(Point(2, 1)), is_(Directions.UP))
        assert_that(Point(2, 2).direction_to(Point(3, 2)), is_(Directions.RIGHT))
        assert_that(Point(2, 2).direction_to(Point(1, 2)), is_(Directions.LEFT))
        assert_that(Point(2, 2).direction_to(Point(2, 3)), is_(Directions.DOWN))

    def test_extended_neighbors(self):
        assert_that(Point(2, 2).extended_neighbors, is_([
            Point(1, 1),
            Point(2, 1),
            Point(3, 1),
            Point(1, 2),
            Point(3, 2),
            Point(1, 3),
            Point(2, 3),
            Point(3, 3)
        ]))

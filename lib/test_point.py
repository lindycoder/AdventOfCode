import unittest

import pytest
from hamcrest import assert_that, is_

from lib.point import Point, Directions, Rotations


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



@pytest.mark.parametrize('p1, p2, steps', [
    (Point(0,0), Point(0, 1), []),
    (Point(0,0), Point(0, 2), [Point(0, 1)]),
    (Point(1,0), Point(0, 0), []),
    (Point(2,0), Point(0, 0), [Point(1, 0)]),
    (Point(0,0), Point(1, 1), []),
    (Point(0,0), Point(2, 2), [Point(1, 1)]),
    (Point(0,0), Point(3, 9), [Point(1, 3), Point(2, 6)]),
    (Point(3,9), Point(0, 0), [Point(2, 6), Point(1, 3)]),
])
def test_raytrace(p1, p2, steps):
    assert_that(list(p1.raytrace(p2)), is_(steps))


@pytest.mark.parametrize('direction,rotation,result', [
    (Directions.UP, Rotations.CW, Directions.RIGHT),
    (Directions.RIGHT, Rotations.CW, Directions.DOWN),
    (Directions.DOWN, Rotations.CW, Directions.LEFT),
    (Directions.LEFT, Rotations.CW, Directions.UP),
    (Directions.UP, Rotations.CCW, Directions.LEFT),
    (Directions.LEFT, Rotations.CCW, Directions.DOWN),
    (Directions.DOWN, Rotations.CCW, Directions.RIGHT),
    (Directions.RIGHT, Rotations.CCW, Directions.UP),
])
def test_directions_turn(direction,rotation,result):
    assert_that(direction.turn(rotation), is_(result))

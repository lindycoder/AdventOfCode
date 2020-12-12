import math
from dataclasses import dataclass
from enum import Enum

import pytest
from hamcrest import assert_that, is_, contains_inanyorder


@dataclass(frozen=True, unsafe_hash=True)
class Point:
    x: int
    y: int

    def manhattan_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __lt__(self, other):
        return self.tuple() < other.tuple()

    def __mul__(self, other: int):
        return Point(self.x * other, self.y * other)

    def tuple(self):
        return self.x, self.y

    def direction_to(self, other):
        return Directions(other - self)

    def raytrace(self, target: 'Point'):
        if target == self:
            return

        dist_x = target.x - self.x
        dist_y = target.y - self.y

        if dist_x == 0:
            step = Point(0, 1 if dist_y > 0 else -1)
        elif dist_y == 0:
            step = Point(1 if dist_x > 0 else -1, 0)
        else:
            d = math.gcd(dist_x, dist_y)
            step = Point(dist_x // d, dist_y // d)

        p = Point(self.x, self.y) + step
        while p != target:
            yield p
            p += step

    @property
    def extended_neighbors(self):
        try:
            return _neighbors_cache[self]
        except KeyError:
            _neighbors_cache[self] = [self + n for n in Directions]
            return _neighbors_cache[self]


_neighbors_cache = {}


class Rotations(Enum):
    CW = 'CW'
    CCW = 'CCW'


@dataclass(frozen=True, unsafe_hash=True)
class Directions(Point, Enum):
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)

    UP_LEFT = UP + LEFT
    UP_RIGHT = UP + RIGHT
    DOWN_RIGHT = DOWN + RIGHT
    DOWN_LEFT = DOWN + LEFT

    def __init__(self, point):
        object.__setattr__(self, "x", point.x)
        object.__setattr__(self, "y", point.y)

    def turn(self, direction: Rotations):
        return _rotations[self, direction]


_rotations = {
    (Directions.UP, Rotations.CW): Directions.RIGHT,
    (Directions.RIGHT, Rotations.CW): Directions.DOWN,
    (Directions.DOWN, Rotations.CW): Directions.LEFT,
    (Directions.LEFT, Rotations.CW): Directions.UP,
    (Directions.UP, Rotations.CCW): Directions.LEFT,
    (Directions.LEFT, Rotations.CCW): Directions.DOWN,
    (Directions.DOWN, Rotations.CCW): Directions.RIGHT,
    (Directions.RIGHT, Rotations.CCW): Directions.UP,
}


##### TEST


@pytest.mark.parametrize('p,mul,expected', [
    (Point(0,0), 10, Point(0,0)),
    (Point(1,1), 10, Point(10,10)),
    (Point(3,-4), 10, Point(30,-40)),
    (Point(-4, 1), 0, Point(0, 0)),
    (Point(-4, 1), 1, Point(-4, 1)),
])
def test_mul(p,mul,expected):
    assert_that(p * mul, is_(expected))


def test_direction_to():
    assert_that(Point(2, 2).direction_to(Point(2, 1)), is_(Directions.UP))
    assert_that(Point(2, 2).direction_to(Point(3, 2)), is_(Directions.RIGHT))
    assert_that(Point(2, 2).direction_to(Point(1, 2)), is_(Directions.LEFT))
    assert_that(Point(2, 2).direction_to(Point(2, 3)), is_(Directions.DOWN))


def test_extended_neighbors():
    assert_that(Point(2, 2).extended_neighbors, contains_inanyorder(
        Point(1, 1),
        Point(2, 1),
        Point(3, 1),
        Point(1, 2),
        Point(3, 2),
        Point(1, 3),
        Point(2, 3),
        Point(3, 3)
    ))


@pytest.mark.parametrize('p1, p2, steps', [
    (Point(0, 0), Point(0, 0), []),
    (Point(0, 0), Point(0, 1), []),
    (Point(0, 0), Point(0, 2), [Point(0, 1)]),
    (Point(1, 0), Point(0, 0), []),
    (Point(2, 0), Point(0, 0), [Point(1, 0)]),
    (Point(0, 0), Point(1, 1), []),
    (Point(0, 0), Point(2, 2), [Point(1, 1)]),
    (Point(0, 0), Point(3, 9), [Point(1, 3), Point(2, 6)]),
    (Point(3, 9), Point(0, 0), [Point(2, 6), Point(1, 3)]),
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
def test_directions_turn(direction, rotation, result):
    assert_that(direction.turn(rotation), is_(result))

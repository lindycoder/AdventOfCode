import math
from dataclasses import dataclass
from enum import Enum
from itertools import groupby


@dataclass(unsafe_hash=True)
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

    def tuple(self):
        return self.x, self.y

    def direction_to(self, other):
        return Directions(other - self)

    def raytrace(self, target: 'Point'):

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
            _neighbors_cache[self] = [self + n for n in _extended_neighbors]
            return _neighbors_cache[self]


_neighbors_cache = {}


class Rotations(Enum):
    CW = 'CW'
    CCW = 'CCW'


class Directions(Enum):
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)

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

_extended_neighbors = [
    Directions.UP.value + Directions.LEFT.value,
    Directions.UP.value,
    Directions.UP.value + Directions.RIGHT.value,
    Directions.LEFT.value,
    Directions.RIGHT.value,
    Directions.DOWN.value + Directions.LEFT.value,
    Directions.DOWN.value,
    Directions.DOWN.value + Directions.RIGHT.value,
]


def group(iterable, key):
    return groupby(sorted(iterable, key=key), key=key)

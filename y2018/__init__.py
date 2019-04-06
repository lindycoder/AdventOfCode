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

    @property
    def extended_neighbors(self):
        try:
            return _neighbors_cache[self]
        except KeyError:
            _neighbors_cache[self] = [self + n for n in _extended_neighbors]
            return _neighbors_cache[self]

_neighbors_cache=  {}

class Directions(Enum):
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)


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

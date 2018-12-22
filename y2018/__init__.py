from dataclasses import dataclass
from enum import Enum


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


class Directions(Enum):
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    UP = Point(0, -1)
    DOWN = Point(0, 1)

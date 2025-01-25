from dataclasses import dataclass
from itertools import count
from typing import Self

import pytest
from hamcrest import assert_that, is_, has_properties

from lib.point import Directions, Point


@dataclass(frozen=True)
class Rectangle:
    left: int
    right: int
    top: int
    bottom: int

    @classmethod
    def by_size(cls, width: int, height: int) -> Self:
        return cls(0, width - 1, 0, height - 1)

    # def perimeter(self, start: Point):
    #     if start.x == self.left:
    #         points = [self.top_left, self.top_right, self.bottom_right,
    #                   self.bottom_left]
    #     elif start.x == self.right:
    #         points = [self.bottom_right, self.bottom_left, self.top_left,
    #                   self.top_right]
    #     elif start.y == self.top:
    #         points = [self.top_right, self.bottom_right, self.bottom_left,
    #                   self.top_left]
    #     elif start.y == self.bottom:
    #         points = [self.bottom_left, self.top_left, self.top_right,
    #                   self.bottom_right]
    #     else:
    #         raise Exception('Point not on rectangle')
    #
    #     yield start
    #     current = start
    #     for p in points + [start]:
    #         if current != p:
    #             yield from current.raytrace(p)
    #         if p != start:
    #             yield p
    #         current = p

    @property
    def top_left(self):
        return Point(self.left, self.top)

    @property
    def top_right(self):
        return Point(self.right, self.top)

    @property
    def bottom_left(self):
        return Point(self.left, self.bottom)

    @property
    def bottom_right(self):
        return Point(self.right, self.bottom)

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    def find_edge(self, point: Point, direction: Directions):
        for i in count(0):
            check_p = point + direction * i
            if check_p not in self:
                return point + direction * (i - 1)

    def __contains__(self, item):
        return self.left <= item.x <= self.right and self.top <= item.y <= self.bottom

    def expand(self) -> "Rectangle":
        return Rectangle(self.left-1, self.right+1, self.top-1,self.bottom+1)


# @pytest.mark.parametrize('rect,start,points', [
#     (Rectangle(0, 1, 0, 1), Point(0, 0),
#      [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]),
#     (Rectangle(0, 2, 0, 2), Point(1, 0),
#      [Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2), Point(1, 2),
#       Point(0, 2), Point(0, 1), Point(0, 0)]),
# ])
# def test_perimeter(rect, start, points):
#     assert_that(list(rect.perimeter(start)), is_(points))


@pytest.mark.parametrize('rect,point,expected', [
    (Rectangle(0, 1, 0, 1), Point(0, 0), True),
    (Rectangle(0, 1, 0, 1), Point(-1, 0), False),
    (Rectangle(0, 1, 0, 1), Point(0, -1), False),
    (Rectangle(0, 1, 0, 1), Point(1, 1), True),
    (Rectangle(0, 1, 0, 1), Point(2, 1), False),
    (Rectangle(0, 1, 0, 1), Point(1, 2), False),
])
def test_insize(rect, point, expected):
    assert_that(point in rect, is_(expected))


@pytest.mark.parametrize('val, matches', [
    (Rectangle.by_size(1, 1), Rectangle(0, 1, 0, 1)),
    (Rectangle.by_size(10, 10), Rectangle(0, 10, 0, 10)),
])
def test_by_size(val, matches):
    assert_that(val, is_(matches))


@pytest.mark.parametrize('val, matches', [
    (Rectangle.by_size(1, 1), has_properties(width=1, height=1)),
    (Rectangle.by_size(10, 10), has_properties(width=10, height=10)),
])
def test_by_size(val, matches):
    assert_that(val, matches)

@pytest.mark.parametrize('point, direction, expected', [
    (Point(0, 0), Directions.UP, Point(0, 0)),
    (Point(0, 0), Directions.UP_RIGHT, Point(0, 0)),
    (Point(0, 0), Directions.RIGHT, Point(10, 0)),
    (Point(0, 0), Directions.DOWN_RIGHT, Point(10, 10)),
    (Point(0, 0), Directions.DOWN, Point(0, 10)),
    (Point(2, 4), Directions.UP, Point(2, 0)),
    (Point(2, 4), Directions.UP_RIGHT, Point(6, 0)),
    (Point(2, 4), Directions.RIGHT, Point(10, 4)),
    (Point(2, 4), Directions.DOWN_RIGHT, Point(8, 10)),
    (Point(2, 4), Directions.DOWN, Point(2, 10)),
    (Point(2, 4), Directions.DOWN_LEFT, Point(0, 6)),
    (Point(2, 4), Directions.LEFT, Point(0, 4)),
    (Point(2, 4), Directions.UP_LEFT, Point(0, 2)),
])
def test_find_edge(point, direction, expected):
    r = Rectangle.by_size(10, 10)
    assert_that(r.find_edge(point, direction), is_(expected))


def test_expand():
    initial = Rectangle(0, 1, 0, 1)

    assert_that(initial.expand(), is_(Rectangle(-1, 2, -1, 2)))

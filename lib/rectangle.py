from dataclasses import dataclass

import pytest
from hamcrest import assert_that, is_, has_properties

from y2018 import Point


@dataclass
class Rectangle:
    left: int
    right: int
    top: int
    bottom: int

    @classmethod
    def by_size(cls, width: int, height: int) -> 'Rectangle':
        return cls(0, width, 0, height)

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

    def __contains__(self, item):
        return self.left <= item.x <= self.right and self.top <= item.y <= self.bottom


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

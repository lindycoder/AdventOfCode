import re
from dataclasses import dataclass

import pytest
from hamcrest import assert_that, is_


@dataclass
class Point3d:
    x: int
    y: int
    z: int

    _parse_regex = re.compile('^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$')

    @classmethod
    def from_string(cls, s):
        return cls(*list(map(int, cls._parse_regex.match(s).groups())))

    def __add__(self, other):
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)


    def __str__(self):
        return f'<x={self.x}, y={self.y}, z={self.z}>'


@pytest.mark.parametrize('s,expected', [
    ('<x=2, y=-10, z=-7>', Point3d(2, -10, -7))
])
def test_from_string(s, expected):
    assert_that(Point3d.from_string(s), is_(expected))


@pytest.mark.parametrize('a,b,expected', [
    (Point3d(2, -10, -7), Point3d(2, -10, -7), Point3d(4, -20, -14))
])
def test_add(a, b, expected):
    assert_that(a + b, is_(expected))

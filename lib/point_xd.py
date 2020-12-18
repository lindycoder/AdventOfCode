from dataclasses import dataclass
from dataclasses import dataclass
from itertools import product
from typing import Tuple

import pytest
from hamcrest import assert_that, has_length


@dataclass(frozen=True, init=False)
class PointXD:
    coords: Tuple[int, ...]

    def __init__(self, *args):
        object.__setattr__(self, 'coords', args)

    def __add__(self, other: 'PointXD') -> 'PointXD':
        return self.__class__(*(a + b
                                for a, b
                                in zip(self.coords, other.coords)))


def neighbors_xd(dimensions):
    vals = (-1, 0, 1)
    neighbors = [PointXD(*values) for values in product(*(vals for _ in range(dimensions)))]
    neighbors.remove(PointXD(*([0] * dimensions)))
    return neighbors


@pytest.mark.parametrize('dimensions', range(2, 10))
def test_neighbors_xd(dimensions: int):
    assert_that(neighbors_xd(dimensions), has_length((3 ** dimensions) - 1))


@pytest.mark.parametrize('dimensions', range(2, 10))
def test_point_xd_add(dimensions: int):
    a = PointXD(*(i for i in range(dimensions)))
    b = PointXD(*(i * 2 for i in range(dimensions)))
    expected = PointXD(*(i * 2 + i for i in range(dimensions)))

    assert_that(a + b, expected)


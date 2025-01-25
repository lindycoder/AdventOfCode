from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, Container, Dict, Optional, Self

import pytest
from hamcrest import has_entries, assert_that, has_properties

from lib.point import Point
from lib.rectangle import Rectangle


@dataclass(frozen=True)
class Map:
    features: Mapping[Point, str]
    rect: Rectangle

    @classmethod
    def from_input(cls, data: str, features: Container[str]) -> Self:
        points = {}
        lines = data.splitlines()
        for y, line in enumerate(lines):
            for x, content in enumerate(line):
                if not features or content in features:
                    points[Point(x, y)] = content

        return cls(points, Rectangle.by_size(len(lines[0]), len(lines)))

    def __str__(self):
        out = f"Map <{self.rect}>\n"
        lines = []
        for y in range(self.rect.top, self.rect.bottom + 1):
            lines.append(
                "".join(
                    self.features.get(Point(x, y), " ")
                    for x in range(self.rect.left, self.rect.right + 1)
                )
            )
        return out + "\n".join(lines)

    def __getitem__(self, item: Point) -> str:
        return self.features.__getitem__(item)

    def items(self) -> Iterable[tuple[Point, str]]:
        return self.features.items()

    def get(self, p: Point, default: Optional[str] = None) -> str:
        return self.features.get(p, default)

    @property
    def top_right(self):
        return self.rect.top_right

    @property
    def top_left(self):
        return self.rect.top_left

    @property
    def bottom_right(self):
        return self.rect.bottom_right

    @property
    def bottom_left(self):
        return self.rect.bottom_left


@pytest.mark.parametrize(
    "val, features, expect",
    [
        (
            dedent(
                """\
                .#.
                #.#
                """
            ),
            None,
            has_properties(
                features=has_entries(
                    Point(0, 0),
                    ".",
                    Point(1, 0),
                    "#",
                    Point(2, 0),
                    ".",
                    Point(0, 1),
                    "#",
                    Point(1, 1),
                    ".",
                    Point(2, 1),
                    "#",
                ),
                rect=has_properties(
                    width=2,
                    height=1,
                ),
            ),
        ),
        (
            dedent(
                """\
                .#.
                #.#
                """
            ),
            ("#,"),
            has_properties(
                features=has_entries(
                    Point(1, 0),
                    "#",
                    Point(0, 1),
                    "#",
                    Point(2, 1),
                    "#",
                )
            ),
        ),
    ],
)
def test_map_from_input(val, features, expect):
    assert_that(Map.from_input(val, features), expect)


@pytest.mark.parametrize(
    "prop,matches",
    [
        ("top_left", Point(0, 0)),
        ("top_right", Point(2, 0)),
        ("bottom_right", Point(2, 2)),
        ("bottom_left", Point(0, 2)),
    ],
)
def test_map_locations(prop, matches):
    map = Map.from_input(
        dedent(
            """\
            ...
            .#.
            ...
            """
        ),
        features=("#",),
    )

    assert_that(map, has_properties(prop, matches))

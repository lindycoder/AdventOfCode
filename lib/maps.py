from dataclasses import dataclass
from typing import Any, Dict, List

import pytest
from hamcrest import has_entries, assert_that, is_, all_of, has_properties

from lib.point import Point
from lib.rectangle import Rectangle


@dataclass
class Map:
    features: Dict[Point, Any]
    rect: Rectangle

    @classmethod
    def from_input(cls, data: str, features: List[str]) -> 'Map':
        points = {}
        lines = data.strip().splitlines()
        for y, line in enumerate(lines):
            for x, content in enumerate(line):
                if not features or content in features:
                    points[Point(x, y)] = content

        return cls(points, Rectangle.by_size(len(lines[0]), len(lines)))

    def __str__(self):
        out = f'Map <{self.rect}>\n'
        lines= []
        for y in range(self.rect.top, self.rect.bottom + 1):
            lines.append(''.join(self.features.get(Point(x, y), ' ')
                           for x in range(self.rect.left, self.rect.right + 1)))
        return out + '\n'.join(lines)


@pytest.mark.parametrize('val, features, expect', [
    ("""\
.#.
#.#
""",
     None,
     has_properties(
         features=has_entries(
             Point(0, 0), '.',
             Point(1, 0), '#',
             Point(2, 0), '.',
             Point(0, 1), '#',
             Point(1, 1), '.',
             Point(2, 1), '#',
         ),
         rect=has_properties(
             width=3,
             height=2,
         )
     )),
    ("""\
.#.
#.#
""",
     ('#,'),
     has_properties(
         features=has_entries(
             Point(1, 0), '#',
             Point(0, 1), '#',
             Point(2, 1), '#',
         )))
])
def test_map_from_input(val, features, expect):
    assert_that(Map.from_input(val, features), expect)

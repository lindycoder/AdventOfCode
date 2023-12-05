import re
import sys
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from textwrap import dedent
from typing import Optional

import pytest
from hamcrest import assert_that, is_, contains_exactly, any_of

from lib.maps import Map
from lib.point import Point
from lib.rectangle import Rectangle

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    symbols = re.findall("[^0-9.\n]", data.strip())
    symbol_map = Map.from_input(data, symbols)

    part_numbers = extract_numbers(data)
    pn_with_symbols = filter(partial(has_adjacent_symbol, symbol_map), part_numbers)
    return sum(p.number for p in pn_with_symbols)


def compute2(data: str) -> int | str:
    symbol_map = Map.from_input(data, "*")

    gears = defaultdict(list)
    for part_number in extract_numbers(data):
        if adjacent_gear := get_adjacent_symbol_point(symbol_map, part_number):
            gears[adjacent_gear].append(part_number.number)

    real_gears = filter(lambda e: len(e) == 2, gears.values())
    return sum(a * b for a, b in real_gears)


@dataclass(frozen=True)
class PartNumber:
    number: int
    location: Rectangle


DIGITS_RE = re.compile(r"\d+")


def extract_numbers(raw: str) -> Iterable[PartNumber]:
    for row, line in enumerate(raw.strip().splitlines()):
        for match in DIGITS_RE.finditer(line):
            start = match.span(0)[0]
            part_number = match.group(0)

            yield PartNumber(
                number=int(part_number),
                location=Rectangle(
                    left=start, right=start + len(part_number) - 1, top=row, bottom=row
                ),
            )


def get_adjacent_symbol_point(
    symbol_map: Map, part_number: PartNumber
) -> Optional[Point]:
    rect = part_number.location.expand()
    for point in (
        rect.top_left,
        *rect.top_left.raytrace(rect.top_right),
        rect.top_right,
        *rect.top_right.raytrace(rect.bottom_right),
        rect.bottom_right,
        *rect.bottom_right.raytrace(rect.bottom_left),
        rect.bottom_left,
        *rect.bottom_left.raytrace(rect.top_left),
    ):
        if symbol_map.get(point) is not None:
            return point

    return None


def has_adjacent_symbol(symbol_map: Map, part_number: PartNumber) -> bool:
    return get_adjacent_symbol_point(symbol_map, part_number) is not None


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1", {PartNumber(number=1, location=Rectangle(0, 0, 0, 0))}),
        ("23", {PartNumber(number=23, location=Rectangle(0, 1, 0, 0))}),
        ("456", {PartNumber(number=456, location=Rectangle(0, 2, 0, 0))}),
        ("...\n456\n...", {PartNumber(number=456, location=Rectangle(0, 2, 1, 1))}),
        ("..456..", {PartNumber(number=456, location=Rectangle(2, 4, 0, 0))}),
        (".\n.456.\n.", {PartNumber(number=456, location=Rectangle(1, 3, 1, 1))}),
    ],
)
def test_extract_numbers(raw: str, expected: set[PartNumber]):
    assert_that(list(extract_numbers(raw)), contains_exactly(*expected))


@pytest.mark.parametrize(
    ("symbols", "expected"),
    [
        ([], False),
        ([Point(0, 1)], False),
        ([Point(1, 1)], True),
        ([Point(2, 1)], True),
        ([Point(3, 1)], True),
        ([Point(4, 1)], True),
        ([Point(5, 1)], False),
        ([Point(0, 2)], False),
        ([Point(1, 2)], True),
        ([Point(4, 2)], True),
        ([Point(5, 2)], False),
        ([Point(0, 3)], False),
        ([Point(1, 3)], True),
        ([Point(2, 3)], True),
        ([Point(3, 3)], True),
        ([Point(4, 3)], True),
        ([Point(5, 3)], False),
        ([Point(1, 1), Point(1, 2)], True),
    ],
    ids=str,
)
def test_adjacency(symbols: Sequence[Point], expected: bool):
    symbols_map = Map(features={p: "*" for p in symbols}, rect=Rectangle(0, 0, 0, 0))
    part_number = PartNumber(number=12, location=Rectangle(2, 3, 2, 2))

    assert_that(has_adjacent_symbol(symbols_map, part_number), is_(expected))
    if expected:
        assert_that(
            get_adjacent_symbol_point(symbols_map, part_number), is_(any_of(*symbols))
        )
    else:
        assert_that(get_adjacent_symbol_point(symbols_map, part_number), is_(None))


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            dedent(
                """\
                467..114..
                ...*......
                ..35..633.
                ......#...
                617*......
                .....+.58.
                ..592.....
                ......755.
                ...$.*....
                .664.598..                
                """
            ),
            4361,
        ),
        (puzzle_input, 540025),
    ],
)
def test_compute(val: str, expect: int | str):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            dedent(
                """\
                467..114..
                ...*......
                ..35..633.
                ......#...
                617*......
                .....+.58.
                ..592.....
                ......755.
                ...$.*....
                .664.598..
                """
            ),
            467835,
        )
    ],
)
def test_compute2(val: str, expect: int | str):
    assert_that(compute2(val), is_(expect))


if __name__ == "__main__":
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

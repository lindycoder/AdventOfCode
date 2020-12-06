import sys
from dataclasses import dataclass
from operator import attrgetter
from typing import ClassVar, Iterable, Mapping

import pytest
from hamcrest import assert_that, has_properties, is_


def compute(data):
    return max(map(attrgetter('id'), parse(data)))


def compute2(data):
    all_ids = sorted(map(attrgetter('id'), parse(data)))
    for s1, s2 in zip(all_ids[:-1], all_ids[1:]):
        if s2 - s1 == 2:
            return s1 + 1


def parse(data: str) -> Iterable['Seat']:
    return map(Seat.from_boarding_pass, data.strip().splitlines())


@dataclass
class Seat:
    row: int
    column: int

    _row_chars: ClassVar[Mapping[str, int]] = {
        'F': 0,
        'B': 1,
    }
    _column_chars: ClassVar[Mapping[str, int]] = {
        'L': 0,
        'R': 1,
    }

    @property
    def id(self):
        return self.row * 8 + self.column

    @classmethod
    def from_boarding_pass(cls, data: str) -> 'Seat':
        return cls(
            row=_bin_partitioning_location(cls._row_chars, data[:7]),
            column=_bin_partitioning_location(cls._column_chars, data[-3:]),
        )


def _bin_partitioning_location(chars: Mapping[str, int], data: str) -> int:
    max_power = len(data) - 1
    total = 0
    for i, char in enumerate(data):
        total += chars[char] * (2 ** (max_power - i))
    return total


@pytest.mark.parametrize('code,row,col,seat_id', [
    ('FBFBBFFRLR', 44, 5, 357),
    ('BFFFBBFRRR', 70, 7, 567),
    ('FFFBBBFRRR', 14, 7, 119),
    ('BBFFBBFRLL', 102, 4, 820),
])
def test_seat_parse(code, row, col, seat_id):
    assert_that(Seat.from_boarding_pass(code), has_properties(
        row=row,
        column=col,
        id=seat_id
    ))


@pytest.mark.parametrize('data,match', [
    ("""
FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
""", 820)
])
def test_compute(data, match):
    assert_that(compute(data), is_(match))


@pytest.mark.parametrize('data,match', [
    ("""
BFFFBBFRLL
BFFFBBFRLR
BFFFBBFRRR
""", 566)
])
def test_compute2(data, match):
    assert_that(compute2(data), match)


puzzle_input = """\
BFFBFBFLRL
BFBFBBBLRR
BFBFBFBLRR
BFBFFFFRLR
BBFFBBFRRR
FBBBFFFRLL
FFBFBFFLLL
BBFBFFFRLL
FBBBFFBLRR
FFFFBFFRRL
BFBFBFBRLL
FFBFFBBLLL
BFFBBFFRLR
FBBFFFFLRR
FBFBFFBRRR
FFBFFBBRRR
FBBBFFFRRL
FFBBBBFRRL
BFFBBBBLLL
BFBBFBBLLR
FBBFBFFLLR
FBBFBFFLRR
BFFFFBFLLL
FBBBBBBRRR
FBFFBBFLLR
BBFBFFBRLR
FFFFFBBLLR
FBBFBBBRLL
FFFFBBFRRR
FFFFBFBLRL
FFFBFBFLLR
FFBFBBBLRR
BFFBBBFRLR
FFFBFBBLLL
FBFBBBFLRR
BBFFFBFLLL
FFFFFBBLRR
FFBFBFFRLL
BFFFBBFRLR
BFBBBFBLLR
FFFBBFFLRL
BFBBBFBLLL
FBFBBFBRLR
BBFFBFFRRR
BFFFFBBLRR
FBBBBBFLRL
FBFBBBBRRR
FBFBBFFLLL
BFBBBFBRLL
FFBBFBBLRR
FFBFBBBRRR
FFFFFBFLRL
BFFBBBFLRR
BFBBFBFLLR
FFBFBBBLRL
FBBBBFBLLL
BFBBBFFLRR
FBBFFBBLRR
BFFBBFBLRR
FBBBBBFLLL
FFFFBBBRLR
FBFBBBFLLR
BFBFFBFRLR
BFFBFFBRRR
FBBFFFFLRL
BFBFBBFLRL
BBFBFFFRLR
FBFFFFBLRR
BFFFBFFRLL
FBFFBFBLLR
FFFBFFFRLR
FFFBFFFRLL
BFFBFBBLLL
FFBBFBBLRL
BFBBBBFLRL
BFBBBBFLRR
BFBFFFFRRL
BFBBBFBRLR
BBFFBBBLLR
FBBFBBFRLR
FBFBFBFLLR
BFBFFBBRRR
FFFFBBFLLR
FBFFBFFLLL
BFFFFFBRLR
FBFBBBFLRL
BFFFBBFLLR
FBFBFBBRRR
FBFFBFBLRL
BBFFFBBLLL
FBFFFBFRRL
BBFFFFBRLR
BBFFBFBRRL
BFFBBBBRLR
FBFFFBBLRL
FBBFBBFLLR
FFBBBBBLLL
FBBBBBFLLR
FFBFFBFRLR
BFFBBFBLRL
FFBBBBFRLR
BFFBFBBRRL
FBFBBBFLLL
BBFBFFBRRR
FBFBBFFLLR
BFFFFFBRLL
FBBBBFBLLR
FFBBBFBLRR
FBBBBFBRLR
FBBBBBBRRL
FBBFFFBRRL
FBFBFFFLRR
FBBFFFBRLR
BFFBFBFRRL
FFBFBBFRLL
FBFBFFFRRR
BFFFFBFRRR
FFFFFBFRRL
BBFFBFFLRL
FBBBBBBLLR
BFFFBFFRRR
FFFFFBFRLL
FBBFBFBLLL
FFFFBBFLRR
BFBBFFFRLR
FFBFFBBLRR
FBFFBFBLRR
FFBBBFBLRL
FFFBBFBRLR
BFBFFBBLLR
FFFBBFBLLL
BBFFFBBLRL
FBFBFFFRLR
BBFFBFFRLR
FFFBFBFRLR
FFBBBBFLLR
BBFFBFFLRR
FFFFFBFRLR
BFBFBBFRRR
BBFFFBFRRL
BFFBFBFLLR
FFFBBBBLLL
BFFFBBFLLL
BBFFFBBRRL
BFFFFBFRLL
BFBFBBBLLR
BBFBFFBRRL
FBFFBBFLLL
FBFBFFFRRL
FBBFBBBLRR
BFBBFFBRLL
FBFBBBBRLR
FFFBBFFLRR
FBBFFBFRRL
BFFBBBBLRR
FFFFBBFRLR
FBFBBBFRRR
BFFBFFFRLL
BFFFFFFRRL
FBFFFFBRLR
BFFFFBBRRL
FBBBBBFRLR
FBBBBFBLRR
FFFBBFBRLL
FBBFBBFRRL
FFFBBBBRRL
FBBFFBBRRL
BFFBBFFLLR
FFFBFFBRRL
FBFFBFFLLR
FFFFFFBRLL
FFBBFBBRLR
FFBBFBFLRR
FFFBFFBRRR
FFBFFBBLLR
BFBFBFBLLR
FFBBBBFRRR
BFBBBFBLRL
BFFFBBFRRL
FBFBBBFRLL
BBFFFFBRRR
FBBFBFBRLR
BFBBBFFRRL
FBBBBFBRRL
FBBBFFBLRL
FBFFFBBRRL
BFBBFFBRRL
FBFBBFFLRL
FBFBBBBLRL
FFBBBFBRRL
FBBBBBBLRL
FFFFBBFRLL
FBFBBFBRLL
BFBFBBFLLR
FBFFFBBRLR
BFBFBBBRRR
FBBBBBBLRR
BFFBFFBRRL
FFBBBBBRLR
BFFFBBFLRL
FBFBBBBRLL
FFFFFBFRRR
BFBBBBFRLR
FFBFFBFRRL
FBBBBBBRLR
FBFFFBBLRR
FFFBFFBRLR
BFBFFBFLLR
FFFFFBBRRL
FBBBBBFRRL
FFFFBBBRRR
BFBBFFFRLL
BBFFBFBLLR
FFFFBFFLRR
FBFFFBFLLL
FBBFFBFRLR
BBFBFFBLLR
BBFBFFFLRL
BFFFBBBRLR
BFFBFFBLRL
BFBFBFFLRL
FBBFFBBRLR
FBFBFBBRLL
FFBFFFFLLL
FFFFBFBLLL
FBBFFBBLLR
FFFFBBBLRR
FFFFFBBRRR
BBFFFFFRLL
FBFBBFBRRR
FBBFFFFRRR
FFFFBFBRLR
BFFFFBBLLR
FFFBBBFRLL
BFFBBBBRRR
FBFFBBFRLL
BFBBFBFLRL
FBFBFBBLLL
FFBFFFFRRL
FBFBBBFRRL
FBBBBBBRLL
BFFFBFBRRR
BFBFBFBRRR
FBFFFBBRLL
BFFFFBBLLL
FFFBFFFRRL
FBBBBFFRRL
BFFFFFFLRR
BFBFBFFLRR
BFFFFBBRLL
FBBFFFFRRL
BFBBFBBRRR
FFFBFFBLLR
BFFBFFFRLR
FFBFFFBLLR
BFBFBFBLLL
BFFBFFFLRR
FFBBFFBLRR
FBBFFBFRLL
FFBFBFBRRL
FBFFFFFLLR
FBFFBBFRLR
FBFBBBFRLR
FFBBFFFLRR
FBBFFFFLLL
FFFBFFFLRL
BFFBBFBLLR
BFFFFFBLLL
BBFBFFBLLL
BFFBFBBLRR
BBFFFFBRLL
FBFFBFFLRL
FBBFFFFLLR
FFFBBFFRLR
FFFBBFBLRL
BFFBBBBLLR
BFBBBFBRRL
FFBBBFFLRR
FBBFFBBRLL
FFFBFBBRRR
BFFBFFFLRL
BFFFBFFLLR
FFFBFBFLLL
FFBFBFFRRL
FFFBFFFRRR
BFBFFFFLRL
BFFFFFBRRL
FFFBFBBLRL
FBFFBFFRRL
FFFFBFFLLR
FFBBBBFRLL
FBBBBFFLRR
FFFFBFFLLL
BFBBBBFRRL
FBFBBFFLRR
FFBBFBFRLL
FFFBFBBRLL
BFFFFFFLRL
BBFFFFBLRL
BFFFFFFRLR
FBFFFBFRLR
FBFFFFFLRL
BFBFBFFRLL
FFBBFBFLRL
FFFBBBFLLR
FBBFFFBRRR
FFFFFBFLRR
FBFFFBBLLR
FFFFBFBLRR
FBBFBBBLLR
FBBBFFBLLL
BBFFBFFRRL
BFBBFBBLLL
FBFFBFFRRR
FBFFFFBRLL
FFBBBFBRRR
FBBFFBBLLL
BBFFBBBRLL
FBFFFBFLRR
FBBBFFBRLR
FFBBBBBLLR
FBFFFFBLRL
BFFFBFBRLL
FFFFFBBLRL
BFBBFFBLLL
BBFFBBFLRR
BBFFBFFLLL
FBFBFFBRRL
BFFBBFFRRL
BFFBBFBRRR
FFBBBFBRLL
FBBFBFBRRL
FBFBBFBLLL
BFFFBBBLLL
FFFBBBFLRL
BFBBFFFLRL
FFFBFFBLLL
FFBBFBBRRR
FBBBBFFLLL
BBFBFFFRRR
FFBFFBFLRR
BFFBBFBLLL
BFFFBFBLLR
FFBBFBFRRR
BBFFFBBLRR
FFFFBFFRLL
BFBBBFFRLL
BFBFBFFRRL
BFBFFBBLRR
FBBFFFFRLL
FFFBFBBLLR
BBFFBBBLRR
FFBFBFBRLR
BBFFBBFLRL
BBFFFBBLLR
BFFFBBFLRR
FBBBBFFRLL
FBBFFFBLRR
BFBFBFBRLR
FBFBBFFRLR
FFFFBFFLRL
FBBBFBBLLR
FBFFFFFRLR
FBBFBBFLRR
BFBFBFFRLR
FFBFFBFLLR
FFFFBBBRLL
FBBBFBBRLL
FFFBFBFLRL
BFBBFFFLLR
BFFBFFBLRR
BFFFBFFRLR
FBBFFBFLLL
FBFBBBBRRL
FBBBBBFRLL
FBFFBBBRLR
FFBFFFBRRL
FFBFFBFLLL
BFBFBBFRLR
BFFFBFFLRL
FFBBBBBRRL
FBBFFBBLRL
FBFFFBBRRR
FBBFBFFLRL
BFFBFBFLRR
FFBBBFFRRR
BFBFFBBRLR
FBFBFBFRRL
FFBFBBBLLL
FBBFFFBLLL
FFFBBFBRRL
FFFFBBBRRL
FBBBFBFLLR
FBBBBBFRRR
FBFBBBBLLL
FFFBFBBLRR
FFBBFBBLLL
FBBFBBFLLL
FBFFFFBRRR
FBBBFFFLRR
FFFBFBBRLR
FBFFFFFRRR
BFBBFBFLLL
BFFFBBFRRR
BFFFBFBLRR
FBFFBFBRLR
BFBFFFBRLR
BFBBBBBLRL
BBFFBFBRRR
FFBFFFFRLL
FFFFFBFLLR
FBBBFBFRRR
BFBFFFBRRR
FBFBFFBLRL
FBFFBFBLLL
FBBFFFBLRL
BFFBFBBRLL
FFFBFFBLRR
BFBBFBFLRR
FBBFBBFRLL
FFBFBFFLLR
FFBBFBFRLR
FBFBFBBLRR
FFFBFBBRRL
FBFBFFFLLR
BFFBBFFLRR
FFBFFBBLRL
FFFFBFBRLL
BFBBBFFRRR
BFBFFFFRRR
FBFBBFBRRL
BFBBFFFLRR
BFBBFFBLRR
BFBFFFFLRR
FBFBFFFLLL
FFFBBBBRRR
FBBBBFFLRL
FBFBFFBLLL
BBFBFFBLRL
FFBFFBBRRL
BBFFFFBRRL
FBFFBBBLRR
FBFBFFFRLL
BFBBBFFLLL
FBBBFFBRRL
BBFFBFFLLR
FBFFFFFRRL
BFFBFFBRLR
BFBFBBFLRR
FFBFFFBLRL
FFBFBBBLLR
FFFBBBBLLR
FFBBFBFRRL
FFBFFFFRLR
FFBFFFBRRR
FBBFFBFLRR
BBFBFFFLRR
FFBFBFBLLL
BFBBFFFRRR
FBBBFFFLLR
FBFFBFFLRR
BBFFFFBLLR
FBFFFBFLRL
FFFBBFBLRR
FBBBBFBLRL
FFFFFFBRRR
BFBBFBFRLR
FFFBFBFRRL
FFBBFFFLRL
FFFFBBBLLL
FBBFBFFRRR
BFFBFBFLLL
BFFFFFFRLL
BFBBBBBRLR
FBBBFBFLRR
BFBBBFFLLR
BFBBBBBRRL
FFBBBFFLLL
BFBFBFFLLR
FBFBFBFRLR
FBBFBBFRRR
BFFBBFFRRR
FFFFFFBRLR
FBBFBFBLRL
FFBFFBFRRR
FFBFFFBLLL
FBBFBBBRLR
BFBFBBBRLR
BBFBFFBLRR
FBFFBFBRRL
FBFBFBBLRL
FFBBBFBRLR
BFBFFBBRRL
FFBBFFBRRL
FBFFFFFRLL
BFBBBBFRLL
BBFFFFBLRR
FBBBFBFRRL
FBFBFFBRLR
FFFFBFBRRR
FBFFBBFLRR
BFFFBFBRLR
BFBBFBFRLL
FBBBFFFRRR
FFBFBBFRRL
FBBBFFFLLL
FBBFBFBLLR
FFFFBFFRRR
FFFFBBFLLL
BFFBFBFRLL
FFBFBFBLLR
BFFBFFFRRR
BBFBFFFLLL
FBFFFFFLLL
FFFBBBBRLL
FFBBFBBLLR
FBFFFFBLLL
BFBBBBFLLR
FFFBBFBRRR
BBFBFBFLLL
BFBBFFFRRL
BFBFFBBLRL
FBFBBFFRRL
FFFBBBBRLR
FBFFFFBLLR
FFFBBBFLLL
BFBBFFBRLR
FFBFBBFLLR
BBFBFFBRLL
FBFBBFBLLR
BFBFFFBLRL
FFFFBBFLRL
BBFFFBFRLL
FBBBFFBRLL
BFFFBFFRRL
BFBFBBFRRL
FBFBFBBRLR
FFFFFBBRLL
BFBFFFBRRL
BFFFFBBRLR
FBFFBBBRLL
FFBFFBBRLR
BFFBFBBRRR
BBFFFBFLRL
FBFFFBFLLR
FBBFFFFRLR
BFFFBFBLRL
FFBFBBFLLL
BFFFFFBLLR
FFBBFBBRRL
FBFBBBBLLR
BFFBBFBRLL
BBFFBBFLLL
FFBFFBBRLL
FFBBBFBLLR
BBFBFBFLRL
BFFFBBBLRL
FBBFBBBLRL
FBBFBFFRRL
BFBFFBBRLL
FFBBBBBLRL
FFBBBBFLLL
BFBBBFBLRR
FFFBFBFRRR
BFBBBBBLLR
FFBBFFBLLL
BFBBBBFLLL
FBBBFBFRLR
FFBFFFFLLR
BBFFBBBRRL
BFFBBFFRLL
BFFBBBBLRL
BFBFBFFRRR
FFBFBBFRLR
BBFFBBFRLR
BFFFBBBLLR
BFBFFBFRRL
FFFFFBFLLL
FBFFBBBRRL
BFBFBBFLLL
BFFFFFBLRL
FBBBFBBLLL
FFBBFFBRRR
FFFBBFFLLR
BFBFFBFLRL
FFBFFFBRLR
FBFFFBFRLL
BFFFFFFLLR
BFFBBBFRRR
FFBFBFFRLR
BBFFBFBRLL
FFFBFBFRLL
BBFFFBFRLR
BFFBFFBLLL
FFBFBBFRRR
BFBFFBFRLL
FBBBBFFRLR
FFBFBFBRLL
BFFBFBBLLR
FBFFBFFRLL
FFBFBBBRRL
FBFBBFBLRR
FBBFFBFRRR
FFBFBFFRRR
BBFFFFFLRL
FBBBFFBLLR
FBFBFBFRLL
BBFFFFFRLR
FBBBBFBRRR
BBFFFFFRRR
FFFBFFFLLR
BFBFBBBLRL
FBFBBBBLRR
BBFFFBFLLR
BFBBFBBLRL
BFFBFBFRLR
BFFBBFBRRL
BFFBFFBRLL
FFBFFFBRLL
FFBBFFFRLL
FBFBFFFLRL
FBBFBBBLLL
BFFBFFFLLL
FBFFFFFLRR
BFBFBBBRLL
FBFFBBBLLL
FFFBBFFRLL
FFBFFFFRRR
FFBBBBFLRL
FFBFFBFRLL
FFBBFFFRRR
BFBBBBBLLL
FFFBBFFLLL
BFBBBFFRLR
FBFFBBBLRL
BFBBFFBLRL
FBBFBFFLLL
FFFBFFFLLL
FBBBFBBRRL
FFFBFBFLRR
BFBBFFBLLR
FFBFBFBRRR
BFBFBBBLLL
FBFBFBBRRL
BFFFBBBRLL
FBFBFFBRLL
FBFFBBFRRL
BFFFBBBRRR
FFFFBFFRLR
BFBBFBFRRR
BFBBBBBRLL
FBBBFBBRLR
FFBFFFBLRR
BBFFFFFLLL
FFBFBFFLRL
BFBFFBFRRR
BBFFBBFRLL
FFBBBFBLLL
BFFFFFBLRR
FBBBBBBLLL
BFFBFFFLLR
FFBFBFFLRR
BFBBBBBLRR
FBBFBFBRLL
BFBBBBFRRR
BBFFFFBLLL
BFFBFFBLLR
FBFBFBBLLR
BFFFFFBRRR
FBBFBFFRLR
FBFFBBFLRL
FBFFBBBLLR
FFBBFFBRLR
FFBFFFFLRL
FBBBFBBRRR
FFBFBBBRLL
BFBFFFBLLR
BFBFFBFLLL
FFFBBFFRRL
FBBFFBBRRR
FFFFBBBLLR
BFBFFFBRLL
BFBFFFFLLL
BFFBFFFRRL
FBBFFBFLLR
FBFFBBBRRR
FFFFBFBRRL
BFFFFBFLLR
FFFBFFFLRR
BFBBFBFRRL
FFFFBFBLLR
FBBFBFBLRR
FFFBBBFRRR
FFFBBBBLRL
FBFFFFBRRL
BFBBFFBRRR
FFBFFFFLRR
FFBBFFFRLR
BFBFFFBLRR
FFBBFBFLLR
FFBBFFFLLL
BFFFBFBRRL
FFBBBFFRLR
FBFBFBFRRR
FFFFFBBLLL
BBFFBBFLLR
FBFBFBFLRR
BBFFFFFRRL
BFBBFBBLRR
FBBBBBFLRR
BFFBBFFLRL
BBFBFFFRRL
FBFFBFFRLR
FBFBFFBLRR
FBBBFBFLRL
FFFBBBBLRR
BBFFFBBRRR
FFBBBBFLRR
BBFFBBBRRR
FBFBFBFLRL
BBFFBBBLRL
BFBBFBBRLR
FBBBFBFLLL
BFFBFBBLRL
BFFFFFFRRR
BFFBBBFLLL
FFBFBBFLRR
FFFBFFBRLL
FBBFFFBLLR
FFBBBFFLRL
BFBFBFBLRL
BFBFFFBLLL
FFBBBFFRRL
BBFFBBBRLR
BFBFFFFLLR
BFFFBBBRRL
BBFFBFBRLR
BFFFBFBLLL
BFFFBFFLLL
BFBFFBFLRR
BFFBBFBRLR
BBFFBBFRRL
BFBBFBBRLL
FFBBBBBRRR
BFBBBFBRRR
FBFFBBFRRR
BBFFBFBLLL
BFFFFBBRRR
FBBFBBBRRL
BFFBBBFLLR
BFBFBFBRRL
FFBBFFFRRL
BFFBBFFLLL
FBBBBFFRRR
BBFFFBFLRR
BBFFFFFLRR
FBFFFBBLLL
FBBBFFFRLR
FBBBFFFLRL
BFFBBBFLRL
FFBFBBBRLR
FFBFFBFLRL
FBFBFBFLLL
FBBBBFFLLR
BFFFFFFLLL
FFFBBBFLRR
FBBBFBBLRL
FBBBBFBRLL
BFBBBFFLRL
BBFFBFFRLL
BBFFFFFLLR
FBBFBFBRRR
FBFBBFFRRR
BFFBBBFRLL
BFFFFBFRLR
FFBFBFBLRL
FFFFBBFRRL
FFFFFFBRRL
FFFBFFBLRL
BFFBBBBRLL
FBFBBFBLRL
BBFFFBBRLL
FBFFBFBRLL
FFBBBBBRLL
FFBFBBFLRL
FFFFFBBRLR
FFBBFBFLLL
FFFFFFBLRR
BBFFFBFRRR
FBBFFFBRLL
FFFFBBBLRL
BFFFFBFLRR
BBFBFBFLLR
BFFFFBFRRL
BFBBFFFLLL
FBFFBFBRRR
BFFFBBFRLL
BFFFFBBLRL
FFFBBBFRRL
FBFFFBFRRR
FFBBBFFRLL
BFBFFBBLLL
BFBFBBBRRL
BFFFFBFLRL
FBBFBBBRRR
FBBFBBFLRL
FBBBFBBLRR
FBBBFFBRRR
BBFFBFBLRR
FFBBBFFLLR
BFBFBFFLLL
FFBBFFBLLR
FBFBBFFRLL
FBBFFBFLRL
FFBFBFBLRR
FFFBBFBLLR
FFBBFFBLRL
BFBBBBBRRR
BFBFBBFRLL
FFBBFFFLLR
FFBBFFBRLL
FFFBBBFRLR
BFFFBFFLRR
BFFBFBBRLR
BBFFBBBLLL
FBFBFFBLLR
FFFBBFFRRR
BBFBFFFLLR
FBBFBFFRLL
FFBBFBBRLL
FBBBFBFRLL
BFBBFBBRRL
BFBFFFFRLL
BFFFBBBLRR
FFBBBBBLRR
BBFFFBBRLR
BFFBBBFRRL
BBFFBFBLRL
BFFBBBBRRL
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

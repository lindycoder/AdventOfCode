from dataclasses import dataclass
from functools import reduce, partial
from itertools import batched, count
from typing import Sequence, Iterable, Generator

import sys
from pathlib import Path
from textwrap import dedent

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    almanac = parse_almanac(data)

    location_mapper = partial(map_value, almanac.mappers)
    locations = map(location_mapper, almanac.seeds)
    lowest = min(locations)
    return lowest


def compute2(data: str) -> int | str:
    almanac = parse_almanac(data)

    # Get from location instead of from seed

    valid_seed_ranges = list(seed_ranges(almanac.seeds))

    reversed_mappers = [
        RangeMapper(
            ranges=frozenset({MapRange(r.dest, r.src, r.length) for r in mapper.ranges})
        )
        for mapper in reversed(almanac.mappers)
    ]
    seed_from_location = partial(map_value, reversed_mappers)

    for location in count():
        final_seed = seed_from_location(location)
        if any(final_seed in rng for rng in valid_seed_ranges):
            return location


@dataclass(frozen=True)
class MapRange:
    src: int
    dest: int
    length: int

    def __contains__(self, item):
        return self.src <= item < self.src + self.length


@dataclass(frozen=True)
class RangeMapper:
    ranges: frozenset[MapRange]

    def __getitem__(self, item: int) -> int:
        for range in self.ranges:
            if item in range:
                return range.dest + item - range.src
        return item


@dataclass(frozen=True)
class Almanac:
    seeds: Sequence[int]
    mappers: Sequence[RangeMapper]


def map_value(mappers: Sequence[RangeMapper], value: int) -> int:
    return reduce(lambda current, mapper: mapper[current], mappers, value)


def seed_ranges(seeds: Sequence[int]) -> Generator[MapRange, None, None]:
    for start, length in batched(seeds, n=2):
        yield MapRange(start, start, length)


def parse_almanac(raw: str) -> Almanac:
    lines = raw.strip().splitlines()
    seeds = map(int, lines[0].removeprefix("seeds: ").split(" "))

    all_mappers = []
    current_ranges = []
    for line in lines[3:]:
        if line == "":
            continue

        if line.endswith("map:"):
            all_mappers.append(RangeMapper(ranges=frozenset(current_ranges)))
            current_ranges = []
        else:
            dest, src, len = map(int, line.split(" "))
            current_ranges.append(MapRange(src, dest, len))

    all_mappers.append(RangeMapper(ranges=frozenset(current_ranges)))

    return Almanac(seeds=list(seeds), mappers=all_mappers)


def test_map_value():
    mappers = [
        RangeMapper(frozenset({MapRange(10, 20, 5)})),
        RangeMapper(frozenset({MapRange(20, 30, 5)})),
    ]

    assert_that(map_value(mappers, 12), is_(32))


def test_seed_ranges():
    seeds = [1, 3, 10, 2]

    assert_that(list(seed_ranges(seeds)), is_([MapRange(1, 1, 3), MapRange(10, 10, 2)]))


@pytest.mark.parametrize(
    ("mapper", "val", "expected"),
    [
        (RangeMapper(ranges=frozenset()), 123, 123),
        (RangeMapper(ranges=frozenset({MapRange(10, 20, 2)})), 9, 9),
        (RangeMapper(ranges=frozenset({MapRange(10, 20, 2)})), 10, 20),
        (RangeMapper(ranges=frozenset({MapRange(10, 20, 2)})), 11, 21),
        (RangeMapper(ranges=frozenset({MapRange(10, 20, 2)})), 12, 12),
        (
            RangeMapper(ranges=frozenset({MapRange(10, 20, 2), MapRange(30, 70, 5)})),
            29,
            29,
        ),
        (
            RangeMapper(ranges=frozenset({MapRange(10, 20, 2), MapRange(30, 70, 5)})),
            30,
            70,
        ),
        (
            RangeMapper(ranges=frozenset({MapRange(10, 20, 2), MapRange(30, 70, 5)})),
            36,
            36,
        ),
        (
            RangeMapper(ranges=frozenset({MapRange(10, 20, 2), MapRange(30, 70, 5)})),
            11,
            21,
        ),
    ],
)
def test_range_mapper_matching(mapper: RangeMapper, val: int, expected: int) -> None:
    assert_that(mapper[val], is_(expected))


def test_parse_almanac():
    data = dedent(
        """\
        seeds: 79 14
        
        seed-to-soil map:
        50 98 2
        52 50 48
        
        soil-to-fertilizer map:
        0 15 37
        """
    )
    assert_that(
        parse_almanac(data),
        is_(
            Almanac(
                seeds=[79, 14],
                mappers=[
                    RangeMapper(frozenset({MapRange(98, 50, 2), MapRange(50, 52, 48)})),
                    RangeMapper(frozenset({MapRange(15, 0, 37)})),
                ],
            )
        ),
    )


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            dedent(
                """\
                seeds: 79 14 55 13
                
                seed-to-soil map:
                50 98 2
                52 50 48
                
                soil-to-fertilizer map:
                0 15 37
                37 52 2
                39 0 15
                
                fertilizer-to-water map:
                49 53 8
                0 11 42
                42 0 7
                57 7 4
                
                water-to-light map:
                88 18 7
                18 25 70
                
                light-to-temperature map:
                45 77 23
                81 45 19
                68 64 13
                
                temperature-to-humidity map:
                0 69 1
                1 0 69
                
                humidity-to-location map:
                60 56 37
                56 93 4
                """
            ),
            35,
        ),
    ],
)
def test_compute(val: str, expected: int | str):
    assert_that(compute(val), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            dedent(
                """\
                seeds: 79 14 55 13
                
                seed-to-soil map:
                50 98 2
                52 50 48
                
                soil-to-fertilizer map:
                0 15 37
                37 52 2
                39 0 15
                
                fertilizer-to-water map:
                49 53 8
                0 11 42
                42 0 7
                57 7 4
                
                water-to-light map:
                88 18 7
                18 25 70
                
                light-to-temperature map:
                45 77 23
                81 45 19
                68 64 13
                
                temperature-to-humidity map:
                0 69 1
                1 0 69
                
                humidity-to-location map:
                60 56 37
                56 93 4
                """
            ),
            46,
        )
    ],
)
def test_compute2(val: str, expected: int | str):
    assert_that(compute2(val), is_(expected))


if __name__ == "__main__":
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

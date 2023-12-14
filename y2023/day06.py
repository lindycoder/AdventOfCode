import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from math import prod
from pathlib import Path
from textwrap import dedent
from typing import Generator

import pytest
from hamcrest import assert_that, is_, contains

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    races = parse(data)
    times = map(beating_times, races)
    return prod(times)


def compute2(data: str) -> int | str:
    race = parse_with_kerning(data)
    return beating_times(race)


@dataclass
class Race:
    time: int
    distance: int


NUM_RE = re.compile(r"\d+")


def parse(data: str) -> Generator[Race, None, None]:
    time_line, dist_line = map(lambda e: NUM_RE.findall(e), data.strip().splitlines())
    for time, dist in zip(time_line, dist_line, strict=True):
        yield Race(int(time), int(dist))


def parse_with_kerning(data: str) -> Race:
    time, dist = map(
        lambda e: e.split(":")[1].replace(" ", ""), data.strip().splitlines()
    )
    return Race(int(time), int(dist))


def launch(race_time: int, hold_time: int) -> int:
    if hold_time == 0:
        return 0

    return (race_time - hold_time) * hold_time


def beating_times(race: Race) -> int:
    first = 0
    for i in range(1, race.time):
        if launch(race.time, i) > race.distance:
            first = i
            break

    last = 0
    for i in range(race.time, 1, -1):
        if launch(race.time, i) > race.distance:
            last = i
            break

    return last - first + 1


def test_parse():
    data = dedent(
        """\
        Time:      7  15   30
        Distance:  9  40  200
        """
    )
    assert_that(
        list(parse(data)),
        is_(
            [
                Race(time=7, distance=9),
                Race(time=15, distance=40),
                Race(time=30, distance=200),
            ]
        ),
    )


def test_parse_with_kerning():
    data = dedent(
        """\
        Time:      7  15   30
        Distance:  9  40  200
        """
    )
    assert_that(
        parse_with_kerning(data),
        is_(
            Race(time=71530, distance=940200),
        ),
    )


@pytest.mark.parametrize(
    ("race_time", "hold_time", "expected_dist"),
    [
        (7, 0, 0),
        (7, 1, 6),
        (7, 2, 10),
        (7, 3, 12),
        (7, 4, 12),
        (7, 5, 10),
        (7, 6, 6),
        (7, 7, 0),
    ],
)
def test_launch(race_time: int, hold_time: int, expected_dist: int):
    assert_that(launch(race_time, hold_time), is_(expected_dist))


@pytest.mark.parametrize(
    ("race", "expected"),
    [
        (Race(7, 9), 4),
        (Race(15, 40), 8),
        (Race(30, 200), 9),
    ],
)
def test_beating_times(race: Race, expected: int):
    assert_that(beating_times(race), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            dedent(
                """\
                Time:      7  15   30
                Distance:  9  40  200
                """
            ),
            288,
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
                Time:      7  15   30
                Distance:  9  40  200
                """
            ),
            71503,
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

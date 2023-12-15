import sys
from collections.abc import Sequence
from pathlib import Path
from textwrap import dedent
from typing import Iterable

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    histories = map(parse, data.strip().splitlines())
    reductions = map(to_reductions, histories)
    return sum(map(extrapolate, reductions))


def compute2(data: str) -> int | str:
    histories = map(parse, data.strip().splitlines())
    reductions = map(to_reductions, histories)
    return sum(map(extrapolate_left, reductions))


def parse(raw: str) -> Sequence[int]:
    return list(map(int, raw.split(" ")))


def get_diffs(original: Iterable[int]) -> Sequence[int]:
    return [b - a for a, b in zip(original[:-1], original[1:], strict=True)]


def to_reductions(history: Sequence[int]) -> Sequence[Sequence[int]]:
    reductions = [history]
    while not all(e == 0 for e in reductions[-1]):
        reductions.append(get_diffs(reductions[-1]))
    return reductions


def extrapolate(reduction: Sequence[Sequence[int]]) -> int:
    extrapolated = 0
    for previous_step in reversed(reduction[:-1]):
        extrapolated = previous_step[-1] + extrapolated
    return extrapolated


def extrapolate_left(reduction: Sequence[Sequence[int]]) -> int:
    extrapolated = 0
    for previous_step in reversed(reduction[:-1]):
        extrapolated = previous_step[0] - extrapolated
    return extrapolated


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        ("10 13 16", [10, 13, 16]),
        ("10 -10 -115", [10, -10, -115]),
    ],
)
def test_parse(val: str, expected: Sequence[int]):
    assert_that(parse(val), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        ([10, 13, 17], [3, 4]),
        ([10, -10, -115], [-20, -105]),
    ],
)
def test_get_diffs(val: Sequence[int], expected: Sequence[int]):
    assert_that(get_diffs(val), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            [10, 13, 16, 21, 30, 45],
            [
                [10, 13, 16, 21, 30, 45],
                [3, 3, 5, 9, 15],
                [0, 2, 4, 6],
                [2, 2, 2],
                [0, 0],
            ],
        ),
        (
            [10, -10, -30],
            [
                [10, -10, -30],
                [-20, -20],
                [0],
            ],
        ),
    ],
)
def test_to_reductions(val: Sequence[int], expected: Sequence[Sequence[int]]):
    assert_that(to_reductions(val), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            [
                [10, 13, 16, 21, 30, 45],
                [3, 3, 5, 9, 15],
                [0, 2, 4, 6],
                [2, 2, 2],
                [0, 0],
            ],
            68,
        ),
        (
            [
                [10, -10, -30],
                [-20, -20],
                [0],
            ],
            -50,
        ),
    ],
)
def test_extrapolate(val: Sequence[Sequence[int]], expected: int):
    assert_that(extrapolate(val), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            [
                [10, 13, 16, 21, 30, 45],
                [3, 3, 5, 9, 15],
                [0, 2, 4, 6],
                [2, 2, 2],
                [0, 0],
            ],
            5,
        ),
        (
            [
                [10, -10, -30],
                [-20, -20],
                [0],
            ],
            30,
        ),
    ],
)
def test_extrapolate_left(val: Sequence[Sequence[int]], expected: int):
    assert_that(extrapolate_left(val), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            dedent(
                """\
                0 3 6 9 12 15
                1 3 6 10 15 21
                10 13 16 21 30 45
                """
            ),
            114,
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
                0 3 6 9 12 15
                1 3 6 10 15 21
                10 13 16 21 30 45
                """
            ),
            2,
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

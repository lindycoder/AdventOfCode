import sys
from collections.abc import Sequence, Mapping
from pathlib import Path
from textwrap import dedent
from types import MappingProxyType

import pytest
from hamcrest import assert_that, is_

from lib.maps import Map
from lib.point import Point
from lib.rectangle import Rectangle

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()

_PIPE_ENDS = MappingProxyType(
    {
        "|": (Point(0, -1), Point(0, 1)),
        "-": (Point(-1, 0), Point(1, 0)),
        "L": (Point(0, -1), Point(1, 0)),
        "J": (Point(0, -1), Point(-1, 0)),
        "7": (Point(0, 1), Point(-1, 0)),
        "F": (Point(0, 1), Point(1, 0)),
    }
)


def compute(data: str) -> int | str:
    pipe_map = Map.from_input(data, features=["S", *_PIPE_ENDS.keys()])
    path = _get_loop(pipe_map)

    return int(len(path) / 2)




def compute2(data: str) -> int | str:
    pipe_map = Map.from_input(data, features=["S", *_PIPE_ENDS.keys()])
    path = _get_loop(pipe_map)

    main_loop = set(path)
    known = set(main_loop)

    for step in path[1:]:
        for neighbor in step.neighbors:
            if neighbor not in known:


    return 0


def _get_loop(pipe_map) -> Sequence[Point]:
    start = next(k for k, v in pipe_map.items() if v == "S")
    path = [start, get_any_connection(pipe_map, start)]
    while True:
        previous, current_end = path[-2:]
        end1, end2 = map(lambda e: current_end + e, _PIPE_ENDS[pipe_map[current_end]])
        if end1 == previous:
            next_pipe = end2
        else:
            next_pipe = end1

        if next_pipe == start:
            break
        else:
            path.append(next_pipe)
    return path


def get_any_connection(pipe_map: Map, start: Point) -> Point:
    for neighbor in start.neighbors:
        if pipe := pipe_map.get(neighbor):
            if any(neighbor + pipe_end == start for pipe_end in _PIPE_ENDS[pipe]):
                return neighbor


@pytest.mark.parametrize(
    ("features", "start", "expected"),
    [
        # Next is up
        ({Point(2, 1): "|"}, Point(2, 2), Point(2, 1)),
        ({Point(2, 1): "7"}, Point(2, 2), Point(2, 1)),
        ({Point(2, 1): "F"}, Point(2, 2), Point(2, 1)),
        # Next is right
        ({Point(3, 2): "-"}, Point(2, 2), Point(3, 2)),
        ({Point(3, 2): "7"}, Point(2, 2), Point(3, 2)),
        ({Point(3, 2): "J"}, Point(2, 2), Point(3, 2)),
        # Next is down
        ({Point(2, 3): "|"}, Point(2, 2), Point(2, 3)),
        ({Point(2, 3): "L"}, Point(2, 2), Point(2, 3)),
        ({Point(2, 3): "J"}, Point(2, 2), Point(2, 3)),
        # Next is left
        ({Point(1, 2): "-"}, Point(2, 2), Point(1, 2)),
        ({Point(1, 2): "L"}, Point(2, 2), Point(1, 2)),
        ({Point(1, 2): "F"}, Point(2, 2), Point(1, 2)),
    ],
)
def test_get_any_connection(
    features: Mapping[Point, str], start: Point, expected: Point
):
    pipe_map = Map(features=features, rect=Rectangle(0, 0, 0, 0))
    assert_that(get_any_connection(pipe_map, start), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            dedent(
                """\
                .....
                .S-7.
                .|.|.
                .L-J.
                .....
                """
            ),
            4,
        ),
        (
            dedent(
                """\
                -L|F7
                7S-7|
                L|7||
                -L-J|
                L|-JF
                """
            ),
            4,
        ),
        (
            dedent(
                """\
                ..F7.
                .FJ|.
                SJ.L7
                |F--J
                LJ...
                """
            ),
            8,
        ),
        (
            dedent(
                """\
                7-F7-
                .FJ|7
                SJLL7
                |F--J
                LJ.LJ
                """
            ),
            8,
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
                ...........
                .S-------7.
                .|F-----7|.
                .||.....||.
                .||.....||.
                .|L-7.F-J|.
                .|..|.|..|.
                .L--J.L--J.
                ...........
                """
            ),
            4,
        ),
        (
            dedent(
                """\
                ..........
                .S------7.
                .|F----7|.
                .||....||.
                .||....||.
                .|L-7F-J|.
                .|..||..|.
                .L--JL--J.
                ..........
                """
            ),
            4,
        ),
        (
            dedent(
                """\
                .F----7F7F7F7F-7....
                .|F--7||||||||FJ....
                .||.FJ||||||||L7....
                FJL7L7LJLJ||LJ.L-7..
                L--J.L7...LJS7F-7L7.
                ....F-J..F7FJ|L7L7L7
                ....L7.F7||L7|.L7L7|
                .....|FJLJ|FJ|F7|.LJ
                ....FJL-7.||.||||...
                ....L---J.LJ.LJLJ...
                """
            ),
            8,
        ),
        (
            dedent(
                """\
                FF7FSF7F7F7F7F7F---7
                L|LJ||||||||||||F--J
                FL-7LJLJ||||||LJL-77
                F--JF--7||LJLJ7F7FJ-
                L---JF-JLJ.||-FJLJJ7
                |F|F-JF---7F7-L7L|7|
                |FFJF7L7F-JF7|JL---7
                7-L-JL7||F7|L7F-7F7|
                L.L7LFJ|||||FJL7||LJ
                L7JLJL-JLJLJL--JLJ.L
                """
            ),
            10,
        ),
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

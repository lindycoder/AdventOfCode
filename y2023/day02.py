import re
import sys
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from functools import partial
from math import prod
from pathlib import Path
from textwrap import dedent
from typing import Sequence

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    lines = data.strip().splitlines()

    budget = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    is_valid = partial(game_within_budget, budget)

    games = (parse_game(line) for line in lines)
    valid_games = filter(is_valid, games)
    return sum(g.game_id for g in valid_games)


def compute2(data: str) -> int | str:
    lines = data.strip().splitlines()

    games = (parse_game(line) for line in lines)
    minimal_sets = map(get_minimal_cube_set, games)
    return sum(prod(cube_set.values()) for cube_set in minimal_sets)


type CubeSet = Mapping[str, int]


@dataclass
class Game:
    game_id: int
    sets: Sequence[CubeSet]


GAME_RE = re.compile(r"Game (\d+): (.*)")
DRAW_RE = re.compile(r"(\d+) (\w+)")


def parse_game(line: str) -> Game:
    match = GAME_RE.match(line)
    drawn = match.group(2).split(";")
    return Game(game_id=int(match.group(1)), sets=[_parse_draw(draw) for draw in drawn])


def _parse_draw(draw: str) -> CubeSet:
    return {color: int(n) for n, color in DRAW_RE.findall(draw)}


def game_within_budget(budget: CubeSet, game: Game) -> bool:
    for game_set in game.sets:
        if any(n > budget[color] for color, n in game_set.items()):
            return False

    return True


def get_minimal_cube_set(game: Game) -> CubeSet:
    draws = defaultdict(list)
    for game_set in game.sets:
        for color, n in game_set.items():
            draws[color].append(n)
    return {color: max(values) for color, values in draws.items()}


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
            Game(
                game_id=1,
                sets=[
                    {"blue": 3, "red": 4},
                    {"red": 1, "green": 2, "blue": 6},
                    {"green": 2},
                ],
            ),
        ),
        ("Game 100: 100 blue", Game(game_id=100, sets=[{"blue": 100}])),
    ],
)
def test_parse_game(val, expect):
    assert_that(parse_game(val), is_(expect))


@pytest.mark.parametrize(
    ("game", "budget", "is_valid"),
    [
        (
            Game(game_id=1, sets=[{"a": 1}]),
            {"a": 1},
            True,
        ),
        (
            Game(game_id=1, sets=[{"a": 2}]),
            {"a": 1},
            False,
        ),
        (
            Game(game_id=1, sets=[{"a": 1}, {"a": 2}]),
            {"a": 1},
            False,
        ),
        (
            Game(game_id=1, sets=[{"a": 1, "b": 2}, {"a": 1, "b": 2}]),
            {"a": 2, "b": 2},
            True,
        ),
        (
            Game(game_id=1, sets=[{"b": 2}, {"a": 2}]),
            {"a": 1, "b": 2},
            False,
        ),
    ],
)
def test_game_within_budget(game: Game, budget: CubeSet, is_valid: bool):
    assert_that(game_within_budget(budget, game), is_(is_valid))


@pytest.mark.parametrize(
    ("game", "expected"),
    [
        (
            Game(game_id=1, sets=[{"a": 1}]),
            {"a": 1},
        ),
        (
            Game(game_id=1, sets=[{"a": 2}]),
            {"a": 2},
        ),
        (
            Game(game_id=1, sets=[{"a": 1}, {"a": 2}]),
            {"a": 2},
        ),
        (
            Game(game_id=1, sets=[{"a": 1, "b": 2}, {"a": 1, "b": 2}]),
            {"a": 1, "b": 2},
        ),
        (
            Game(game_id=1, sets=[{"b": 2}, {"a": 2}]),
            {"a": 2, "b": 2},
        ),
    ],
)
def test_get_minimal_cube_set(game: Game, expected: CubeSet):
    assert_that(get_minimal_cube_set(game), is_(expected))


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            dedent(
                """\
                Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
                Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
                Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
                Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
                Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
                """
            ),
            8,
        ),
        (puzzle_input, 2449),
    ],
)
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            dedent(
                """\
                Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
                Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
                Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
                Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
                Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
                """
            ),
            2286,
        )
    ],
)
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


if __name__ == "__main__":
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

import re
import sys
from collections.abc import Generator, Iterator
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from textwrap import dedent
from types import MappingProxyType
from typing import Mapping, Iterable, Optional

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str, start: str = "AAA", finish: str = "ZZZ") -> int | str:
    instructions, network = parse(data)

    return next(find_goals(cycle(instructions), network, start, finish))


def compute2(data: str, start: str = "A", finish: str = "Z") -> int | str:
    instructions, network = parse(data)

    journey = instructions * 10000  # Longer boot, faster result
    journey_length = len(journey)
    compiled = compile_node_journeys(journey, network, finish)

    tracked_nodes = [n for n in network.keys() if n.endswith(start)]

    travelled = 0
    while True:
        current_journeys = [compiled[n] for n in tracked_nodes]
        if result := get_winning_step((n.seen_goals for n in current_journeys)):
            return travelled + result

        tracked_nodes = [n.ends_with for n in current_journeys]
        travelled += journey_length


_DIR = MappingProxyType({"L": 0, "R": 1})

NETWORK_LINE_RE = re.compile(r"(\w+) = \((\w+), (\w+)\)")


def parse(raw: str) -> [str, Mapping[str, tuple[str, str]]]:
    instructions, network = raw.strip().split("\n\n")

    return (
        [_DIR[e] for e in instructions],
        {node: (left, right) for node, left, right in NETWORK_LINE_RE.findall(network)},
    )


def find_goals(
    instructions: Iterable[int],
    network: Mapping[str, tuple[str, str]],
    start: str,
    goal_id: str = "Z",
) -> Generator[int, None, None]:
    node = start
    for i, direction in enumerate(instructions):
        node = network[node][direction]
        if node.endswith(goal_id):
            yield i + 1


@dataclass
class NodeJourney:
    ends_with: str
    seen_goals: frozenset[int]


def node_journey(
    instructions: Iterable[int],
    network: Mapping[str, tuple[str, str]],
    start: str,
    goal_id: str = "Z",
) -> NodeJourney:
    node = start
    seen_goals = set[int]()
    for i, direction in enumerate(instructions):
        node = network[node][direction]
        if node.endswith(goal_id):
            seen_goals.add(i + 1)

    return NodeJourney(ends_with=node, seen_goals=frozenset(seen_goals))


def compile_node_journeys(
    instructions: Iterable[int],
    network: Mapping[str, tuple[str, str]],
    goal_id: str = "Z",
) -> Mapping[str, NodeJourney]:
    return {
        node: node_journey(instructions, network, node, goal_id)
        for node in network.keys()
    }


def get_winning_step(
    seen_goals_list: Iterator[frozenset[int]],
) -> Optional[int]:
    final_set = next(seen_goals_list)
    for seen_goals in seen_goals_list:
        final_set &= seen_goals

    if not final_set:
        return None
    return sorted(final_set)[0]


def test_parse() -> None:
    data = dedent(
        """\
        LLR
        
        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        """
    )

    assert_that(
        parse(data), is_(([0, 0, 1], {"AAA": ("BBB", "BBB"), "BBB": ("AAA", "ZZZ")}))
    )


def test_find_goals() -> None:
    instructions = [1, 1, 1]
    network = {
        "AAA": ("XXX", "BBB"),
        "BBB": ("XXX", "BBZ"),
        "BBZ": ("XXX", "CCZ"),
        "CCZ": ("XXX", "DDZ"),
    }

    result = find_goals(
        instructions,
        network,
        start="AAA",
        goal_id="Z",
    )

    assert_that(list(result), is_([2, 3]))


def test_node_journey() -> None:
    instructions = [1, 1, 1]
    network = {
        "AAA": ("XXX", "BBB"),
        "BBB": ("XXX", "BBZ"),
        "BBZ": ("XXX", "CCZ"),
        "CCZ": ("XXX", "DDZ"),
    }

    result = node_journey(
        instructions,
        network,
        start="AAA",
        goal_id="Z",
    )

    assert_that(result, is_(NodeJourney(ends_with="CCZ", seen_goals=frozenset({2, 3}))))


def test_compile_goals_reached() -> None:
    instructions = [1, 1, 1]
    network = {
        "AAA": ("XXX", "BBB"),
        "BBB": ("XXX", "BBZ"),
        "BBZ": ("XXX", "CCZ"),
        "CCZ": ("XXX", "DDZ"),
        "DDZ": ("XXX", "AAA"),
    }

    result = compile_node_journeys(
        instructions,
        network,
        goal_id="Z",
    )

    assert_that(
        result,
        is_(
            {
                "AAA": NodeJourney(ends_with="CCZ", seen_goals=frozenset({2, 3})),
                "BBB": NodeJourney(ends_with="DDZ", seen_goals=frozenset({1, 2, 3})),
                "BBZ": NodeJourney(ends_with="AAA", seen_goals=frozenset({1, 2})),
                "CCZ": NodeJourney(ends_with="BBB", seen_goals=frozenset({1})),
                "DDZ": NodeJourney(ends_with="BBZ", seen_goals=frozenset({3})),
            }
        ),
    )


@pytest.mark.parametrize(
    ("seen_goals", "expected"),
    [
        ([frozenset({1, 2, 3}), frozenset({2, 3})], 2),
        ([frozenset({1, 2}), frozenset({3})], None),
        ([frozenset({}), frozenset({})], None),
    ],
)
def test_get_winning_step(
    seen_goals: Iterable[frozenset[int]], expected: Optional[int]
) -> None:
    result = get_winning_step(iter(seen_goals))
    assert_that(result, is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            dedent(
                """\
                RL
                
                AAA = (BBB, CCC)
                BBB = (DDD, EEE)
                CCC = (ZZZ, GGG)
                DDD = (DDD, DDD)
                EEE = (EEE, EEE)
                GGG = (GGG, GGG)
                ZZZ = (ZZZ, ZZZ)
                """
            ),
            2,
        ),
        (
            dedent(
                """\
                LLR
                
                AAA = (BBB, BBB)
                BBB = (AAA, ZZZ)
                ZZZ = (ZZZ, ZZZ)
                """
            ),
            6,
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
                LR
                
                11A = (11B, XXX)
                11B = (XXX, 11Z)
                11Z = (11B, XXX)
                22A = (22B, XXX)
                22B = (22C, 22C)
                22C = (22Z, 22Z)
                22Z = (22B, 22B)
                XXX = (XXX, XXX)
                """
            ),
            6,
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

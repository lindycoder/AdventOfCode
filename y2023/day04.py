import re
from collections import defaultdict

import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Iterable

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    cards = parse_cards(data)
    points = map(calculate_points, cards)
    return sum(points)


def compute2(data: str) -> int | str:
    cards = parse_cards(data)

    total_cards = 0
    copies = defaultdict(lambda: 0)

    for card in cards:
        card_count = 1 + copies[card.card_id]
        total_cards += card_count

        points = calculate_matching_numbers(card)
        for offset in range(points):
            copies[card.card_id + offset + 1] += card_count

    return total_cards


@dataclass(frozen=True)
class Card:
    card_id: int
    winning: frozenset[int]
    numbers: Sequence[int]


CARD_RE = re.compile(r"Card \s*(\d+): ([\s\d]+) \| ([\s\d]+)")


def parse_cards(raw: str) -> Iterable[Card]:
    for card_id, winning, numbers in CARD_RE.findall(raw):
        yield Card(
            card_id=int(card_id),
            winning=frozenset(_parse_numbers(winning)),
            numbers=list(_parse_numbers(numbers)),
        )


def _parse_numbers(raw: str) -> Iterable[int]:
    return map(int, filter(lambda e: len(e) > 0, raw.strip().split(" ")))


def calculate_matching_numbers(card: Card) -> int:
    return len(set(card.numbers) & card.winning)


def calculate_points(card: Card) -> int:
    matching = calculate_matching_numbers(card)
    return 0 if not matching else 2 ** (matching - 1)


def test_parse_card():
    raw = dedent(
        """\
        Card   1:  1 48  2 86  3 | 83 86  6 31 17  9 48 53
        Card 101:  5  6 |  1  2
    """
    )
    assert_that(
        list(parse_cards(raw)),
        is_(
            [
                Card(
                    card_id=1,
                    winning=frozenset({1, 48, 2, 86, 3}),
                    numbers=[83, 86, 6, 31, 17, 9, 48, 53],
                ),
                Card(
                    card_id=101,
                    winning=frozenset({5, 6}),
                    numbers=[1, 2],
                ),
            ]
        ),
    )


@pytest.mark.parametrize(
    ("card", "expected"),
    [
        (Card(card_id=1, winning=frozenset({1}), numbers=[]), 0),
        (Card(card_id=1, winning=frozenset({1}), numbers=[1]), 1),
        (Card(card_id=1, winning=frozenset({1, 2}), numbers=[1, 2]), 2),
        (Card(card_id=1, winning=frozenset({1, 2, 3}), numbers=[1, 2, 3]), 3),
        (Card(card_id=1, winning=frozenset({1, 2, 3, 4}), numbers=[1, 2, 3, 4]), 4),
        (Card(card_id=1, winning=frozenset({1, 2}), numbers=[3, 1, 4, 2, 5]), 2),
    ],
)
def test_calculate_matching_numbers(card: Card, expected: int):
    assert_that(calculate_matching_numbers(card), is_(expected))


@pytest.mark.parametrize(
    ("card", "expected"),
    [
        (Card(card_id=1, winning=frozenset({1}), numbers=[]), 0),
        (Card(card_id=1, winning=frozenset({1}), numbers=[1]), 1),
        (Card(card_id=1, winning=frozenset({1, 2}), numbers=[1, 2]), 2),
        (Card(card_id=1, winning=frozenset({1, 2, 3}), numbers=[1, 2, 3]), 4),
        (Card(card_id=1, winning=frozenset({1, 2, 3, 4}), numbers=[1, 2, 3, 4]), 8),
        (Card(card_id=1, winning=frozenset({1, 2}), numbers=[3, 1, 4, 2, 5]), 2),
    ],
)
def test_calculate_points(card: Card, expected: int):
    assert_that(calculate_points(card), is_(expected))


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            dedent(
                """\
                Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
                Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
                Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
                Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
                Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
                Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
                """
            ),
            13,
        ),
        (puzzle_input, 23847),
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
                Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
                Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
                Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
                Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
                Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
                Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
                """
            ),
            30,
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

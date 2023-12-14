import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    hands = map(parse_hand, data.strip().splitlines())
    by_strength = sorted(
        hands,
        key=lambda hand: (
            hand_strength_by_distribution(hand.cards),
            effective_value(hand.cards),
        ),
    )
    return sum((i + 1) * hand.bid for i, hand in enumerate(by_strength))


def compute2(data: str) -> int | str:
    hands = map(parse_hand, data.strip().splitlines())
    by_strength = sorted(
        hands,
        key=lambda hand: (
            hand_strength_by_distribution_with_joker(hand.cards),
            effective_value_with_joker(hand.cards),
        ),
    )
    return sum((i + 1) * hand.bid for i, hand in enumerate(by_strength))


@dataclass
class Hand:
    cards: str
    bid: int


def hand_strength_by_distribution(cards: str) -> int:
    card_counter = Counter(cards)
    return sum(10 ** c[1] for c in card_counter.most_common())


def hand_strength_by_distribution_with_joker(cards: str) -> int:
    card_counter = Counter(cards)
    wild_cards = card_counter["J"]
    top_cards = [c[1] for c in card_counter.most_common() if c[0] != "J"]
    if not top_cards:
        return 10**5  # All J

    return sum(10**c for c in [top_cards[0] + wild_cards, *top_cards[1:]])


_HEX_VALUES = {
    "A": "E",
    "K": "D",
    "Q": "C",
    "J": "B",
    "T": "A",
    "9": "9",
    "8": "8",
    "7": "7",
    "6": "6",
    "5": "5",
    "4": "4",
    "3": "3",
    "2": "2",
}


def effective_value(cards: str) -> int:
    return int("".join(map(lambda e: _HEX_VALUES[e], cards)), base=16)


_JOKER_HEX_VALUES = {
    "A": "D",
    "K": "C",
    "Q": "B",
    "T": "A",
    "9": "9",
    "8": "8",
    "7": "7",
    "6": "6",
    "5": "5",
    "4": "4",
    "3": "3",
    "2": "2",
    "J": "1",
}


def effective_value_with_joker(cards: str) -> int:
    return int("".join(map(lambda e: _JOKER_HEX_VALUES[e], cards)), base=16)


def parse_hand(raw: str) -> Hand:
    cards, bid = raw.split(" ")
    return Hand(cards, int(bid))


@pytest.mark.parametrize(
    ("cards", "expected"),
    [
        ("AAAAA", 100000),  # Five of a kind
        ("AA8AA", 10010),  # Four of a kind
        ("23332", 1100),  # Full house
        ("TTT98", 1020),  # Three of a kind
        ("23432", 210),  # Two pair
        ("A23A4", 130),  # One pair
        ("23456", 50),  # High card
    ],
)
def test_hand_strength_by_distribution(cards: str, expected: int) -> None:
    assert_that(hand_strength_by_distribution(cards), is_(expected))


@pytest.mark.parametrize(
    ("cards", "expected"),
    [
        ("AAAAA", 100000),  # Five of a kind
        ("AJJJJ", 100000),  # Five of a kind
        ("JJJJJ", 100000),  # Five of a kind
        ("AA8AA", 10010),  # Four of a kind
        ("QJJQ2", 10010),  # Four of a kind
        ("23332", 1100),  # Full house
        ("23J32", 1100),  # Full house
        ("TTT98", 1020),  # Three of a kind
        ("TT98J", 1020),  # Three of a kind
        ("23432", 210),  # Two pair
        ("A23A4", 130),  # One pair
        ("A23J4", 130),  # One pair
        ("23456", 50),  # High card
    ],
)
def test_hand_strength_by_distribution_with_joker(cards: str, expected: int) -> None:
    assert_that(hand_strength_by_distribution_with_joker(cards), is_(expected))


@pytest.mark.parametrize(
    ("cards", "expected"),
    [
        ("23456", 0x23456),
        ("789TJ", 0x789AB),
        ("QKA23", 0xCDE23),
    ],
)
def test_effective_value(cards: str, expected: int) -> None:
    assert_that(effective_value(cards), is_(expected))


@pytest.mark.parametrize(
    ("cards", "expected"),
    [
        ("23456", 0x23456),
        ("789TJ", 0x789A1),
        ("QKA23", 0xBCD23),
    ],
)
def test_effective_value_with_joker(cards: str, expected: int) -> None:
    assert_that(effective_value_with_joker(cards), is_(expected))


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("T55J5 684", Hand("T55J5", 684)),
        ("KK677 28", Hand("KK677", 28)),
    ],
)
def test_parse_hand(raw: str, expected: Hand):
    assert_that(parse_hand(raw), is_(expected))


@pytest.mark.parametrize(
    ("val", "expected"),
    [
        (
            dedent(
                """\
                32T3K 765
                T55J5 684
                KK677 28
                KTJJT 220
                QQQJA 483
                """
            ),
            6440,
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
                32T3K 765
                T55J5 684
                KK677 28
                KTJJT 220
                QQQJA 483
                """
            ),
            5905,
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

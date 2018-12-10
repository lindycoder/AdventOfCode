import re
import sys
import unittest
from dataclasses import dataclass
from itertools import cycle
from typing import Any

from hamcrest import assert_that, is_


def compute(data):
    player_count, turns = map(lambda e: int(e),
                              re.match("(\d+) players; last marble is worth (\d+) points", data).groups())

    scores = play(player_count, turns)

    return max(scores.values())


def compute2(data):
    player_count, turns = map(lambda e: int(e),
                              re.match("(\d+) players; last marble is worth (\d+) points", data).groups())

    scores = play(player_count, turns * 100)

    return max(scores.values())


def play(player_count, turns):
    circle = Circle().insert(0)

    marbles = iter(range(1, turns + 1))

    players = {i: 0 for i in range(1, player_count + 1)}

    for player in cycle(players.keys()):
        try:
            marble = next(marbles)
        except StopIteration:
            return players

        if marble % 23 == 0:
            print(marble / turns * 100, "%")
            players[player] += marble
            repeat(7, circle.turn_ccw)
            players[player] += circle.pop()
        else:
            repeat(2, circle.turn_cw)
            circle.insert(marble)

        # print(player, "--", list(iter(circle)))


def repeat(times, operation):
    for i in range(0, times):
        operation()


@dataclass
class Circle:
    current: "_Link" = None

    def insert(self, value):
        if self.current is None:
            self.current = Circle._Link(value)
            self.current.before = self.current
            self.current.after = self.current
        else:
            before = self.current.before
            after = self.current
            new = Circle._Link(value, before=before, after=after)
            before.after = new
            after.before = new

            self.current = new

        return self

    def pop(self):
        current = self.current

        current.before.after = current.after
        current.after.before = current.before

        self.current = current.after

        return current.value

    def turn_cw(self):
        self.current = self.current.after

    def turn_ccw(self):
        self.current = self.current.before

    def __iter__(self):
        start_at = self.current
        stop_at = self.current

        def iter():
            current = start_at
            while True:
                yield current.value
                current = current.after
                if current is stop_at:
                    return

        return iter()

    @dataclass
    class _Link:
        value: Any
        before: "Circle._Link" = None
        after: "Circle._Link" = None

        def __repr__(self):
            return f"({self.before.value}) -> ({self.value}) -> ({self.after.value})"


class CircleTest(unittest.TestCase):
    def test_inserts(self):
        circle = Circle().insert("a")
        assert_that(list(iter(circle)), is_(["a"]))

        circle.insert("b")
        circle.insert("c")
        circle.insert("d")

        assert_that(list(iter(circle)), is_(["d", "c", "b", "a"]))


class ProvidedTest(unittest.TestCase):
    def test_part_1_1(self):
        assert_that(compute("9 players; last marble is worth 25 points"), is_(32))

    def test_part_1_2(self):
        assert_that(compute("10 players; last marble is worth 1618 points"), is_(8317))

    def test_part_1_3(self):
        assert_that(compute("13 players; last marble is worth 7999 points"), is_(146373))

    def test_part_1_4(self):
        assert_that(compute("17 players; last marble is worth 1104 points"), is_(2764))

    def test_part_1_5(self):
        assert_that(compute("21 players; last marble is worth 6111 points"), is_(54718))

    def test_part_1_6(self):
        assert_that(compute("30 players; last marble is worth 5807 points"), is_(37305))


puzzle_input = "428 players; last marble is worth 70825 points"

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

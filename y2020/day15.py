import sys
from collections import defaultdict

import pytest
from hamcrest import assert_that, is_

from lib.profiling import reporting


def compute(data, turns=2020):
    return play_the_game(data, turns)[0]


def play_the_game(data, turns):
    numbers = list(map(int, data.strip().split(',')))
    i = 0
    last_called = defaultdict(lambda: [])
    for i, n in enumerate(numbers):
        last_called[n].insert(0, i + 1)
    last_turn_num = numbers[-1]

    for i in reporting(range(i + 2, turns + 1), every=10000):
        if len(last_called[last_turn_num]) == 1:
            last_turn_num = 0
        else:
            last_turn_num = last_called[last_turn_num][0] - \
                            last_called[last_turn_num][1]

        last_called[last_turn_num] = [i] + last_called[last_turn_num][:1]

    return last_turn_num, last_called


def compute2(data, turns=30000000):
    return play_the_game(data, turns)[0]


@pytest.mark.parametrize('val,expect', [
    ('0,3,6', 436),
    ('1,3,2', 1),
    ('2,1,3', 10),
    ('1,2,3', 27),
    ('2,3,1', 78),
    ('3,2,1', 438),
    ('3,1,2', 1836),
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ('0,3,6', 175594),
    ('1,3,2', 2578),
    ('2,1,3', 3544142),
    ('1,2,3', 261214),
    ('2,3,1', 6895259),
    ('3,2,1', 18),
    ('3,1,2', 362),])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = "16,11,15,0,1,7"

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

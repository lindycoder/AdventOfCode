import pytest
import sys
from hamcrest import assert_that, is_
from itertools import chain

from lib.circle import Circle
from lib.profiling import reporting


def compute(data, moves=100):
    circle = Circle.from_iterable(map(int, data))

    play_game(circle, moves)

    circle.seek(1)
    return ''.join(map(str, circle))[1:]


def play_game(circle, moves):
    all_elements = set(circle)
    lowest = min(all_elements)
    highest = max(all_elements)

    for _ in reporting(range(moves), every=10000):
        current = circle.current
        circle.turn_cw()
        pickup = [circle.pop() for _ in range(3)]

        dest = current - 1
        while dest in pickup or dest < lowest or dest > highest:
            if dest < lowest:
                dest = highest + 1
            dest -= 1

        circle.seek(dest)

        for e in reversed(pickup):
            circle.insert_after(e)

        circle.seek(current).turn_cw()


def compute2(data):
    numbers = list(map(int, data))
    circle = Circle.from_iterable(chain(numbers,
                                        range(max(numbers) + 1, 1000001)))

    play_game(circle, 10000000)

    circle.seek(1).turn_cw()
    n1 = circle.current
    circle.turn_cw()
    n2 = circle.current

    return n1 * n2


@pytest.mark.parametrize('val,moves,expect', [
    ("389125467", 10, '92658374'),
    ("389125467", 100, '67384529'),
])
def test_compute(val, moves, expect):
    assert_that(compute(val, moves=moves), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("389125467", 149245887792),
])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = "362981754"

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

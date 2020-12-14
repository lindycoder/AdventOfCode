import logging
import sys
from dataclasses import dataclass
from functools import reduce
from itertools import count
from operator import mul

import pytest
from hamcrest import assert_that, is_


def compute(data):
    number, buses = data.strip().splitlines()
    number = int(number)
    buses = list(map(int, filter(lambda e: e != 'x', buses.split(','))))

    next_buses = [
        ((number // bus + 1) * bus - number, bus)
        for bus in buses
    ]

    t, bus = sorted(next_buses)[0]
    return t * bus


@dataclass
class Bus:
    index: int
    number: int


def compute2(data):
    buses = []
    for i, bus_id in enumerate(data.strip().splitlines()[1].split(',')):
        if bus_id != 'x':
            buses.append(Bus(i, int(bus_id)))

    first_bus = buses[0]

    timestamp = 0
    interval = first_bus.number
    for bus in buses[1:]:
        time_diff = bus.index - first_bus.index
        timestamp, interval = matching_interval(
            start_at=timestamp,
            interval=interval,
            time_diff=time_diff,
            next_bus_index=bus.number,
        )

    return timestamp


def matching_interval(start_at, interval, time_diff, next_bus_index):
    first_match = None

    for i in count(1):
        timestamp = interval * i + start_at

        if (timestamp + time_diff) % next_bus_index == 0:
            if first_match is None:
                first_match = timestamp
            else:
                return first_match, timestamp - first_match


@pytest.mark.parametrize('val,expect', [
    ("""\
939
7,13,x,x,59,x,31,19
""", 295)
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("""\
0
7,13,x,x,59,x,31,19
""", 1068781),
    ("""\
0
17,x,13,19
""", 3417),
    ("""\
0
67,7,59,61
""", 754018),
    ("""\
0
67,x,7,59,61
""", 779210),
    ("""\
0
67,7,x,59,61
""", 1261476),
    ("""\
0
1789,37,47,1889
""", 1202161486),
    ("""\
1000299
41,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,971,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17,13,x,x,x,x,23,x,x,x,x,x,29,x,487,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19
""", 404517869995362),
])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = """\
1000299
41,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37,x,x,x,x,x,971,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17,13,x,x,x,x,23,x,x,x,x,x,29,x,487,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

import logging
import sys
from collections import Counter

import pytest
from hamcrest import assert_that, is_


def compute(data):
    s, e = tuple(map(int, data.split('-')))
    return sum(1 for i in range(s, e+1) if meets(i))


def compute2(data):
    s, e = tuple(map(int, data.split('-')))
    return sum(1 for i in range(s, e+1) if meets2(i))



def meets(v):
    v = str(v)
    c = Counter(v)
    if all(c[e] == 1 for e in c.elements()):
        logging.info(f'{v} has no double')
        return False

    if "".join(sorted(v)) != v:
        logging.info(f'{v} is decreasing')
        return False

    return True


def meets2(v):
    v = str(v)
    c = Counter(v)
    if not any(v == 2 for v in c.values()):
        logging.info(f'{v} has no double')
        return False

    if "".join(sorted(v)) != v:
        logging.info(f'{v} is decreasing')
        return False

    return True


@pytest.mark.parametrize('val,expect', [
(111111, True),
(223450, False),
(123789, False),
])
def test_v(val, expect):
    assert_that(meets(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
(112233, True),
(123444, False),
(111122, True),
])
def test_v2(val, expect):
    assert_that(meets2(val), is_(expect))


puzzle_input = "256310-732736"

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

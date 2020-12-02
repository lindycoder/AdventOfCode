import math
from collections import defaultdict, Counter
from functools import reduce
from itertools import groupby

import pytest
from hamcrest import assert_that, is_


def lcm(*numbers):
    occurences = defaultdict(lambda: 0)

    for n in numbers:
        if n <= 1:
            continue
        factors = prime_factors(n)
        c = Counter(
            {
                f: len(list(g))
                for f, g in groupby(sorted(factors))
            }
        )

        for number, count in c.items():
            occurences[number] = max(occurences[number], count)

    return reduce(
        lambda a, b: a * b,
        (pow(number, count)
        for number, count in occurences.items()),
        1
    )


def prime_factors(n):
    while n % 2 == 0:
        yield 2
        n = n / 2

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            yield i
            n = n / i

    if n > 2:
        yield n


@pytest.mark.parametrize('numbers,expected', [
    (list(range(1, 11)), 2520),
    (list(range(1, 9)), 840)
])
def test_lcm(numbers, expected):
    assert_that(lcm(*numbers), is_(expected))

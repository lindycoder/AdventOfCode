import logging
import sys
from dataclasses import dataclass
from typing import List, Callable, Mapping, Tuple

import pytest
from hamcrest import assert_that, is_

from y2019.intcode import Intcode


def compute(data, noun=12, verb=2):
    code = Intcode.from_input(data)
    code[1] = noun
    code[2] = verb

    code.run()
    return code[0]


def compute2(data):
    for noun in range(99):
        for verb in range(99):
            r = compute(data, noun, verb)
            logging.debug(f'testing {noun} {verb} == {r}')
            if r == 19690720:
                return 100 * noun + verb


@pytest.mark.parametrize('val,expect', [
    ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
     [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
])
def test_v(val, expect):
    ex = Intcode(val)
    ex.run()
    assert_that(ex.state, is_(expect))


puzzle_input = """1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,5,23,1,6,23,27,1,27,5,31,2,31,10,35,2,35,6,39,1,39,5,43,2,43,9,47,1,47,6,51,1,13,51,55,2,9,55,59,1,59,13,63,1,6,63,67,2,67,10,71,1,9,71,75,2,75,6,79,1,79,5,83,1,83,5,87,2,9,87,91,2,9,91,95,1,95,10,99,1,9,99,103,2,103,6,107,2,9,107,111,1,111,5,115,2,6,115,119,1,5,119,123,1,123,2,127,1,127,9,0,99,2,0,14,0"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

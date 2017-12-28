import unittest

import sys
from collections import defaultdict
from textwrap import dedent

from hamcrest import assert_that, is_

def run_state_machine(states, start):
    step = 0
    tape = defaultdict(lambda : 0)
    cursor = 0
    current_state = states[start]
    while True:
        step += 1

        new_val, move, next_state = current_state[tape[cursor]]

        tape[cursor] = new_val
        cursor += move
        current_state = states[next_state]

        yield tape



def compute(states, iterations=12208951):
    state_machine = run_state_machine(states, "A")

    tape = None
    for i in range(0, iterations):
        tape = next(state_machine)

    return sum(tape.values())


def compute2(data):
    return 0


class DayTest(unittest.TestCase):
    def test_example(self):
        input_raw = dedent("""\
            Begin in state A.
            Perform a diagnostic checksum after 6 steps.
            
            In state A:
              If the current value is 0:
                - Write the value 1.
                - Move one slot to the right.
                - Continue with state B.
              If the current value is 1:
                - Write the value 0.
                - Move one slot to the left.
                - Continue with state B.
            
            In state B:
              If the current value is 0:
                - Write the value 1.
                - Move one slot to the left.
                - Continue with state A.
              If the current value is 1:
                - Write the value 1.
                - Move one slot to the right.
                - Continue with state A.""")

        input = {
            "A": {
                0: (1, 1, "B"),
                1: (0, -1, "B"),
            },
            "B": {
                0: (1, -1, "A"),
                1: (1, 1, "A"),
            },
        }

        assert_that(compute(input, iterations=6), is_(3))


puzzle_input_raw = """\
Begin in state A.
Perform a diagnostic checksum after 12208951 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state E.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state C.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the right.
    - Continue with state A.

In state C:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state D.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the right.
    - Continue with state C.

In state D:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state E.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state F.

In state E:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state C.

In state F:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state E.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

puzzle_input = {
    "A": {
        0: (1, 1, "B"),
        1: (0, -1, "E"),
    },
    "B": {
        0: (1, -1, "C"),
        1: (0, 1, "A"),
    },
    "C": {
        0: (1, -1, "D"),
        1: (0, 1, "C"),
    },
    "D": {
        0: (1, -1, "E"),
        1: (0, -1, "F"),
    },
    "E": {
        0: (1, -1, "A"),
        1: (1, -1, "C"),
    },
    "F": {
        0: (1, -1, "E"),
        1: (1, 1, "A"),
    }
}
if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

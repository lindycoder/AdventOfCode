import unittest

from hamcrest import assert_that, is_

X = 0
Y = 1


def compute(input):
    pos = [0, 0]
    directions = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    facing = 0

    commands = [(m[0], int(m[1:])) for m in input.split(", ")]

    for command in commands:
        direction, length = command

        facing += 1 if direction == 'R' else -1
        if facing < 0:
            facing = len(directions) - 1
        if facing >= len(directions):
            facing = 0

        pos[X] += length * directions[facing][X]
        pos[Y] += length * directions[facing][Y]

    return abs(pos[X]) + abs(pos[Y])


class ComputeTest(unittest.TestCase):
    def test_1(self):
        result = compute("R2, L3")
        assert_that(result, is_(5))

    def test_2(self):
        result = compute("R2, R2, R2")
        assert_that(result, is_(2))

    def test_3(self):
        result = compute("R5, L5, R5, R3")
        assert_that(result, is_(12))


if __name__ == '__main__':
    print("Result is {}".format(compute("R4, R5, L5, L5, L3, R2, R1, R1, L5, R5, R2, L1, L3, L4, R3, L1, L1, R2, R3, R3, R1, L3, L5, R3, R1, L1, R1, R2, L1, L4, L5, R4, R2, L192, R5, L2, R53, R1, L5, R73, R5, L5, R186, L3, L2, R1, R3, L3, L3, R1, L4, L2, R3, L5, R4, R3, R1, L1, R5, R2, R1, R1, R1, R3, R2, L1, R5, R1, L5, R2, L2, L4, R3, L1, R4, L5, R4, R3, L5, L3, R4, R2, L5, L5, R2, R3, R5, R4, R2, R1, L1, L5, L2, L3, L4, L5, L4, L5, L1, R3, R4, R5, R3, L5, L4, L3, L1, L4, R2, R5, R5, R4, L2, L4, R3, R1, L2, R5, L5, R1, R1, L1, L5, L5, L2, L1, R5, R2, L4, L1, R4, R3, L3, R1, R5, L1, L4, R2, L3, R5, R3, R1, L3")))

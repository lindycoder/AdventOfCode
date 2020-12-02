import logging
import sys
from collections import defaultdict

import pytest
from hamcrest import assert_that, is_

from y2018 import Point, Directions, Rotations
from y2019.intcode import Intcode
from y2019.rectangle import Rectangle


def compute(data):
    logging.getLogger().setLevel(logging.INFO)
    painter = Intcode.from_input(data)

    hull_map = defaultdict(lambda : 0)
    position = Point(0, 0)
    direction = Directions.UP

    paint(painter, hull_map, position, direction)

    return len(hull_map.items())


def paint(painter, hull_map, position, direction):
    while True:
        logging.info(f'IN = {hull_map[position]}')
        painter.stdin.append(hull_map[position])
        painter.run()

        new_color = painter.stdout.pop(0)
        hull_map[position] = new_color

        rotation = painter.stdout.pop(0)
        direction = direction.turn(
            Rotations.CW if rotation == 1 else Rotations.CCW)
        position += direction.value

        logging.info(
            f'OUT = {new_color}/{rotation} p={position} d={direction}')

        if painter.is_halted:
            break


def compute2(data):
    logging.getLogger().setLevel(logging.INFO)
    painter = Intcode.from_input(data)

    hull_map = defaultdict(lambda: 1)
    position = Point(0, 0)
    direction = Directions.UP

    paint(painter, hull_map, position, direction)

    x_s = [p.x for p in hull_map.keys()]
    y_s = [p.y for p in hull_map.keys()]
    hull_rect = Rectangle(
        left=min(x_s),
        right=max(x_s),
        top=min(y_s),
        bottom=max(y_s),
    )

    out = []
    for y in range(hull_rect.top, hull_rect.bottom + 1):
        line = ''
        for x in range(hull_rect.left, hull_rect.right + 1):
            line += '#' if hull_map[Point(x, y)] == 1 else ' '
        out.append(line)

    return '\n' + '\n'.join(out)


def test_v():
    print(compute(puzzle_input))
    raise AssertionError

def test_v2():
    print(compute2(puzzle_input))
    raise AssertionError


puzzle_input = "3,8,1005,8,315,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,29,2,1006,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,55,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,76,1,101,17,10,1006,0,3,2,1005,2,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,110,1,107,8,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,135,1,108,19,10,2,7,14,10,2,104,10,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,170,1,1003,12,10,1006,0,98,1006,0,6,1006,0,59,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,205,1,4,18,10,1006,0,53,1006,0,47,1006,0,86,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,239,2,9,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,266,1006,0,8,1,109,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,294,101,1,9,9,1007,9,1035,10,1005,10,15,99,109,637,104,0,104,1,21102,936995730328,1,1,21102,1,332,0,1105,1,436,21102,1,937109070740,1,21101,0,343,0,1106,0,436,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,179410308187,1,21101,0,390,0,1105,1,436,21101,0,29195603035,1,21102,1,401,0,1106,0,436,3,10,104,0,104,0,3,10,104,0,104,0,21102,825016079204,1,1,21102,1,424,0,1105,1,436,21102,1,825544672020,1,21102,435,1,0,1106,0,436,99,109,2,21202,-1,1,1,21102,1,40,2,21102,467,1,3,21101,0,457,0,1105,1,500,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,462,463,478,4,0,1001,462,1,462,108,4,462,10,1006,10,494,1102,0,1,462,109,-2,2106,0,0,0,109,4,1202,-1,1,499,1207,-3,0,10,1006,10,517,21102,1,0,-3,22101,0,-3,1,22101,0,-2,2,21101,1,0,3,21101,0,536,0,1106,0,541,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,564,2207,-4,-2,10,1006,10,564,21202,-4,1,-4,1105,1,632,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,583,0,0,1106,0,541,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,602,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,624,21202,-1,1,1,21101,624,0,0,106,0,499,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0"

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

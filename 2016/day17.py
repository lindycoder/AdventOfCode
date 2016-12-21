import hashlib
import sys
import unittest

from hamcrest import assert_that, is_


def compute(input):
    passcode = Passcode(input)
    start = (1, 1, "")
    steps_to_do = [start]

    while steps_to_do:
        current_path = steps_to_do.pop(0)
        for step in passcode.doors(current_path):
            if (step[0], step[1]) == (4, 4):
                return step[2]

            steps_to_do.append(step)

def compute2(input):
    passcode = Passcode(input)
    start = (1, 1, "")
    steps_to_do = [start]
    longest_path = None

    while steps_to_do:
        current_path = steps_to_do.pop(0)
        for step in passcode.doors(current_path):
            if (step[0], step[1]) == (4, 4):
                if longest_path is None or len(step[2]) > len(longest_path[2]):
                    longest_path = step
            else:
                steps_to_do.append(step)

    return len(longest_path[2])

class Passcode(object):
    def __init__(self, code):
        self.code = code

    def doors(self, pos):
        possible_doors = [
            (pos[0], pos[1] - 1, "U", 0),
            (pos[0], pos[1] + 1, "D", 1),
            (pos[0] - 1, pos[1], "L", 2),
            (pos[0] + 1, pos[1], "R", 3)
        ]

        indicators = hashlib.md5(bytes(self.code + pos[2], "UTF-8")).hexdigest()[:4]

        return [(d[0], d[1], pos[2] + d[2]) for d in possible_doors
                if 1 <= d[0] <= 4 and 1 <= d[1] <= 4 and self._is_open(indicators[d[3]])]

    def _is_open(self, indicator):
        return int(indicator, 16) > 10


class OpenDoorsTest(unittest.TestCase):
    def test_open_doors(self):
        p = Passcode("hijkl")
        assert_that(p.doors((1, 1, "")), is_([(1, 2, "D")]))
        assert_that(p.doors((1, 2, "D")), is_([(1, 1, "DU"), (2, 2, "DR")]))
        assert_that(p.doors((1, 1, "DU")), is_([(2, 1, "DUR")]))
        assert_that(p.doors((2, 1, "DUR")), is_([]))


class ZComputeTest(unittest.TestCase):
    def test_official_a(self):
        assert_that(compute("ihgpwlah"), is_("DDRRRD"))
    def test_official_b(self):
        assert_that(compute("kglvqrro"), is_("DDUDRLRRUDRD"))
    def test_official_c(self):
        assert_that(compute("ulqzkmiv"), is_("DRURDRUDDLLDLUURRDULRLDUUDDDRR"))

    def test_official2_a(self):
        assert_that(compute2("ihgpwlah"), is_(370))
    def test_official2_b(self):
        assert_that(compute2("kglvqrro"), is_(492))
    def test_official2_c(self):
        assert_that(compute2("ulqzkmiv"), is_(830))


if __name__ == '__main__':
    puzzle_input = "awrkjxxr"

    if sys.argv[1] == "1":
        result = compute(puzzle_input)
    else:
        result = compute2(puzzle_input)

    print("Result is {}".format(result))

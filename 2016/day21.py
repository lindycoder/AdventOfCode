import sys
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_


def compute(initial, operations):
    ps = PasswordScrambler(initial)

    ps.apply(read_data(operations))

    return ps.password

def compute2(initial, operations):
    ps = PasswordScrambler(initial)

    ps.unapply(read_data(operations))

    return ps.password


class PasswordScrambler(object):
    def __init__(self, password):
        self.password = password

    def apply(self, operations):
        for operation in operations:
            getattr(self, operation[0])(*operation[1:])

    def unapply(self, operations):
        for operation in reversed(operations):
            getattr(self, "un" + operation[0])(*operation[1:])

    def swap_position(self, a, b):
        pos = sorted([a, b])
        self.move_position(pos[1], pos[0])
        self.move_position(pos[0] + 1, pos[1])

    def unswap_position(self, a, b):
        self.swap_position(b, a)

    def swap_letter(self, a, b):
        self.swap_position(self.password.index(a), self.password.index(b))

    def unswap_letter(self, a, b):
        self.swap_letter(b, a)

    def reverse_positions(self, a, b):
        self.password = self.password[0:a] + "".join(reversed(list(self.password[a:b+1]))) + self.password[b+1:]

    def unreverse_positions(self, a, b):
        self.reverse_positions(a, b)

    def rotate_left(self, amount):
        self._rotate(amount, 1)

    def unrotate_left(self, amount):
        self.rotate_right(amount)

    def rotate_right(self, amount):
        self._rotate(amount, -1)

    def unrotate_right(self, amount):
        self.rotate_left(amount)

    def move_position(self, a, b):
        pwd = list(self.password)
        pwd.insert(b, pwd.pop(a))
        self.password = "".join(pwd)

    def unmove_position(self, a, b):
        self.move_position(b, a)

    def rotate_based(self, target):
        index = self.password.index(target)
        self.rotate_right(1 + index + (1 if index >= 4 else 0))

    def unrotate_based(self, target):
        original_state = self.password
        rotated = 0
        while original_state != self.password or rotated == 0:
            self.password = original_state
            rotated += 1
            self.rotate_left(rotated)
            self.rotate_based(target)

        self.rotate_left(rotated)

    def _rotate(self, amount, direction):
        amount %= len(self.password)
        self.password = self.password[direction * amount:] + self.password[:direction * amount]


def read_data(input):
    result = []
    for line in input.strip().split("\n"):
        words = line.split()
        cmd = ["{}_{}".format(*words[0:2])]
        for word in words[2:]:
            try:
                cmd.append(int(word))
            except ValueError:
                if len(word) == 1:
                    cmd.append(word)
        result.append(tuple(cmd))

    return result


class PasswordScramblerTest(unittest.TestCase):
    def test_swap_position(self):
        ps = PasswordScrambler("abcde")
        ps.swap_position(4, 0)
        assert_that(ps.password, is_("ebcda"))

    def test_unswap_position(self):
        ps = PasswordScrambler("ebcda")
        ps.unswap_position(4, 0)
        assert_that(ps.password, is_("abcde"))

    def test_swap_letter(self):
        ps = PasswordScrambler("ebcda")
        ps.swap_letter("d", "b")
        assert_that(ps.password, is_("edcba"))

        ps = PasswordScrambler("ehagbdfc")
        ps.swap_letter("d", "c")
        assert_that(ps.password, is_("ehagbcfd"))

    def test_unswap_letter(self):
        ps = PasswordScrambler("edcba")
        ps.unswap_letter("d", "b")
        assert_that(ps.password, is_("ebcda"))

        ps = PasswordScrambler("ehagbcfd")
        ps.unswap_letter("d", "c")
        assert_that(ps.password, is_("ehagbdfc"))

    def test_reverse_positions(self):
        ps = PasswordScrambler("edcba")
        ps.reverse_positions(0, 5)
        assert_that(ps.password, is_("abcde"))

    def test_unreverse_positions(self):
        ps = PasswordScrambler("abcde")
        ps.unreverse_positions(0, 5)
        assert_that(ps.password, is_("edcba"))

    def test_rotate_left(self):
        ps = PasswordScrambler("abcde")
        ps.rotate_left(1)
        assert_that(ps.password, is_("bcdea"))

    def test_unrotate_left(self):
        ps = PasswordScrambler("bcdea")
        ps.unrotate_left(1)
        assert_that(ps.password, is_("abcde"))

    def test_rotate_right(self):
        ps = PasswordScrambler("abcde")
        ps.rotate_right(1)
        assert_that(ps.password, is_("eabcd"))

    def test_unrotate_right(self):
        ps = PasswordScrambler("eabcd")
        ps.unrotate_right(1)
        assert_that(ps.password, is_("abcde"))

    def test_move_position(self):
        ps = PasswordScrambler("bcdea")
        ps.move_position(1, 4)
        assert_that(ps.password, is_("bdeac"))

        ps = PasswordScrambler("bdeac")
        ps.move_position(3, 0)
        assert_that(ps.password, is_("abdec"))

    def test_unmove_position(self):
        ps = PasswordScrambler("bdeac")
        ps.unmove_position(1, 4)
        assert_that(ps.password, is_("bcdea"))

        ps = PasswordScrambler("abdec")
        ps.unmove_position(3, 0)
        assert_that(ps.password, is_("bdeac"))

    def test_rotate_based(self):
        ps = PasswordScrambler("abdec")
        ps.rotate_based('b')
        assert_that(ps.password, is_("ecabd"))

        ps = PasswordScrambler("ecabd")
        ps.rotate_based('d')
        assert_that(ps.password, is_("decab"))

    def _test_unrotate(self, input):
        ps = PasswordScrambler(input)
        ps.rotate_based('a')
        ps.unrotate_based('a')
        assert_that(ps.password, is_(input))

    def test_unrotate_based(self):
        ps = PasswordScrambler("ecabd")
        ps.unrotate_based('b')
        assert_that(ps.password, is_("abdec"))

        ps = PasswordScrambler("decab")
        ps.unrotate_based('d')
        assert_that(ps.password, is_("ecabd"))

        self._test_unrotate("abcdefgh")
        self._test_unrotate("habcdefg")
        self._test_unrotate("ghabcdef")
        self._test_unrotate("fghabcde")
        self._test_unrotate("efghabcd")
        self._test_unrotate("defghabc")
        self._test_unrotate("cdefghab")
        self._test_unrotate("bcdefgha")
        self._test_unrotate("abcdefgh")



class ReadTest(unittest.TestCase):
    def test_read(self):
        input = dedent("""
            swap position 4 with position 0
            swap letter d with letter b
            reverse positions 0 through 4
            rotate left 1 step
            rotate right 10 step
            move position 1 to position 4
            rotate based on position of letter d""")
        assert_that(read_data(input), is_([
            ("swap_position", 4, 0),
            ("swap_letter", 'd', 'b'),
            ("reverse_positions", 0, 4),
            ("rotate_left", 1),
            ("rotate_right", 10),
            ("move_position", 1, 4),
            ("rotate_based", 'd'),
        ]))


class ZComputeTest(unittest.TestCase):
    def test_official(self):
        input = dedent("""
            swap position 4 with position 0
            swap letter d with letter b
            reverse positions 0 through 4
            rotate left 1 step
            move position 1 to position 4
            move position 3 to position 0
            rotate based on position of letter b
            rotate based on position of letter d""")
        assert_that(compute("abcde", input), is_("decab"))

    def test_official2(self):
        input = dedent("""
            swap position 4 with position 0
            swap letter d with letter b
            reverse positions 0 through 4
            rotate left 1 step
            move position 1 to position 4
            move position 3 to position 0
            rotate based on position of letter b
            rotate based on position of letter d""")
        assert_that(compute2("decab", input), is_("abcde"))

    def test_official2_1(self):
        assert_that(compute2("aefgbcdh", puzzle_input), is_("abcdefgh"))


puzzle_input = dedent("""
    rotate based on position of letter a
    swap letter g with letter d
    move position 1 to position 5
    reverse positions 6 through 7
    move position 5 to position 4
    rotate based on position of letter b
    reverse positions 6 through 7
    swap letter h with letter f
    swap letter e with letter c
    reverse positions 0 through 7
    swap position 6 with position 4
    rotate based on position of letter e
    move position 2 to position 7
    swap position 6 with position 4
    rotate based on position of letter e
    reverse positions 2 through 3
    rotate right 2 steps
    swap position 7 with position 1
    move position 1 to position 2
    move position 4 to position 7
    move position 5 to position 0
    swap letter e with letter f
    move position 4 to position 7
    reverse positions 1 through 7
    rotate based on position of letter g
    move position 7 to position 4
    rotate right 6 steps
    rotate based on position of letter g
    reverse positions 0 through 5
    reverse positions 0 through 7
    swap letter c with letter f
    swap letter h with letter f
    rotate right 7 steps
    rotate based on position of letter g
    rotate based on position of letter c
    swap position 1 with position 4
    move position 7 to position 3
    reverse positions 2 through 6
    move position 7 to position 0
    move position 7 to position 1
    move position 6 to position 7
    rotate right 5 steps
    reverse positions 0 through 6
    move position 1 to position 4
    rotate left 3 steps
    swap letter d with letter c
    move position 4 to position 5
    rotate based on position of letter f
    rotate right 1 step
    move position 7 to position 6
    swap position 6 with position 0
    move position 6 to position 2
    rotate right 1 step
    swap position 1 with position 6
    move position 2 to position 6
    swap position 2 with position 1
    reverse positions 1 through 7
    move position 4 to position 1
    move position 7 to position 0
    swap position 6 with position 7
    rotate left 1 step
    reverse positions 0 through 4
    rotate based on position of letter c
    rotate based on position of letter b
    move position 2 to position 1
    rotate right 0 steps
    swap letter b with letter d
    swap letter f with letter c
    swap letter d with letter a
    swap position 7 with position 6
    rotate right 0 steps
    swap position 0 with position 3
    swap position 2 with position 5
    swap letter h with letter f
    reverse positions 2 through 3
    rotate based on position of letter c
    rotate left 2 steps
    move position 0 to position 5
    swap position 2 with position 3
    rotate right 1 step
    rotate left 2 steps
    move position 0 to position 4
    rotate based on position of letter c
    rotate based on position of letter g
    swap position 3 with position 0
    rotate right 3 steps
    reverse positions 0 through 2
    move position 1 to position 2
    swap letter e with letter c
    rotate right 7 steps
    move position 0 to position 7
    rotate left 2 steps
    reverse positions 0 through 4
    swap letter e with letter b
    reverse positions 2 through 7
    rotate right 5 steps
    swap position 2 with position 4
    swap letter d with letter g
    reverse positions 3 through 4
    reverse positions 4 through 5""")

if __name__ == '__main__':

    if sys.argv[1] == "1":
        result = compute("abcdefgh", puzzle_input)
    else:
        result = compute2("fbgdceah", puzzle_input)

    print("Result is {}".format(result))

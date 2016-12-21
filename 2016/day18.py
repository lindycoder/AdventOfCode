import hashlib
import sys
import unittest

from hamcrest import assert_that, is_

SAFE = "."
TRAP = "^"

def compute(input, rows):
    row = input
    total_safe = row.count(SAFE)
    for i in range(1, rows):
        row = craft_row(row)
        total_safe += row.count(SAFE)

    return total_safe


def craft_row(previous):
    return "".join(TRAP if is_trap(tiles(previous, i - 1, i + 1)) else SAFE
                   for i in range(0, len(previous)))


def is_trap(indicator):
    return indicator in [
        TRAP + TRAP + SAFE,
        SAFE + TRAP + TRAP,
        TRAP + SAFE + SAFE,
        SAFE + SAFE + TRAP
    ]


class IsTrapTest(unittest.TestCase):
    def test_is_trap_by_rule1(self):
        assert_that(is_trap(TRAP + TRAP + SAFE), is_(True))

    def test_is_trap_by_rule2(self):
        assert_that(is_trap(SAFE + TRAP + TRAP), is_(True))

    def test_is_trap_by_rule3(self):
        assert_that(is_trap(TRAP + SAFE + SAFE), is_(True))

    def test_is_trap_by_rule4(self):
        assert_that(is_trap(SAFE + SAFE + TRAP), is_(True))

    def test_is_safe(self):
        assert_that(is_trap(SAFE + SAFE + SAFE), is_(False))
        assert_that(is_trap(TRAP + TRAP + TRAP), is_(False))
        assert_that(is_trap(TRAP + SAFE + TRAP), is_(False))


def tiles(row, start, stop):
    row = SAFE + row + SAFE
    return row[start + 1:stop + 2]




class TilesTest(unittest.TestCase):
    def test_get_3_tiles_middle(self):
        assert_that(tiles(".^.", 0, 2), is_(".^."))
        assert_that(tiles("^.^.^", 1, 3), is_(".^."))
        
    def test_get_3_tiles_limits(self):
        assert_that(tiles(".^.", -1, 1), is_("..^"))
        assert_that(tiles(".^.", 1, 3), is_("^.."))


class RowCraftTest(unittest.TestCase):
    def test_row_craft(self):
        assert_that(craft_row("..^^."), is_(".^^^^"))

    def test_row_craft2(self):
        assert_that(craft_row(".^^^^"), is_("^^..^"))

    def test_row_craft3(self):
        assert_that(craft_row(".^^.^.^^^^"), is_("^^^...^..^"))

    def test_row_craft3a(self):
        assert_that(craft_row("^^^...^..^"), is_("^.^^.^.^^."))

    def test_row_craft4(self):
        assert_that(craft_row("^.^^.^.^^."), is_("..^^...^^^"))

    def test_row_craft5(self):
        assert_that(craft_row("..^^...^^^"), is_(".^^^^.^^.^"))

    def test_row_craft6(self):
        assert_that(craft_row(".^^^^.^^.^"), is_("^^..^.^^.."))

    def test_row_craft7(self):
        assert_that(craft_row("^^..^.^^.."), is_("^^^^..^^^."))

    def test_row_craft8(self):
        assert_that(craft_row("^^^^..^^^."), is_("^..^^^^.^^"))

    def test_row_craft9(self):
        assert_that(craft_row("^..^^^^.^^"), is_(".^^^..^.^^"))

    def test_row_craft10(self):
        assert_that(craft_row(".^^^..^.^^"), is_("^^.^^^..^^"))


class ZComputeTest(unittest.TestCase):
    def test_official(self):
        assert_that(compute(".^^.^.^^^^", rows=10), is_(38))



if __name__ == '__main__':
    puzzle_input = "^^.^..^.....^..^..^^...^^.^....^^^.^.^^....^.^^^...^^^^.^^^^.^..^^^^.^^.^.^.^.^.^^...^^..^^^..^.^^^^"

    if sys.argv[1] == "1":
        result = compute(puzzle_input, rows=40)
    else:
        result = compute(puzzle_input, rows=400000)

    print("Result is {}".format(result))

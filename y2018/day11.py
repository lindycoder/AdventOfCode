import sys
import unittest
from dataclasses import dataclass

from hamcrest import assert_that, is_


def compute(data):
    power_grid = PowerGrid(int(data))

    grid_size, pack_size = 300, 3

    coords, level = biggest_pack(power_grid, grid_size, pack_size)

    return ",".join(map(str, coords))


def biggest_pack(power_grid, grid_size, pack_size):
    cellpacks = {}

    for x in range(1, grid_size - pack_size + 2):
        for y in range(1, grid_size - pack_size + 2):
            levels = []
            for w in range(0, pack_size):
                for h in range(0, pack_size):
                    levels.append(power_grid[x + w, y + h])
            cellpacks[x, y] = sum(levels)

    return max(cellpacks.items(), key=lambda e: e[1])


def compute2(data):
    power_grid = PowerGrid(int(data))

    biggest_packs = {}
    for pack_size in range(5, 300 + 1):
        coords, level = biggest_pack(power_grid, 300, pack_size)

        print(f"Biggest pack of {pack_size} is {level}")
        biggest_packs[coords[0], coords[1], pack_size] = level

        specs, level = max(biggest_packs.items(), key=lambda e: e[1])
        print(f"max is {','.join(map(str, specs))} with {level}")


@dataclass
class PowerGrid(dict):
    serial: int
    size: int = 300

    def __post_init__(self):
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                self[x, y] = self.powerlevel(x, y)

    def powerlevel(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += self.serial
        power_level *= rack_id
        hundreds = int(power_level / 100) % 10
        return hundreds - 5


class PowerLevelTest(unittest.TestCase):
    def test_power_level_1(self):
        grid = PowerGrid(8)
        assert_that(grid[3, 5], is_(4))

    def test_power_level_2(self):
        grid = PowerGrid(57)
        assert_that(grid[122, 79], is_(-5))

    def test_power_level_3(self):
        grid = PowerGrid(39)
        assert_that(grid[217, 196], is_(0))

    def test_power_level_4(self):
        grid = PowerGrid(71)
        assert_that(grid[101, 153], is_(4))


class ProvidedTest(unittest.TestCase):
    def test_part_1_1(self):
        assert_that(compute(18), is_("33,45"))

    def test_part_1_2(self):
        assert_that(compute(42), is_("21,61"))


puzzle_input = "3628"

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

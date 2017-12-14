import sys
import unittest

from hamcrest import assert_that, is_

from y2017.day10 import knot_hash


def compute(data):
    return sum(sum(e) for e in disk_grid(data, grid_size=128))


def compute2(data):
    grid_size = 128
    grid = disk_grid(data, grid_size)

    group_count = 0
    part_of_a_group = []

    for y in range(0, grid_size):
        for x in range(0, grid_size):
            if grid[y][x] == 1 and (y, x) not in part_of_a_group:
                part_of_a_group.extend(crawl_group(grid, y, x, []))
                group_count += 1

    return group_count


DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def crawl_group(grid, y, x, so_far):
    size = len(grid)
    result = [(y, x)]
    for d in DIRECTIONS:
        ty = y + d[0]
        tx = x + d[1]
        if 0 <= ty < size and 0 <= tx < size:
            if (ty, tx) not in so_far and grid[ty][tx] == 1:
                result.extend(crawl_group(grid, ty, tx, result + so_far))

    return result


def top_neighbor(y, x):
    return y - 1, x


def left_neighbor(y, x):
    return y, x - 1


def disk_grid(data, grid_size):
    grid = []
    for i in range(0, grid_size):
        row_hash = knot_hash("{}-{}".format(data, i))
        grid.append(list(int(e) for e in hex_to_bin(row_hash)))
    return grid


def hex_to_bin(num):
    return bin(int(num, 16))[2:].zfill(len(num) * 4)


class DayTest(unittest.TestCase):
    def test_example(self):
        assert_that(compute("flqrgnkx"), is_(8108))

    def test_puzzle(self):
        assert_that(compute(puzzle_input), is_(8214))


class Day2Test(unittest.TestCase):
    def test_example(self):
        assert_that(compute2("flqrgnkx"), is_(1242))

        # def test_puzzle(self):
        #     assert_that(compute2(puzzle_input), is_(8214))


class HexToBinTest(unittest.TestCase):
    def test_1(self):
        assert_that(hex_to_bin("0"), is_("0000"))

    def test_2(self):
        assert_that(hex_to_bin("e"), is_("1110"))

    def test_3(self):
        assert_that(hex_to_bin("a0c2017"), is_("1010000011000010000000010111"))

    def test_4(self):
        assert_that(hex_to_bin("55"), is_("01010101"))


class CrawlTest(unittest.TestCase):
    def test_crawl_square(self):
        grid = [
            [1, 1],
            [1, 1]
        ]

        members = crawl_group(grid, 0, 0, [])

        assert_that((0, 0) in members)
        assert_that((0, 1) in members)
        assert_that((1, 0) in members)
        assert_that((1, 1) in members)


puzzle_input = "hxtvlmkl"

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

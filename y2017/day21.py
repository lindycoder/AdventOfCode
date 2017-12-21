import unittest

import sys
from textwrap import dedent

from hamcrest import assert_that, is_
from math import sqrt


def compute(data, iterations=5, start=".#...####"):
    enhancements = {}
    for pattern, enhancement in parse(data).items():
        for variation in variations(pattern):
            enhancements[variation] = enhancement

    matrix = start
    for i in range(0, iterations):
        parts = split(matrix)

        new_parts = [enhancements[p] for p in parts]

        matrix = join(new_parts)

    return matrix.count("#")


def compute2(data):
    return compute(data, iterations=18)


def split_size(pattern):
    if len(pattern) <= 9:
        return 1
    width = int(sqrt(len(pattern)))
    return int(((width - (width % 4)) / 2) ** 2)


def split(matrix):
    side = int(sqrt(len(matrix)))

    cell_size = 2 if side % 2 == 0 else 3

    parts = []
    for y in range(0, int(side / cell_size)):
        for x in range(0, int(side / cell_size)):
            cell_top_left = y * side * cell_size + x * cell_size
            parts.append("".join([matrix[cell_top_left + side * line:cell_top_left + side * line + cell_size]
                                  for line in range(0, cell_size)]))

    return parts


def join(parts):
    part_size = len(parts[0])

    side = int(sqrt(len(parts)))
    cell_size = int(sqrt(part_size))

    matrix = ""
    for y in range(0, side):
        lines = ["" for _ in range(0, cell_size)]
        for x in range(0, side):
            part = parts[y * side + x]
            for line in range(0, cell_size):
                lines[line] += part[line * cell_size:line * cell_size + cell_size]

        matrix += "".join(lines)

    return matrix


def parse(data):
    return {line.split(" => ")[0].replace("/", ""): line.split(" => ")[1].replace("/", "") for line in data.split("\n")}


def variations(pattern):
    size = 2 if len(pattern) == 4 else 3
    result = set()

    for _ in range(0, 2):
        result.add(pattern)
        result.add("".join(reversed(pattern)))
        flipped = flip(pattern, size)
        result.add(flipped)
        result.add("".join(reversed(flipped)))
        pattern = clockwise(pattern, size)

    return result


def clockwise(pattern, size):
    return "".join("".join(pattern[col * size + line] for col in range(size - 1, -1, -1)) for line in range(0, size))


def flip(pattern, size):
    return "".join("".join(reversed(pattern[l * size:(l + 1) * size])) for l in range(0, size))


class DayTest(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            ../.# => ##./#../...
            .#./..#/### => #..#/..../..../#..#""")
        assert_that(compute(input, iterations=2), is_(12))

    def test_puzzle(self):
        assert_that(compute(puzzle_input), is_(208))


class ParseTest(unittest.TestCase):
    def test(self):
        patterns = parse(dedent("""\
            ../.# => ##./#../...
            .#./..#/### => #..#/..../..../#..#"""))

        assert_that(patterns["...#"], is_("##.#....."))
        assert_that(patterns[".#...####"], is_("#..#........#..#"))


class VariationsTest(unittest.TestCase):
    def test_clockwise_2x2(self):
        assert_that(clockwise("...#", size=2), is_("..#."))

    def test_clockwise_3x3(self):
        assert_that(clockwise(".#...####", size=3), is_("#..#.###."))

    def test_flip_2x2(self):
        assert_that(flip("...#", size=2), is_("..#."))

    def test_flip_3x3(self):
        assert_that(flip(".#...####", size=3), is_(".#.#..###"))

    def test2x2(self):
        patterns = variations("...#")

        assert_that("...#" in patterns)
        assert_that("#..." in patterns)
        assert_that("..#." in patterns)
        assert_that(".#.." in patterns)

    def test3x3(self):
        patterns = variations(".#...####")

        assert_that(".#...####" in patterns)
        assert_that("####...#." in patterns)
        assert_that("#..#.###." in patterns)
        assert_that(".###.#..#" in patterns)
        assert_that(".#.#..###" in patterns)
        assert_that("###..#.#." in patterns)
        assert_that("##.#.##.." in patterns)
        assert_that("..##.#.##" in patterns)


class ChunkTest(unittest.TestCase):
    def test_split_size_2x2(self):
        assert_that(split_size("#..."), is_(1))

    def test_split_size_3x3(self):
        assert_that(split_size(".#...####"), is_(1))

    def test_split_size_4x4(self):
        assert_that(split_size("#..#........#..#"), is_(4))

    def test_split_size_6x6(self):
        assert_that(split_size("##.##.#..#........##.##.#..#........"), is_(4))

    def test_split_size_8x8(self):
        assert_that(split_size("#..##..#................#..##..##..##..#................#..##..#"), is_(16))

    def test_split_3x3(self):
        assert_that(split(".#...####"), is_([".#...####"]))

    def test_split_4x4(self):
        assert_that(split("#..#........#..#"),
                    is_(["#...", ".#..",
                         "..#.", "...#"]))

    def test_split_6x6(self):
        assert_that(split("##.##.#..#........##.##.#..#........"),
                    is_(["###.", ".#.#", "#...",
                         "..##", "...#", "..#.",
                         "#...", ".#..", "...."]))

    def test_split_8x8(self):
        assert_that(split("#..##..#................#..##..##..##..#................#..##..#"),
                    is_(["#...", ".#..", "#...", ".#..",
                         "..#.", "...#", "..#.", "...#",
                         "#...", ".#..", "#...", ".#..",
                         "..#.", "...#", "..#.", "...#"]))

    def test_join_3x3(self):
        pattern = ".#...####"
        assert_that(join(split(pattern)), is_(pattern))

    def test_join_4x4(self):
        pattern = "#..#........#..#"
        assert_that(join(split(pattern)), is_(pattern))

    def test_join_6x6(self):
        pattern = "##.##.#..#........##.##.#..#........"
        assert_that(join(split(pattern)), is_(pattern))

    def test_join_8x8(self):
        pattern = "#..##..#................#..##..##..##..#................#..##..#"
        assert_that(join(split(pattern)), is_(pattern))

    def test_join_4x4x4(self):
        parts = ["#..#........#..#", "#..#........#..#", "#..#........#..#", "#..#........#..#"]
        assert_that(join(parts), is_("#..##..#................#..##..##..##..#................#..##..#"))


#
# .#.      #
# ..#     #
# ###     ###
#
# #       ##
# # #     # #
# ##      #
#
# ###     ###
# #         #
#  #       #
#
#  ##       #
# # #     # #
#   #      ##
#



puzzle_input = """\
../.. => ###/###/.##
#./.. => ..#/###/##.
##/.. => ..#/##./##.
.#/#. => #../.#./.##
##/#. => #.#/###/.#.
##/## => ##./.../.#.
.../.../... => ...#/.#../#.#./##.#
#../.../... => .#.#/.#../####/###.
.#./.../... => #.##/#.##/.###/##.#
##./.../... => ..##/#.##/.##./..##
#.#/.../... => .#.#/#.#./#..#/...#
###/.../... => #.../.##./.#../.###
.#./#../... => ##.#/...#/##.#/.##.
##./#../... => #.#./###./...#/#.##
..#/#../... => ..##/.###/..../.##.
#.#/#../... => ...#/#..#/#.#./#.#.
.##/#../... => ...#/#.##/..##/.###
###/#../... => .##./..##/##../##.#
.../.#./... => ####/.##./##.#/####
#../.#./... => ..../.##./#..#/##.#
.#./.#./... => ..../#.##/#.../..#.
##./.#./... => .###/.#.#/...#/....
#.#/.#./... => ..##/.#../.###/#.##
###/.#./... => ..../..##/##.#/###.
.#./##./... => .###/.#.#/#..#/#.#.
##./##./... => #..#/#..#/#.##/.##.
..#/##./... => #.##/...#/..#./.##.
#.#/##./... => ..##/#.../..../...#
.##/##./... => ##.#/...#/..##/#..#
###/##./... => ..##/..#./.###/..##
.../#.#/... => .###/..##/.#.#/..##
#../#.#/... => ..##/...#/##../..#.
.#./#.#/... => ..##/##.#/#..#/###.
##./#.#/... => #.../####/..#./#...
#.#/#.#/... => ..../##.#/.##./#..#
###/#.#/... => ..##/#.#./.#.#/.#..
.../###/... => ..##/.#../.#.#/#..#
#../###/... => #.#./.#../.##./....
.#./###/... => ##.#/...#/###./#.##
##./###/... => ..../#.../.###/#.#.
#.#/###/... => ####/..../...#/....
###/###/... => ##.#/##../#.##/#...
..#/.../#.. => ##.#/..#./#.##/..#.
#.#/.../#.. => .#../...#/..#./.##.
.##/.../#.. => ...#/#.../#..#/#..#
###/.../#.. => .###/##../.##./.#..
.##/#../#.. => ..##/#.##/.#.#/...#
###/#../#.. => ...#/.###/..../#..#
..#/.#./#.. => #..#/..../..#./..##
#.#/.#./#.. => #..#/..../#.#./.###
.##/.#./#.. => ..../.##./..##/.#.#
###/.#./#.. => ##.#/###./##.#/..##
.##/##./#.. => #.#./..../###./####
###/##./#.. => #..#/#.##/#.##/#...
#../..#/#.. => ##../#..#/#.../###.
.#./..#/#.. => #.#./.#.#/..../.#.#
##./..#/#.. => #.#./#.../#.#./#..#
#.#/..#/#.. => ..##/.#.#/.#../.###
.##/..#/#.. => ##.#/..##/..../.###
###/..#/#.. => ..#./.##./...#/.#.#
#../#.#/#.. => #.../.#../#.#./##..
.#./#.#/#.. => ..../..../##../#...
##./#.#/#.. => ..#./..../#.../..#.
..#/#.#/#.. => #.#./.#.#/.#../#.##
#.#/#.#/#.. => ...#/##.#/.##./#...
.##/#.#/#.. => ..#./...#/.##./#...
###/#.#/#.. => ..##/#..#/..../..##
#../.##/#.. => ##.#/##.#/#.##/.#.#
.#./.##/#.. => ..##/##../#.#./####
##./.##/#.. => #.#./..../..##/#.##
#.#/.##/#.. => ..#./###./##.#/##.#
.##/.##/#.. => #..#/...#/..##/....
###/.##/#.. => ..##/##../##.#/#.##
#../###/#.. => ####/###./.###/....
.#./###/#.. => ...#/.##./...#/#.##
##./###/#.. => ...#/...#/##.#/.##.
..#/###/#.. => ..##/.##./#.#./...#
#.#/###/#.. => .###/.##./.###/.#.#
.##/###/#.. => ##../.#../#.#./##.#
###/###/#.. => ..../..../.###/##..
.#./#.#/.#. => ##.#/##.#/..##/.##.
##./#.#/.#. => .#../#.##/#.##/#.#.
#.#/#.#/.#. => ..##/#.#./#.../..##
###/#.#/.#. => ##.#/.#.#/##.#/.###
.#./###/.#. => #.#./..#./..##/.##.
##./###/.#. => ...#/#.##/###./#.##
#.#/###/.#. => ...#/.###/#.#./#.#.
###/###/.#. => .#.#/#..#/####/#...
#.#/..#/##. => #.##/#.#./##../####
###/..#/##. => ##.#/...#/..../####
.##/#.#/##. => #.../#..#/..##/....
###/#.#/##. => ##../###./...#/####
#.#/.##/##. => ##.#/..##/..../#...
###/.##/##. => ..#./####/..../#...
.##/###/##. => ..##/#.##/..#./####
###/###/##. => #.##/...#/..../..#.
#.#/.../#.# => ..#./#.##/#..#/#.#.
###/.../#.# => ..#./###./..##/#...
###/#../#.# => .###/#..#/##../.#..
#.#/.#./#.# => ###./##.#/.#../#..#
###/.#./#.# => ##.#/###./#.../...#
###/##./#.# => ####/##../#.../....
#.#/#.#/#.# => ..#./..##/..#./...#
###/#.#/#.# => ...#/##.#/##.#/#.##
#.#/###/#.# => ..#./####/.#../##.#
###/###/#.# => ..../.#.#/..../...#
###/#.#/### => #.#./..##/##.#/....
###/###/### => ..#./#.##/####/###."""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

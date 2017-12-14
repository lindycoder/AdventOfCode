import unittest

import sys
from hamcrest import assert_that, is_

U = 0
L = 1
D = 2
R = 3
X = 0
Y = 1


def compute(data):
    start = int(data)

    if start == 1:
        return 0

    layer = 0
    layer_start = 1
    layer_length = 1
    while start > layer_start + layer_length:
        layer += 1
        layer_start += layer_length
        layer_length = layer * 8

    return layer + ((start + 1 - layer_start) % layer)


def compute2(data):
    expected = int(data)
    g = empty_grid(10)

    crawler = spiral_crawl(middle(g))
    start = next(crawler)
    g[start[Y]][start[X]] = 1
    for index, pos in enumerate(crawler, start=1):
        val = around(g, pos)
        if val > expected:
            return val

        g[pos[Y]][pos[X]] = val


def show_grid(layers):
    g = empty_grid(layers)
    last_element = (layers * 2 - 1) ** 2 + 1

    for index, pos in enumerate(spiral_crawl(middle(g)), start=1):
        if index >= last_element:
            return g

        g[pos[Y]][pos[X]] = index


def empty_grid(layers):
    return [[None for _ in range(0, layers * 2 - 1)] for _ in range(0, layers * 2 - 1)]


def middle(grid):
    perimeter = int((len(grid) + 1) / 2)
    return [perimeter - 1, perimeter - 1]


def around(g, pos):
    return sum(g[pos[Y] + m[Y]][pos[X] + m[X]] or 0 for m in (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1)
    ))


def spiral_crawl(start):
    dir = R
    pos = start
    pos[X] -= 1

    size = 1
    done = 0
    i = 1
    while True:
        i += 1
        if dir == R:
            pos[X] += 1
        elif dir == U:
            pos[Y] -= 1
        elif dir == L:
            pos[X] -= 1
        elif dir == D:
            pos[Y] += 1

        yield tuple(pos)

        done += 1
        if done == size:
            if dir != R:
                dir += 1
                done = 0
        elif done > size:
            if size == 1:
                size = 2
            else:
                size += 2
            dir = 0
            done = 1


class DayTest(unittest.TestCase):
    def test_manathan(self):
        assert_that(compute(1), is_(0))
        assert_that(compute(12), is_(3))
        assert_that(compute(23), is_(2))

    def test_big(self):
        assert_that(compute(1024), is_(31))


class GridTest(unittest.TestCase):
    def test_empty_grid(self):
        expected = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]
        assert_that(empty_grid(layers=3), is_(expected))

    def test_middle(self):
        grid = [
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
        ]
        assert_that(middle(grid), is_([2, 2]))

    def test_grid(self):
        expected = [
            [17, 16, 15, 14, 13],
            [18, 5, 4, 3, 12],
            [19, 6, 1, 2, 11],
            [20, 7, 8, 9, 10],
            [21, 22, 23, 24, 25],
        ]
        assert_that(show_grid(layers=3), is_(expected))

    def test_crawl(self):
        grid = [
            [17, 16, 15, 14, 13],
            [18, 5, 4, 3, 12],
            [19, 6, 1, 2, 11],
            [20, 7, 8, 9, 10],
            [21, 22, 23, 24, 25],
        ]
        crawler = spiral_crawl(start=[2, 2])
        assert_that(next(crawler), ((2, 2)))
        assert_that(next(crawler), ((2, 3)))
        assert_that(next(crawler), ((1, 3)))
        assert_that(next(crawler), ((1, 2)))
        assert_that(next(crawler), ((1, 1)))
        assert_that(next(crawler), ((2, 1)))
        assert_that(next(crawler), ((3, 1)))
        assert_that(next(crawler), ((4, 1)))
        assert_that(next(crawler), ((4, 2)))
        assert_that(next(crawler), ((4, 3)))
        assert_that(next(crawler), ((4, 4)))


class Day2Test(unittest.TestCase):
    def test_grid1(self):
        assert_that(compute2(1), is_(2))
        assert_that(compute2(2), is_(4))
        assert_that(compute2(4), is_(5))
        assert_that(compute2(5), is_(10))
        assert_that(compute2(747), is_(806))


puzzle_input = "277678"

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

import re
import sys
import unittest
from dataclasses import dataclass
from itertools import groupby
from textwrap import dedent

from hamcrest import assert_that, is_

from y2018 import Point


def compute(data):
    points = parse(data)
    for i in range(0, 20000):
        for point in points:
            point.tick()

        left = min(point.x for point in points)
        right = max(point.x for point in points)
        top = min(point.y for point in points)
        bottom = max(point.y for point in points)

        size = abs(right - left) * abs(bottom - top)
        # if 10000 < i < 11000:
        #     print(i, "Size is", size)
        if i == 10368:
            active_points = {(p.x, p.y) for p in points}
            for y in range(top, bottom + 1):
                for x in range(left, right + 1):
                    if (x, y) in active_points:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            # for line in groupby(sorted(points, key=lambda p: (p.y, p.x)), key=lambda e: e[0]):
            #     for p in line:

    return None


def compute2(data):
    return None


def parse(data):
    points = []
    for line in data.split("\n"):
        p_x, p_y, v_x, v_y = map(int, re.match(r"position=<(.+),(.+)> velocity=<(.+),(.+)>", line).groups())
        points.append(MovingPoint(p_x, p_y, v_x, v_y))
    return points


@dataclass
class MovingPoint(Point):
    v_x: int
    v_y: int

    def tick(self):
        self.x += self.v_x
        self.y += self.v_y


class ParseTest(unittest.TestCase):
    def test_parse(self):
        input = dedent("""\
            position=< 9,  1> velocity=< 0,  2>
            position=< 7,  0> velocity=<-1,  0>
            position=< 3, -2> velocity=<-1,  1>""")

        assert_that(parse(input), is_([
            MovingPoint(9, 1, 0, 2),
            MovingPoint(7, 0, -1, 0),
            MovingPoint(3, -2, -1, 1),
        ]))


class MovingPointTest(unittest.TestCase):
    def test_tick(self):
        point = MovingPoint(3, 9, 1, -2)

        assert_that((point.x, point.y), is_((3, 9)))

        point.tick()

        assert_that((point.x, point.y), is_((4, 7)))

        point.tick()

        assert_that((point.x, point.y), is_((5, 5)))
        point.tick()

        assert_that((point.x, point.y), is_((6, 3)))


class ProvidedTest(unittest.TestCase):
    input = dedent("""\
        position=< 9,  1> velocity=< 0,  2>
        position=< 7,  0> velocity=<-1,  0>
        position=< 3, -2> velocity=<-1,  1>
        position=< 6, 10> velocity=<-2, -1>
        position=< 2, -4> velocity=< 2,  2>
        position=<-6, 10> velocity=< 2, -2>
        position=< 1,  8> velocity=< 1, -1>
        position=< 1,  7> velocity=< 1,  0>
        position=<-3, 11> velocity=< 1, -2>
        position=< 7,  6> velocity=<-1, -1>
        position=<-2,  3> velocity=< 1,  0>
        position=<-4,  3> velocity=< 2,  0>
        position=<10, -3> velocity=<-1,  1>
        position=< 5, 11> velocity=< 1, -2>
        position=< 4,  7> velocity=< 0, -1>
        position=< 8, -2> velocity=< 0,  1>
        position=<15,  0> velocity=<-2,  0>
        position=< 1,  6> velocity=< 1,  0>
        position=< 8,  9> velocity=< 0, -1>
        position=< 3,  3> velocity=<-1,  1>
        position=< 0,  5> velocity=< 0, -1>
        position=<-2,  2> velocity=< 2,  0>
        position=< 5, -2> velocity=< 1,  2>
        position=< 1,  4> velocity=< 2,  1>
        position=<-2,  7> velocity=< 2, -2>
        position=< 3,  6> velocity=<-1, -1>
        position=< 5,  0> velocity=< 1,  0>
        position=<-6,  0> velocity=< 2,  0>
        position=< 5,  9> velocity=< 1, -2>
        position=<14,  7> velocity=<-2,  0>
        position=<-3,  6> velocity=< 2, -1>""")

    def test_part_1(self):
        assert_that(compute(self.input), is_(False))

    def test_part_2(self):
        assert_that(compute2(self.input), is_(False))


puzzle_input = """\
position=< 41660,  20869> velocity=<-4, -2>
position=< 41617,  10491> velocity=<-4, -1>
position=< 41669, -10244> velocity=<-4,  1>
position=< 10509, -41348> velocity=<-1,  4>
position=<-41324, -51717> velocity=< 4,  5>
position=< 41616, -30982> velocity=<-4,  3>
position=< 31242, -51716> velocity=<-3,  5>
position=<-20570, -30976> velocity=< 2,  3>
position=< 20882,  51971> velocity=<-2, -5>
position=<-10205, -30981> velocity=< 1,  3>
position=< 31299, -20612> velocity=<-3,  2>
position=<-41320,  51974> velocity=< 4, -5>
position=<-10205, -51723> velocity=< 1,  5>
position=<-10237,  10492> velocity=< 1, -1>
position=<-10181, -10244> velocity=< 1,  1>
position=< 31275, -10243> velocity=<-3,  1>
position=< 52025,  51974> velocity=<-5, -5>
position=< 41634, -20612> velocity=<-4,  2>
position=< 41632, -20610> velocity=<-4,  2>
position=< 52028, -10247> velocity=<-5,  1>
position=<-30972,  51969> velocity=< 3, -5>
position=<-30946, -20609> velocity=< 3,  2>
position=<-30918,  31229> velocity=< 3, -3>
position=< 41618, -51714> velocity=<-4,  5>
position=< 31284,  31231> velocity=<-3, -3>
position=<-30931, -20616> velocity=< 3,  2>
position=<-30964,  31238> velocity=< 3, -3>
position=<-20577,  10495> velocity=< 2, -1>
position=< 20899, -51720> velocity=<-2,  5>
position=< 31284, -41354> velocity=<-3,  4>
position=<-20570,  10491> velocity=< 2, -1>
position=<-20605,  20865> velocity=< 2, -2>
position=<-41320, -41345> velocity=< 4,  4>
position=<-41328, -10240> velocity=< 4,  1>
position=< 20926,  41601> velocity=<-2, -4>
position=<-30967,  10491> velocity=< 3, -1>
position=< 41637, -10242> velocity=<-4,  1>
position=<-10179,  20864> velocity=< 1, -2>
position=<-51665, -10240> velocity=< 5,  1>
position=<-30951,  41600> velocity=< 3, -4>
position=<-51709, -10246> velocity=< 5,  1>
position=< 20923, -10239> velocity=<-2,  1>
position=<-41296,  31237> velocity=< 4, -3>
position=< 10521,  41601> velocity=<-1, -4>
position=<-41296, -30983> velocity=< 4,  3>
position=<-20586,  20861> velocity=< 2, -2>
position=<-10176,  10499> velocity=< 1, -1>
position=< 20894,  10493> velocity=<-2, -1>
position=< 51977, -20613> velocity=<-5,  2>
position=<-30965,  51967> velocity=< 3, -5>
position=<-41296,  20866> velocity=< 4, -2>
position=<-41334, -51714> velocity=< 4,  5>
position=< 41648,  31238> velocity=<-4, -3>
position=< 20896,  10495> velocity=<-2, -1>
position=<-20566, -30978> velocity=< 2,  3>
position=< 20910, -20609> velocity=<-2,  2>
position=<-41315,  10491> velocity=< 4, -1>
position=< 51995, -41345> velocity=<-5,  4>
position=< 10558, -51714> velocity=<-1,  5>
position=< 20870, -41345> velocity=<-2,  4>
position=<-41303,  10497> velocity=< 4, -1>
position=< 41621,  10498> velocity=<-4, -1>
position=< 41621, -51716> velocity=<-4,  5>
position=<-51689,  31230> velocity=< 5, -3>
position=<-30927,  20864> velocity=< 3, -2>
position=< 10559,  10500> velocity=<-1, -1>
position=< 10557,  20867> velocity=<-1, -2>
position=<-51672,  31238> velocity=< 5, -3>
position=< 20890, -51720> velocity=<-2,  5>
position=<-10236,  10495> velocity=< 1, -1>
position=<-30963, -10238> velocity=< 3,  1>
position=<-20603,  41605> velocity=< 2, -4>
position=<-20563,  20869> velocity=< 2, -2>
position=<-20553, -20608> velocity=< 2,  2>
position=< 31267, -51719> velocity=<-3,  5>
position=<-41285,  31229> velocity=< 4, -3>
position=< 41608,  20864> velocity=<-4, -2>
position=<-30914, -10241> velocity=< 3,  1>
position=<-41315,  20865> velocity=< 4, -2>
position=< 52021, -20613> velocity=<-5,  2>
position=< 52029, -41345> velocity=<-5,  4>
position=<-30919, -51717> velocity=< 3,  5>
position=<-20570, -41345> velocity=< 2,  4>
position=< 52012, -51714> velocity=<-5,  5>
position=<-41301, -41354> velocity=< 4,  4>
position=< 41666,  10495> velocity=<-4, -1>
position=< 52009, -30984> velocity=<-5,  3>
position=< 52017, -41354> velocity=<-5,  4>
position=<-30941, -30981> velocity=< 3,  3>
position=< 20872, -30982> velocity=<-2,  3>
position=< 31263,  41603> velocity=<-3, -4>
position=< 10530, -30984> velocity=<-1,  3>
position=< 41653,  10492> velocity=<-4, -1>
position=<-41284,  20864> velocity=< 4, -2>
position=< 31268,  51971> velocity=<-3, -5>
position=<-41288, -10240> velocity=< 4,  1>
position=<-20602,  51975> velocity=< 2, -5>
position=<-51701,  31238> velocity=< 5, -3>
position=< 31284, -51722> velocity=<-3,  5>
position=< 52006,  20866> velocity=<-5, -2>
position=< 10557, -51721> velocity=<-1,  5>
position=<-51700,  10497> velocity=< 5, -1>
position=< 10501,  31234> velocity=<-1, -3>
position=< 20927,  31233> velocity=<-2, -3>
position=< 31268, -10239> velocity=<-3,  1>
position=<-30927,  20866> velocity=< 3, -2>
position=< 20926,  41604> velocity=<-2, -4>
position=<-20574,  41602> velocity=< 2, -4>
position=< 41632, -10247> velocity=<-4,  1>
position=<-41317,  20864> velocity=< 4, -2>
position=< 10501, -20608> velocity=<-1,  2>
position=<-41283, -20609> velocity=< 4,  2>
position=<-20606, -20615> velocity=< 2,  2>
position=< 10551, -51714> velocity=<-1,  5>
position=<-20550,  51976> velocity=< 2, -5>
position=< 51997,  20860> velocity=<-5, -2>
position=<-30965, -20612> velocity=< 3,  2>
position=< 41664, -30984> velocity=<-4,  3>
position=< 41640, -10241> velocity=<-4,  1>
position=< 31283,  51970> velocity=<-3, -5>
position=< 10536,  10495> velocity=<-1, -1>
position=< 31300, -51715> velocity=<-3,  5>
position=< 41644, -41354> velocity=<-4,  4>
position=< 52006,  31234> velocity=<-5, -3>
position=< 52002, -10243> velocity=<-5,  1>
position=< 31292,  41599> velocity=<-3, -4>
position=<-51657,  10498> velocity=< 5, -1>
position=<-20586,  51974> velocity=< 2, -5>
position=< 20903, -41350> velocity=<-2,  4>
position=< 41621, -10242> velocity=<-4,  1>
position=< 51985, -10242> velocity=<-5,  1>
position=< 20899, -10245> velocity=<-2,  1>
position=< 41645,  10500> velocity=<-4, -1>
position=< 10542, -41354> velocity=<-1,  4>
position=< 10533, -41351> velocity=<-1,  4>
position=<-41300, -51723> velocity=< 4,  5>
position=< 41668, -41345> velocity=<-4,  4>
position=<-20606,  20868> velocity=< 2, -2>
position=< 41608, -10239> velocity=<-4,  1>
position=< 31273, -51723> velocity=<-3,  5>
position=<-10225, -30985> velocity=< 1,  3>
position=<-10193,  20869> velocity=< 1, -2>
position=< 41617,  31238> velocity=<-4, -3>
position=<-30938,  31229> velocity=< 3, -3>
position=< 10557,  41607> velocity=<-1, -4>
position=<-20588, -20607> velocity=< 2,  2>
position=< 51993, -41346> velocity=<-5,  4>
position=< 20890, -20613> velocity=<-2,  2>
position=<-51713,  51971> velocity=< 5, -5>
position=<-41288, -10247> velocity=< 4,  1>
position=< 10559, -30985> velocity=<-1,  3>
position=< 20905, -51714> velocity=<-2,  5>
position=< 41637,  41607> velocity=<-4, -4>
position=<-20602, -30984> velocity=< 2,  3>
position=<-20582, -20608> velocity=< 2,  2>
position=<-20595, -41345> velocity=< 2,  4>
position=< 10506, -30976> velocity=<-1,  3>
position=<-20587, -51714> velocity=< 2,  5>
position=< 41616, -30983> velocity=<-4,  3>
position=<-51678,  20860> velocity=< 5, -2>
position=<-51670,  31233> velocity=< 5, -3>
position=< 20902, -51718> velocity=<-2,  5>
position=<-30950, -41350> velocity=< 3,  4>
position=< 20912,  10491> velocity=<-2, -1>
position=< 10543, -10238> velocity=<-1,  1>
position=< 31239,  10491> velocity=<-3, -1>
position=< 10530, -51715> velocity=<-1,  5>
position=< 52006, -10247> velocity=<-5,  1>
position=<-20587, -51714> velocity=< 2,  5>
position=<-20561,  41598> velocity=< 2, -4>
position=<-10229,  51969> velocity=< 1, -5>
position=< 31247,  51971> velocity=<-3, -5>
position=<-41333, -10243> velocity=< 4,  1>
position=< 41632, -10243> velocity=<-4,  1>
position=< 41652,  41598> velocity=<-4, -4>
position=<-20593, -51718> velocity=< 2,  5>
position=<-51677, -10238> velocity=< 5,  1>
position=<-51654, -30976> velocity=< 5,  3>
position=< 41656, -10242> velocity=<-4,  1>
position=< 20930,  20869> velocity=<-2, -2>
position=< 20929, -30981> velocity=<-2,  3>
position=<-41312,  31235> velocity=< 4, -3>
position=< 31288,  41598> velocity=<-3, -4>
position=< 41649, -10241> velocity=<-4,  1>
position=<-10194, -30976> velocity=< 1,  3>
position=<-51670, -30985> velocity=< 5,  3>
position=< 20903,  20860> velocity=<-2, -2>
position=<-20566, -51714> velocity=< 2,  5>
position=<-41335,  41602> velocity=< 4, -4>
position=<-30967,  41602> velocity=< 3, -4>
position=< 20902,  41599> velocity=<-2, -4>
position=< 41628, -20615> velocity=<-4,  2>
position=<-41301, -20616> velocity=< 4,  2>
position=< 41632,  31238> velocity=<-4, -3>
position=< 20899,  20863> velocity=<-2, -2>
position=< 10546,  51976> velocity=<-1, -5>
position=<-51681,  41607> velocity=< 5, -4>
position=<-10216,  41598> velocity=< 1, -4>
position=< 41648, -10238> velocity=<-4,  1>
position=< 52033, -20612> velocity=<-5,  2>
position=< 31248, -41345> velocity=<-3,  4>
position=< 41616, -20615> velocity=<-4,  2>
position=<-51662,  51976> velocity=< 5, -5>
position=<-30962,  51970> velocity=< 3, -5>
position=< 51986,  20860> velocity=<-5, -2>
position=< 10512,  41598> velocity=<-1, -4>
position=<-30926,  41607> velocity=< 3, -4>
position=< 31271, -10238> velocity=<-3,  1>
position=< 10536, -51714> velocity=<-1,  5>
position=< 31287,  31230> velocity=<-3, -3>
position=< 10525, -41346> velocity=<-1,  4>
position=< 41640, -10242> velocity=<-4,  1>
position=<-51680, -41354> velocity=< 5,  4>
position=< 41632, -10241> velocity=<-4,  1>
position=< 20926,  31234> velocity=<-2, -3>
position=<-10196, -30979> velocity=< 1,  3>
position=< 31273, -30981> velocity=<-3,  3>
position=< 20918, -30977> velocity=<-2,  3>
position=<-30933, -30980> velocity=< 3,  3>
position=< 31239, -41354> velocity=<-3,  4>
position=< 20905,  20864> velocity=<-2, -2>
position=<-10226,  41598> velocity=< 1, -4>
position=< 31265, -20612> velocity=<-3,  2>
position=<-41312, -51723> velocity=< 4,  5>
position=< 20906, -41354> velocity=<-2,  4>
position=< 52027, -41354> velocity=<-5,  4>
position=<-30955, -30983> velocity=< 3,  3>
position=<-51688,  41602> velocity=< 5, -4>
position=<-30967, -30985> velocity=< 3,  3>
position=<-41315,  51969> velocity=< 4, -5>
position=< 20931, -41346> velocity=<-2,  4>
position=< 31268, -41353> velocity=<-3,  4>
position=<-51657,  31238> velocity=< 5, -3>
position=< 31240, -51719> velocity=<-3,  5>
position=<-20606,  31238> velocity=< 2, -3>
position=< 31243, -51715> velocity=<-3,  5>
position=<-20569, -41354> velocity=< 2,  4>
position=< 20899,  31232> velocity=<-2, -3>
position=<-10224,  20861> velocity=< 1, -2>
position=< 10521,  10495> velocity=<-1, -1>
position=< 10552, -51714> velocity=<-1,  5>
position=<-20601, -51723> velocity=< 2,  5>
position=< 10545,  41601> velocity=<-1, -4>
position=< 20921,  31238> velocity=<-2, -3>
position=<-51689,  51971> velocity=< 5, -5>
position=< 20902, -41346> velocity=<-2,  4>
position=<-10181, -10239> velocity=< 1,  1>
position=<-20574,  10498> velocity=< 2, -1>
position=<-41288, -10241> velocity=< 4,  1>
position=< 10514,  20865> velocity=<-1, -2>
position=< 31295,  31229> velocity=<-3, -3>
position=<-41303, -30976> velocity=< 4,  3>
position=< 51985,  31232> velocity=<-5, -3>
position=<-20593,  10499> velocity=< 2, -1>
position=<-51681,  41601> velocity=< 5, -4>
position=<-30958, -10238> velocity=< 3,  1>
position=< 20870,  51968> velocity=<-2, -5>
position=< 41632,  10494> velocity=<-4, -1>
position=<-20566,  10499> velocity=< 2, -1>
position=<-30919, -41352> velocity=< 3,  4>
position=< 52006, -41350> velocity=<-5,  4>
position=< 10549,  41599> velocity=<-1, -4>
position=< 51996, -10247> velocity=<-5,  1>
position=<-41344,  31235> velocity=< 4, -3>
position=<-20598, -10245> velocity=< 2,  1>
position=< 52030,  51975> velocity=<-5, -5>
position=<-41331,  41606> velocity=< 4, -4>
position=< 20930, -41350> velocity=<-2,  4>
position=<-20558,  10495> velocity=< 2, -1>
position=< 20931,  31235> velocity=<-2, -3>
position=<-30916, -51723> velocity=< 3,  5>
position=<-20558, -10239> velocity=< 2,  1>
position=< 31239,  41600> velocity=<-3, -4>
position=<-41324,  20862> velocity=< 4, -2>
position=<-10177,  10491> velocity=< 1, -1>
position=< 31300, -51720> velocity=<-3,  5>
position=< 31268, -10246> velocity=<-3,  1>
position=< 10503,  31235> velocity=<-1, -3>
position=<-20586, -20614> velocity=< 2,  2>
position=<-30927,  10492> velocity=< 3, -1>
position=< 20912,  20865> velocity=<-2, -2>
position=<-41283,  20862> velocity=< 4, -2>
position=< 52033,  10492> velocity=<-5, -1>
position=<-51700, -10239> velocity=< 5,  1>
position=<-51705,  41604> velocity=< 5, -4>
position=< 10502, -20612> velocity=<-1,  2>
position=< 10559, -51714> velocity=<-1,  5>
position=<-20547, -51719> velocity=< 2,  5>
position=< 20931, -20614> velocity=<-2,  2>
position=< 41611, -20614> velocity=<-4,  2>
position=< 52033, -30977> velocity=<-5,  3>
position=<-10237, -20612> velocity=< 1,  2>
position=<-30941, -20607> velocity=< 3,  2>
position=< 31263,  10496> velocity=<-3, -1>
position=< 31247,  31235> velocity=<-3, -3>
position=< 20922, -20616> velocity=<-2,  2>
position=< 52021,  51976> velocity=<-5, -5>
position=<-51713, -51716> velocity=< 5,  5>
position=<-41336,  31234> velocity=< 4, -3>
position=< 41640,  51972> velocity=<-4, -5>
position=< 31259, -51719> velocity=<-3,  5>
position=<-20579,  51971> velocity=< 2, -5>
position=<-10208, -10239> velocity=< 1,  1>
position=<-51665, -30978> velocity=< 5,  3>
position=<-30934,  31229> velocity=< 3, -3>
position=< 20894,  41602> velocity=<-2, -4>
position=<-20597, -20612> velocity=< 2,  2>
position=< 41666,  20860> velocity=<-4, -2>
position=< 52001, -51716> velocity=<-5,  5>
position=<-10203, -51714> velocity=< 1,  5>
position=<-10229, -30982> velocity=< 1,  3>
position=<-10181,  41603> velocity=< 1, -4>
position=< 52011, -20616> velocity=<-5,  2>
position=< 31300, -10246> velocity=<-3,  1>
position=<-20550, -20616> velocity=< 2,  2>
position=< 10520,  31238> velocity=<-1, -3>
position=<-10200, -20607> velocity=< 1,  2>
position=<-20598,  51975> velocity=< 2, -5>
position=< 31247, -41345> velocity=<-3,  4>
position=<-10189, -41351> velocity=< 1,  4>
position=< 31288, -41345> velocity=<-3,  4>
position=< 31296, -41354> velocity=<-3,  4>
position=<-51689, -51721> velocity=< 5,  5>
position=< 10533, -20608> velocity=<-1,  2>
position=< 10521,  41604> velocity=<-1, -4>
position=<-10218,  51967> velocity=< 1, -5>
position=< 20918,  51969> velocity=<-2, -5>
position=<-10229,  10498> velocity=< 1, -1>
position=< 51986, -20616> velocity=<-5,  2>
position=< 20913, -51714> velocity=<-2,  5>
position=<-51681, -41345> velocity=< 5,  4>
position=< 31297, -10243> velocity=<-3,  1>
position=<-30939, -20612> velocity=< 3,  2>
position=<-30954, -10247> velocity=< 3,  1>
position=< 51990,  20867> velocity=<-5, -2>
position=<-51654, -41354> velocity=< 5,  4>
position=<-20573, -51714> velocity=< 2,  5>
position=< 20905,  41598> velocity=<-2, -4>
position=< 51977, -51717> velocity=<-5,  5>
position=< 31300,  31234> velocity=<-3, -3>
position=< 41640, -10245> velocity=<-4,  1>
position=<-41296,  51971> velocity=< 4, -5>
position=< 10551, -30976> velocity=<-1,  3>
position=<-20554, -41345> velocity=< 2,  4>
position=< 51986,  20864> velocity=<-5, -2>
position=< 41621, -41352> velocity=<-4,  4>
position=<-30943, -41350> velocity=< 3,  4>
position=< 52010, -41354> velocity=<-5,  4>
position=<-51693, -30980> velocity=< 5,  3>
position=< 41636,  51971> velocity=<-4, -5>
position=< 52006,  41607> velocity=<-5, -4>
position=< 52012,  31233> velocity=<-5, -3>
position=< 31258, -30985> velocity=<-3,  3>
position=<-41303,  51976> velocity=< 4, -5>
position=<-30943,  10494> velocity=< 3, -1>
position=< 52009,  41598> velocity=<-5, -4>
position=<-41332, -30981> velocity=< 4,  3>
position=< 20894,  31235> velocity=<-2, -3>
position=<-10237,  31235> velocity=< 1, -3>
position=< 52038,  31232> velocity=<-5, -3>
position=< 10513,  20869> velocity=<-1, -2>
position=< 31257, -30976> velocity=<-3,  3>
position=< 52035,  51967> velocity=<-5, -5>
position=<-20577, -51716> velocity=< 2,  5>
position=<-10237,  41601> velocity=< 1, -4>
position=< 41637, -20607> velocity=<-4,  2>
position=<-20561, -30983> velocity=< 2,  3>
position=<-41336,  10495> velocity=< 4, -1>
position=< 31296,  51971> velocity=<-3, -5>
position=< 31297, -10238> velocity=<-3,  1>
position=< 51997,  51975> velocity=<-5, -5>
position=< 10533,  31237> velocity=<-1, -3>"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

import re
import unittest

import sys
from collections import defaultdict
from textwrap import dedent

from hamcrest import assert_that, is_


def compute(data):
    instructions = parse(data)

    registers = defaultdict(lambda : 0)

    for instruction in instructions:
        if instruction.cond(registers[instruction.cond_registry], instruction.cond_value):
            registers[instruction.registry] += instruction.direction * instruction.value

    return max(registers.values())


def compute2(data):
    instructions = parse(data)

    registers = defaultdict(lambda : 0)
    maxes = []

    for instruction in instructions:
        if instruction.cond(registers[instruction.cond_registry], instruction.cond_value):
            registers[instruction.registry] += instruction.direction * instruction.value
            maxes.append(max(registers.values()))

    return max(maxes)

def parse(data):
    line_parser = re.compile("^(\w+) (inc|dec) (-?\d+) if (\w+) ([<>=!]+) (-?\d+)", flags=re.MULTILINE)
    instructions = []
    for line in data.split("\n"):
        registry, direction, value, cond_registry, cond_operator, cond_value = line_parser.match(line).groups()
        instructions.append(Instruction(registry,
                                        to_dir(direction),
                                        int(value),
                                        cond_registry,
                                        to_matcher(cond_operator),
                                        int(cond_value)))

    return instructions


def to_matcher(operator):
    return {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
    }[operator]


def to_dir(direction):
    return {
        "inc": 1,
        "dec": -1
    }[direction]


class Instruction:
    def __init__(self, registry, direction, value, cond_registry, cond, cond_value):
        self.registry = registry
        self.direction = direction
        self.value = value
        self.cond_registry = cond_registry
        self.cond = cond
        self.cond_value = cond_value


class DayTest(unittest.TestCase):
    def test_example(self):
        intput = dedent("""\
            b inc 5 if a > 1
            a inc 1 if b < 5
            c dec -10 if a >= 1
            c inc -20 if c == 10""")

        assert_that(compute(intput), is_(1))

class Day2Test(unittest.TestCase):
    def test_example(self):
        intput = dedent("""\
            b inc 5 if a > 1
            a inc 1 if b < 5
            c dec -10 if a >= 1
            c inc -20 if c == 10""")

        assert_that(compute2(intput), is_(10))


class ParseTest(unittest.TestCase):
    def test(self):
        instruction = parse("pr inc -851 if g <= -228")[0]

        assert_that(instruction.registry, is_("pr"))
        assert_that(instruction.direction, is_(1))
        assert_that(instruction.value, is_(-851))
        assert_that(instruction.cond_registry, is_("g"))
        assert_that(instruction.cond(0, 1), is_(True))
        assert_that(instruction.cond_value, is_(-228))

    def test_to_dir(self):
        assert_that(to_dir("dec"), is_(-1))
        assert_that(to_dir("inc"), is_(1))


class ConditionsTest(unittest.TestCase):
    def test_equals(self):
        matcher = to_matcher("==")
        assert_that(matcher(0, 0), is_(True))
        assert_that(matcher(0, 1), is_(False))

    def test_not_equals(self):
        matcher = to_matcher("!=")
        assert_that(matcher(0, 0), is_(False))
        assert_that(matcher(0, 1), is_(True))

    def test_lower_than(self):
        matcher = to_matcher("<")
        assert_that(matcher(0, 1), is_(True))
        assert_that(matcher(1, 1), is_(False))

    def test_lower_than_or_equal(self):
        matcher = to_matcher("<=")
        assert_that(matcher(1, 1), is_(True))
        assert_that(matcher(2, 1), is_(False))

    def test_greater_than(self):
        matcher = to_matcher(">")
        assert_that(matcher(1, 0), is_(True))
        assert_that(matcher(1, 1), is_(False))

    def test_greater_than_or_equal(self):
        matcher = to_matcher(">=")
        assert_that(matcher(1, 1), is_(True))
        assert_that(matcher(1, 2), is_(False))


puzzle_input = """\
g dec 231 if bfx > -10
k dec -567 if wfk == 0
jq inc 880 if a < 2
sh inc -828 if nkr < -5
w inc 595 if nkr > -10
t dec 737 if bfx < 5
ghj dec -693 if pr == 0
yo inc -362 if t == -741
pr inc -851 if g <= -228
lpi inc 628 if lpi <= 0
pr inc -748 if qn > -9
rlq dec -290 if k <= 574
lpi inc 252 if wfk == -4
nkr dec -674 if bfx >= -7
vh dec 429 if fkp != 6
w dec 568 if w <= 604
g dec -700 if vh >= -438
lpi dec 356 if lpi >= 623
afu inc -227 if qn <= 6
m dec 329 if jq != 883
qrc dec 683 if sh != 2
sh dec -322 if qdq <= -7
fkp inc 112 if qdq >= 7
bfx dec -258 if wfk >= -1
nkr inc -259 if ev >= -1
pr dec -806 if ghj == 693
w inc -717 if nkr >= 412
rlq inc -755 if w < -686
afu inc 514 if yo <= 2
a inc 697 if bfx <= 252
qrc dec -733 if lpi > 278
jq inc 843 if ghj != 692
jh inc -321 if u <= 3
afu dec -86 if afu == 287
g inc -374 if w >= -694
m inc 681 if k < 565
ev inc -75 if u == 0
w dec 130 if lpi < 277
ev dec 139 if vh == -429
m inc -283 if m >= -332
fkp dec -48 if yo != -2
g dec -272 if t > -747
wfk dec 752 if pr < -800
bfx inc -164 if rlq != -467
k dec -470 if k <= 566
ghj dec 221 if k < 572
g dec 722 if bfx > 93
wfk dec -256 if qdq >= -7
t inc 337 if bfx > 99
w inc 134 if fkp != 48
nkr inc -605 if w <= -815
wfk dec -938 if vh >= -438
pr dec -938 if wfk < 1204
qn inc -372 if rlq <= -459
bfx dec -38 if g <= -348
qn inc 561 if fkp != 49
ghj dec 555 if rlq >= -466
qdq dec 78 if yo == 0
ev inc -466 if vh > -433
w inc -946 if qdq >= -84
w inc 735 if ghj < -74
lpi dec -616 if afu == 380
nkr dec 259 if qrc != -678
sh dec -406 if m < -620
jq dec -449 if m == -612
ev dec 990 if qrc > -691
g dec -139 if jh > -315
w inc 204 if vh <= -424
yo dec -26 if jq == 2181
a dec -528 if qrc != -688
nkr inc -926 if bfx > 128
qdq inc -241 if w <= -822
g inc -111 if wfk == 1194
bfx inc 282 if qn < 199
jq inc 413 if wfk == 1194
fkp dec -281 if ev < -1660
qrc inc -596 if qn != 199
ev inc 383 if ghj != -74
sh inc -562 if yo <= -6
sh inc 728 if wfk <= 1196
bfx dec -360 if vh < -423
jq inc -774 if qn >= 195
qn dec -939 if ghj == -87
w dec 952 if ghj == -83
yo dec -112 if lpi < 278
qn dec 902 if sh == 728
k dec 507 if qrc == -1279
g dec 155 if a != 537
rlq inc 655 if a < 530
qrc inc 523 if afu == 373
t dec 36 if jh != -319
qn dec -584 if m > -610
ev inc 406 if sh <= 730
pr dec 699 if lpi > 277
a dec 906 if k == 60
jq dec -811 if m != -615
vh inc -874 if qn <= -712
pr inc 325 if vh != -1293
nkr inc -786 if m < -607
pr inc -903 if jq != 3389
fkp inc 758 if rlq <= 182
lpi inc -307 if sh > 725
afu inc -162 if jh <= -314
afu inc -96 if k < 63
t dec 939 if pr <= -427
fkp dec -65 if a <= -370
g dec 246 if nkr > -2160
w inc 62 if sh != 727
jh dec -621 if ev > -891
wfk dec -84 if ev != -878
qdq inc 245 if sh > 725
qdq dec 689 if jh < 310
sh inc -396 if ghj < -79
yo dec 457 if pr < -429
vh dec -545 if pr > -434
rlq inc -848 if nkr > -2166
nkr inc 274 if fkp < 401
nkr inc -165 if fkp > 393
u dec 973 if t <= -1706
vh dec -874 if wfk < 1286
ghj inc 872 if lpi == -35
vh dec 476 if t == -1712
lpi inc -780 if nkr > -2062
a inc 312 if sh != 332
qdq dec -840 if a == -378
k dec 287 if qn <= -707
rlq dec 250 if jh != 304
qdq dec -870 if qrc == -756
pr dec 95 if qrc < -750
m dec 21 if jq <= 3400
qrc dec -995 if vh == -360
fkp inc 422 if g > -626
rlq inc 744 if rlq == -908
qdq dec -856 if rlq >= -168
wfk inc -53 if rlq <= -164
bfx dec 370 if a == -378
w dec 388 if lpi <= -812
jh inc -458 if a <= -375
ev dec 169 if m < -623
afu dec 673 if afu <= 117
jq dec -294 if vh >= -362
ghj inc -595 if qn >= -711
m inc -292 if lpi <= -823
wfk inc -401 if pr >= -536
w inc -846 if fkp <= 818
afu inc 224 if fkp <= 825
qdq dec -22 if fkp != 816
bfx inc 148 if qn == -713
qrc inc -253 if lpi >= -815
w inc -824 if fkp != 816
jq inc 409 if wfk <= 821
a inc -243 if ev < -1044
ev inc 784 if afu <= -329
a inc 492 if a > -625
qrc dec 675 if afu != -327
yo inc -902 if g > -623
jh inc -341 if m <= -632
rlq inc 139 if g > -622
qdq inc -156 if vh <= -355
ev inc 105 if qdq > 1646
g dec -334 if u < -981
qn inc -117 if lpi < -810
fkp dec -419 if jq > 3687
lpi inc 950 if wfk <= 830
m inc 305 if k <= -224
yo inc -355 if vh != -365
jh dec 775 if t < -1710
qrc dec 125 if nkr > -2054
lpi inc 572 if nkr <= -2049
rlq dec 913 if ghj <= 791
g dec -25 if m >= -330
bfx dec -973 if ev == -161
sh inc -500 if t >= -1718
afu inc 496 if qn < -820
afu inc 242 if vh >= -365
t dec -474 if m == -328
w dec -597 if g <= -587
qdq dec 681 if jq == 3690
k dec -349 if bfx != 1530
pr inc -430 if yo != -1595
nkr inc 105 if afu != 410
w dec -788 if jh < -1272
lpi inc 328 if ghj >= 785
rlq inc 694 if vh <= -368
a inc 965 if ev != -168
g inc -962 if jq < 3690
pr inc -181 if lpi == 1035
rlq dec 509 if rlq >= -947
k dec -991 if w >= -1573
bfx dec -516 if qrc < -816
a dec 679 if qdq == 961
lpi inc -640 if jh <= -1273
w dec -13 if rlq >= -1440
m dec 535 if lpi > 402
sh dec -358 if t > -1241
qdq inc -647 if wfk > 821
u dec 409 if a < 838
lpi dec 745 if wfk < 832
yo dec 422 if w < -1564
jq dec 555 if m > -319
fkp inc 202 if qrc < -805
wfk dec -52 if vh == -355
pr inc 473 if jq < 3699
bfx dec -202 if pr > -674
fkp inc 907 if ghj <= 787
yo inc -617 if rlq > -1455
jq inc -300 if jq != 3699
u dec 910 if nkr < -1945
g dec -880 if bfx < 1722
ev inc 47 if ev > -166
a inc 372 if afu == 404
u inc 318 if qdq != 319
afu inc 942 if qdq == 319
sh dec 522 if ghj <= 793
m dec -785 if g <= -588
pr dec 878 if qrc <= -805
a inc -812 if m != 452
wfk dec -695 if lpi >= -355
qdq dec -493 if jh >= -1279
pr dec 325 if k < 1115
nkr inc 581 if sh >= -333
a dec -368 if pr == -1861
ghj dec 135 if qn >= -835
jh dec -209 if a < 406
u dec -518 if lpi > -352
qdq inc 598 if t > -1239
k dec -879 if m != 459
fkp dec -587 if nkr == -1366
yo dec -902 if qrc <= -806
nkr dec -948 if yo == -1739
pr inc -317 if k != 1998
ghj inc 535 if bfx == 1722
nkr inc -72 if vh == -360
ev dec -234 if rlq != -1455
a dec 869 if k == 1992
ev inc -397 if yo >= -1746
bfx dec 642 if bfx <= 1734
jq dec 501 if jh <= -1057
w inc 900 if qdq == 1410
lpi dec 742 if ev >= -277
pr dec 842 if rlq != -1441
qdq inc -56 if a == -473
jh dec -421 if a != -470
jq inc 60 if k >= 1997
lpi inc 181 if g <= -592
jh inc -888 if afu < 1349
w inc 271 if lpi >= -912
wfk dec 319 if jq <= 2890
qrc inc 144 if vh >= -368
rlq dec 263 if nkr <= -492
sh inc 214 if wfk <= 1208
k inc -39 if qrc < -673
rlq dec -388 if qn == -830
fkp inc 917 if vh > -366
u dec -225 if qrc < -663
lpi dec -741 if u > -1550
lpi inc -176 if afu <= 1354
u inc 454 if k <= 1995
qn inc 623 if rlq >= -1059
fkp inc 642 if nkr < -485
jh dec 895 if pr < -3027
k dec 240 if fkp < 3592
afu dec 772 if vh < -367
nkr dec 913 if a < -467
vh inc -941 if lpi != -336
pr inc -623 if nkr != -1409
g dec 849 if qdq != 1356
bfx dec -647 if t >= -1240
jh dec 654 if w != -398
a inc -938 if g != -1442
jq dec 545 if yo > -1747
qdq dec 183 if vh >= -1301
fkp inc -628 if qn != -212
u dec -89 if qdq == 1171
qrc inc -623 if m > 448
pr inc 61 if t < -1237
u dec 83 if qn < -204
qrc inc 179 if m <= 466
nkr dec 2 if nkr != -1408
fkp dec 813 if u >= -1094
sh dec -127 if sh < -111
qdq dec 697 if rlq <= -1069
t dec 191 if k == 1752
u dec 352 if bfx != 1725
nkr inc 188 if fkp == 2145
qn inc -300 if wfk >= 1192
nkr dec -520 if jq >= 2345
pr dec 957 if g < -1446
g inc -2 if g <= -1436
w dec -64 if vh <= -1307
qn inc 290 if w < -387
yo dec -511 if bfx > 1726
qrc inc -534 if bfx < 1742
fkp dec 456 if qn == -226
ev dec 409 if pr > -3597
k dec 457 if lpi > -348
t inc -705 if bfx > 1728
a dec 935 if u >= -1450
a inc -904 if vh > -1309
ev inc 873 if u < -1434
m inc 704 if k != 1286
m inc -331 if qn > -213
t inc -5 if m <= 1161
yo dec 153 if rlq >= -1066
qn dec -693 if u <= -1436
w dec -812 if g > -1451
ghj inc -838 if ev > 180
vh inc -462 if jh <= -3077
rlq inc 806 if bfx <= 1738
nkr dec 827 if yo >= -1387
sh inc -200 if m > 1154
m inc 397 if t == -2147
qdq dec -345 if qrc == -1648
ev inc -238 if afu > 1337
ev dec -284 if u >= -1448
g dec 108 if afu == 1346
ghj inc 291 if ev != 230
jh inc -367 if rlq == -253
u inc -88 if m != 1164
qrc inc -513 if m >= 1160
m inc 428 if bfx == 1734
wfk inc -566 if w <= 421
nkr dec 795 if w < 426
k dec -372 if sh <= -189
lpi inc -167 if t < -2137
rlq dec -939 if qdq != 1522
yo dec 223 if jh < -3439
qrc dec -151 if ghj < 108
fkp inc 172 if ev > 229
qdq inc -527 if u == -1529
u dec -376 if vh == -1763
nkr inc 201 if u <= -1149
qdq dec -277 if pr != -3595
ghj dec 560 if qdq > 1256
sh inc -957 if jh <= -3444
a inc 926 if wfk >= 627
pr dec -156 if yo < -1594
rlq inc 942 if t >= -2147
qrc inc -702 if rlq != 1620
qdq inc -202 if g >= -1550
ghj dec 939 if fkp < 2320
qdq dec -990 if jq == 2344
vh inc -584 if qdq != 2262
ev dec 893 if wfk >= 631
pr inc 441 if jh <= -3444
m inc 262 if fkp >= 2309
k inc 784 if g == -1555
jq dec 425 if lpi >= -520
pr dec 703 if qn == 481
afu dec 380 if yo < -1612
qrc dec 919 if sh == -1148
qdq inc 148 if jh != -3456
k inc -203 if m >= 1425
sh dec -5 if qdq >= 2403
w dec -310 if pr < -2992
u inc -631 if nkr > -2827
fkp dec 858 if u <= -1789
ev dec 351 if wfk != 636
sh inc 875 if ghj >= -1400
qn inc 206 if qn == 476
pr inc -973 if pr >= -2988
qrc inc 267 if a < -2315
k inc -176 if lpi != -519
g dec -388 if sh <= -267
ghj dec 706 if lpi >= -516
sh dec -616 if rlq == 1628
fkp dec 199 if g < -1157
qn dec 749 if qn > 687
qn inc -250 if wfk == 634
m dec 4 if qdq > 2398
t inc 723 if ev >= -1015
w dec 377 if ev < -1006
qdq inc 662 if sh > 340
yo inc 944 if ev < -1011
nkr inc 625 if bfx >= 1732
bfx inc 313 if vh < -2350
u inc -675 if ghj != -2098
bfx dec -228 if vh >= -2349
lpi inc -269 if ev > -1006
qn dec -264 if ghj < -2091
yo inc -718 if vh == -2347
ghj dec -646 if k < 2276
m inc -541 if u != -1793
w inc 809 if jh >= -3456
qrc dec 962 if jq <= 1912
k dec -908 if lpi > -514
g dec -163 if m < 884
pr inc -801 if vh < -2338
a inc 958 if vh < -2341
fkp inc 452 if vh >= -2347
nkr dec -481 if k < 3179
g inc 682 if u >= -1778
vh dec -178 if bfx >= 1968
qn dec -293 if qn > 686
sh dec 612 if sh != 352
bfx dec 473 if lpi <= -505
m dec 77 if a != -1376
rlq dec 709 if qn != 987
vh inc -342 if qdq >= 3068
lpi dec -146 if t <= -1416
vh inc 949 if nkr >= -2209
jh dec -311 if rlq < 926
yo dec 407 if qn > 987
qrc inc -530 if qdq != 3056
lpi inc -879 if pr >= -3802
qrc dec -456 if qn <= 987
t dec -656 if pr < -3785
a dec 382 if wfk != 629
pr inc -873 if u != -1790
ev dec -719 if wfk >= 628
qrc dec -324 if fkp > 2569
g dec -53 if qrc >= -3892
bfx inc -869 if ghj < -1446
ev dec 528 if a < -1739
sh inc 260 if vh <= -1402
yo inc -751 if afu > 1354
afu inc -609 if pr == -4667
wfk inc -413 if m >= 798
u inc -701 if lpi <= -1245
ev dec -712 if nkr != -2205
sh dec 482 if fkp != 2558
nkr dec -302 if a >= -1753
k inc -354 if m < 795
bfx inc 949 if sh == -746
lpi dec 407 if u <= -2480
qn dec -759 if pr < -4666
rlq dec 118 if afu > 733
w inc -978 if g == -1004
sh inc -379 if qrc != -3894
a inc 331 if wfk > 213
wfk dec 476 if bfx == 1567
vh dec 980 if qdq > 3073
jq inc 596 if nkr > -1901
nkr inc 142 if fkp <= 2573
yo inc -343 if sh >= -753
bfx inc 422 if a != -1427
a dec -593 if bfx <= 1994
ghj dec 674 if qdq <= 3062
ghj inc -759 if w > 172
qn dec -754 if qdq >= 3060
qdq dec 971 if qn <= 2507
w inc 183 if nkr != -1756
vh dec 27 if jh != -3145
m inc -466 if t < -758
qdq inc 28 if u != -2477
nkr inc -676 if qdq >= 2119
jh inc -701 if afu >= 731
bfx inc -995 if nkr < -2432
vh inc -211 if sh == -746
pr dec 896 if lpi > -1659
sh dec 259 if pr > -5568
m dec 138 if fkp <= 2566
g dec 420 if qrc <= -3888
vh inc 840 if yo > -3074
nkr dec 642 if a <= -824
nkr inc 524 if w >= 359
ghj dec -992 if wfk == -255
qrc dec -75 if vh == -796
bfx inc 1000 if g < -1423
g dec -716 if a >= -819
nkr inc -806 if sh != -999
pr inc 83 if yo < -3062
pr dec 231 if g != -1424
vh inc 99 if lpi <= -1651
u inc -294 if t <= -759
fkp inc -163 if wfk < -245
k inc -221 if afu == 727
w dec -661 if qn == 2502
ev inc -892 if nkr > -3364
fkp inc -224 if g != -1434
fkp inc -517 if t > -752
sh dec 268 if qrc != -3811
sh inc 907 if bfx == 1994
sh inc -441 if afu > 728
yo inc 81 if fkp == 2176
lpi inc -280 if ghj >= -1227
qdq inc -133 if ev > -1000
afu dec -91 if fkp == 2180
qn inc 513 if k <= 3191
u dec -441 if bfx == 1994
m dec 294 if qdq > 2113
w inc 43 if ev > -1004
w inc 742 if ev > -998
ev inc -574 if rlq > 801
wfk dec 811 if qdq <= 2127
bfx dec -710 if nkr <= -3349
jh inc -249 if lpi < -1933
jh inc 471 if jq >= 2506
ev inc 172 if qdq > 2118
m dec 7 if qrc >= -3811
u inc 409 if afu > 823
qn dec 320 if qrc < -3820
vh inc 861 if g == -1424
pr inc 303 if ev > -830
vh inc 939 if sh < -810
a dec 903 if a >= -815
jq inc 933 if sh != -815
qn inc 614 if k != 3188
ev dec 864 if jh == -3367
jh dec -590 if rlq == 801
yo dec 115 if u != -1924
wfk dec 254 if m == 41
sh dec 259 if fkp >= 2171
ghj inc 571 if bfx <= 2704
ghj dec 128 if g == -1424
k dec 462 if bfx != 2704
nkr inc 874 if w <= 1076
qrc inc -180 if ghj == -776
qn inc 812 if rlq == 801
afu inc 297 if qn >= 4437
wfk dec 497 if pr >= -5170
ghj dec -805 if vh == 169
sh inc 655 if bfx == 2704
lpi dec -494 if nkr < -2476
nkr dec -53 if pr > -5181
jq dec -486 if nkr == -2430
vh dec 708 if sh <= -407
fkp dec -260 if k == 3183
rlq dec -629 if g == -1429
nkr inc -863 if m == 41
k inc 897 if k >= 3180
u dec -471 if afu >= 1122
yo dec 460 if afu != 1134
ghj inc 211 if k > 4073
jq dec -10 if vh < -535
afu inc -526 if pr != -5167
qdq inc 399 if wfk != -1319
rlq dec 426 if t < -757
ev inc -292 if bfx == 2698
vh inc -345 if qdq <= 2513
jq dec -722 if k != 4083
w dec -15 if sh == -411
m dec -191 if lpi == -1439
t inc -72 if jh >= -2780
sh inc -664 if jh != -2777
lpi inc 647 if jh > -2784
k inc -651 if afu == 599
a inc -431 if nkr < -3287
pr dec 254 if g <= -1418
bfx inc 288 if ev >= -1683
jh inc -473 if wfk < -1327
jq dec 871 if qdq < 2529
jq dec 206 if bfx < 2709
m inc 829 if vh <= -535
qrc dec 412 if qrc <= -3995
g dec -881 if wfk > -1323
qn dec -999 if u >= -1448
ghj inc -807 if u >= -1459
rlq dec -967 if sh > -421
rlq inc -608 if vh < -536
t inc -686 if bfx != 2702
yo inc -228 if t >= -1520
a inc 650 if afu > 597
sh dec -918 if fkp > 2436
m inc 210 if jq == 3589
wfk dec -634 if vh > -535
t inc -360 if pr < -5427
m inc 899 if k > 3424
afu dec -768 if jq < 3594
rlq inc -990 if ghj == -1372
t inc -859 if pr < -5438
lpi inc -961 if jq == 3589
bfx dec -476 if rlq != -248
lpi dec -238 if ev > -1697
yo dec -634 if jh >= -2782
a inc -111 if jh != -2774
bfx inc 805 if bfx < 3185
ghj inc -497 if jh <= -2771
sh inc 496 if g == -543
ev dec 555 if jh == -2777
jq inc -547 if wfk >= -1320
wfk inc -489 if rlq != -256
sh dec -212 if ev > -2242
nkr dec 890 if vh == -544
t inc 639 if rlq == -256
ghj inc 397 if jq != 3047
qn inc -489 if bfx <= 3992
rlq dec -359 if a != -720
u inc -474 if t == -1239
jh inc 205 if jh != -2782
t inc -581 if lpi <= -1514
vh inc -319 if afu <= 1370
w dec 908 if yo > -3248
wfk inc 333 if qdq < 2528
qn dec -736 if afu < 1367
afu dec -208 if t > -1824
bfx inc -918 if yo < -3237
a dec -729 if lpi == -1515
u dec -331 if jh < -2577
pr inc -364 if ghj >= -1480
fkp dec 48 if m != 2170
rlq inc 117 if jq <= 3044
qdq dec 867 if wfk == -987
fkp inc 17 if w != 185
lpi dec -5 if ghj <= -1472
qrc dec -512 if u >= -1934
nkr dec -110 if g < -534
afu dec -42 if nkr != -4076
w dec 538 if vh < -856
qrc inc 248 if wfk < -978
qrc inc -797 if qn > 3955
yo dec -672 if jq > 3033
a inc 239 if qdq != 1655
rlq dec -568 if ev < -2247
g dec 958 if qn <= 3952
pr inc 212 if wfk > -991
rlq dec 674 if pr < -5579
m inc 605 if sh > 998
qn dec 575 if wfk <= -978
ghj inc 599 if t == -1820
jq dec -170 if lpi == -1510
ev inc -832 if qrc > -3656
ev dec 52 if ghj > -869
vh inc 248 if u > -1934
t dec 947 if bfx != 3075
jh inc 25 if qdq > 1654
sh inc 192 if qn == 3377
a inc 861 if yo <= -2561
yo inc 326 if m == 2775
afu dec -180 if g >= -1502
fkp dec -489 if bfx == 3067
jh dec 902 if afu > 1787
u inc -116 if ghj != -866
afu dec 854 if g >= -1505
pr dec 207 if pr != -5578
jq dec 600 if rlq >= -458
fkp dec -550 if afu <= 946
qn inc 374 if g >= -1509
afu inc -143 if pr != -5793
qdq dec 649 if rlq != -460
wfk dec 250 if lpi < -1508
t dec 61 if vh >= -620
afu inc -194 if vh == -612
jh inc -33 if k > 3423
jh dec -233 if bfx != 3073
qrc inc -159 if jh < -3244
jq inc 608 if fkp <= 3491
bfx dec -19 if pr == -5790
t dec -942 if ev != -3080
g dec -356 if wfk == -1247
yo dec 172 if qdq <= 1007
fkp inc 791 if lpi > -1511
jh inc 244 if lpi > -1513
afu dec 891 if qn == 3751
yo dec -23 if jh == -3005
ghj dec 451 if ghj == -873
jh dec 202 if g < -1497
qdq inc 876 if t < -1895
sh inc 698 if k < 3438
sh dec 836 if afu != -82
lpi dec -928 if a > 875
jh inc 730 if qdq < 1011
bfx inc -318 if qn <= 3752
k dec -329 if rlq >= -448
lpi inc 354 if pr > -5793
lpi inc -937 if fkp == 4287
wfk inc -267 if nkr >= -4073
bfx inc 466 if t != -1881
t inc -841 if rlq != -461
w inc 135 if m < 2781
u inc -861 if qdq <= 1012
wfk dec -66 if jh < -2469
w dec -527 if ghj != -1324
g dec -560 if k < 3435
lpi inc 907 if qrc != -3810
qdq dec -423 if pr >= -5795
bfx inc -118 if qdq == 1429
pr inc -918 if qrc <= -3806
a dec -127 if ghj <= -1317
qn dec -740 if m > 2768
qdq inc -431 if yo <= -2391
nkr inc 80 if rlq < -456
jh dec -189 if w <= -235
w inc 651 if afu >= -93
jq dec -455 if w > 417
qdq dec 756 if t <= -2725
qdq inc -869 if ev != -3071
ev dec -161 if qdq != -624
a dec -717 if qn < 4495
pr inc -134 if t > -2731
ev inc -592 if jh != -2485
a dec 850 if u >= -2912
jq inc -399 if ghj == -1324
nkr dec 423 if t >= -2734
vh dec 860 if wfk != -1439
sh inc 475 if g >= -946
t inc 33 if k >= 3436
qdq inc 183 if bfx != 3124
m dec 802 if pr < -6841
a inc 579 if fkp != 4282
qdq dec 705 if ghj != -1324
qn inc 856 if afu > -101
vh inc -856 if qn < 5354
t dec 80 if bfx != 3115
qn inc -881 if a < 1456
pr inc -772 if wfk <= -1436
t inc -874 if rlq == -446
wfk inc -710 if rlq < -451
wfk dec -584 if vh > -2339
pr dec 41 if pr == -7614
vh dec 430 if jh > -2487
qn dec 736 if sh < 1542
w inc 912 if u <= -2909
lpi inc -469 if lpi >= -2095
u inc 981 if vh > -2760
sh inc -884 if lpi > -2565
qrc dec -832 if sh >= 642
lpi dec -139 if jh != -2480
w inc -369 if w > 1339
qrc dec -470 if lpi < -2419
qdq dec 535 if qrc < -2501
m dec -160 if rlq < -449
m inc 480 if qrc != -2501
jq dec 46 if ghj >= -1324
fkp inc 691 if nkr == -4501
m inc -364 if pr != -7658
ghj inc 619 if nkr < -4502
wfk inc 99 if qdq == -979
t inc -494 if nkr < -4486
jh inc 243 if jh == -2477
bfx inc 446 if pr >= -7658
sh dec -137 if ghj <= -1321
pr inc 782 if jq >= 2615
pr inc 341 if u < -2918
jh dec -195 if jq == 2622
jh inc -738 if qn >= 3726
k inc -678 if pr <= -6864
bfx dec 895 if vh < -2760
nkr inc -511 if qdq < -980
afu dec 443 if m == 2249
k inc -192 if bfx == 2667
qdq dec 773 if qdq != -980
u dec -371 if ghj <= -1319
t dec 235 if a >= 1442
lpi dec 575 if jh >= -2774
k dec -185 if yo < -2389
rlq dec 663 if lpi <= -2421
a dec 56 if vh < -2758
ghj inc -81 if ev > -3504
pr inc 276 if ev > -3505
u dec -402 if t >= -3535
vh inc 968 if w > 1333
ghj dec -413 if rlq != -1124
ev inc 846 if qn < 3733
nkr inc -604 if k > 2743
t inc -165 if sh <= 775
ev dec 16 if a > 1388
m inc -148 if afu != -532
nkr inc -877 if u < -2533
k inc -785 if wfk > -1474
jq inc 896 if fkp > 4281
ghj dec -659 if ghj != -911
k dec 432 if afu >= -534
nkr dec 57 if qdq <= -1743
qn inc -324 if m != 2101
qn inc 522 if m <= 2107
sh inc 201 if k == 1520
rlq inc 341 if pr > -6879
yo dec -691 if g < -943
t inc -415 if afu <= -532
afu dec -980 if pr == -6873
ghj dec 11 if bfx != 2670
afu inc 873 if ghj < -920
k inc 389 if wfk != -1472
u inc 931 if w > 1332
qrc dec 565 if t != -3958
a inc -729 if rlq < -768
sh dec -345 if nkr > -6039
w inc 553 if m > 2097
lpi dec -388 if qdq != -1755
m dec 766 if fkp >= 4283
vh inc -80 if qdq <= -1751
g inc -839 if qn == 4252
w dec 8 if a >= 672
rlq inc -499 if a == 662
pr dec -627 if yo != -2399
m dec -848 if rlq < -1270
vh dec 150 if qn > 4245
k inc 572 if ghj == -922
g inc 953 if ev >= -2683
lpi dec 731 if fkp == 4287
ev dec 800 if qn > 4247
ev inc 743 if m < 2189
g dec 349 if pr != -6249
pr dec -548 if jq < 3523
m inc 611 if qrc != -3073
ev dec -843 if k == 2492
t inc 444 if vh != -2023
qn inc 101 if m == 2183
lpi dec -749 if pr > -5708
t inc 992 if nkr >= -6039
sh inc -859 if jh < -2781
sh dec 456 if lpi > -2026
ghj inc -765 if w < 1883
k dec -268 if sh < 682
yo inc -994 if sh >= 669
t inc -124 if ev > -2744
jh inc -807 if g < -1170
vh inc -509 if a != 652
ghj inc -904 if ghj == -913
rlq dec -727 if ev > -2740
vh inc -752 if wfk > -1475
k inc 252 if g == -1176
qrc dec -220 if g == -1176
rlq inc 850 if afu > 1314
ghj dec 256 if jh >= -3589
u dec -644 if qdq < -1750
qrc dec -156 if k != 3018
pr dec 540 if lpi < -2013
lpi inc -138 if t == -3086
w inc -935 if ev == -2737
qn inc -507 if lpi > -2019
qn inc -951 if yo == -3390
qdq inc -264 if jh > -3591
wfk dec -87 if u > -965
qn dec -130 if nkr < -6029
g inc -245 if t != -3076
jq inc 992 if qdq < -2013
wfk inc 169 if g <= -1416
m dec -822 if qdq != -2016
vh dec -900 if pr > -6233
ghj inc -57 if sh >= 670
ev dec -617 if pr <= -6229
t inc -284 if w != 958
fkp dec 148 if sh > 664
jq dec 813 if yo < -3385
sh inc 582 if m >= 2181
k inc -737 if vh == -3284
rlq dec 133 if sh < 1250
nkr dec 990 if ev < -2114
lpi dec 144 if jh < -3574
a dec -303 if rlq <= 302
qdq inc 140 if jh == -3583
wfk dec -274 if qn != 3976
qrc dec 982 if ev > -2129
a dec 118 if a <= 956
bfx inc 302 if k >= 2263
rlq dec 286 if ghj != -1238
vh inc -79 if nkr <= -7017
m dec -151 if u > -972
jh dec -165 if w == 953
fkp inc -879 if fkp != 4129
t dec -926 if fkp >= 3267
rlq inc 659 if rlq > 14
qrc dec -879 if bfx <= 2977
pr dec -568 if fkp <= 3265
ghj dec 941 if t == -3367
m inc 852 if jh <= -3411
k inc 781 if nkr == -7024
fkp dec -731 if rlq < 681
w inc -147 if u == -957
vh inc 928 if k == 3052
t inc -993 if qdq != -2015
u inc 920 if wfk != -1216
qrc dec -891 if pr != -5673
rlq inc 195 if fkp > 3985
jq dec 837 if rlq >= 861
nkr inc -784 if pr == -5670
u inc 873 if w < 963
t dec -903 if rlq == 870
qn inc 751 if jq != 2851
jh inc 591 if bfx != 2971
wfk dec -608 if m < 3187
rlq inc 16 if qdq != -2012
qn inc -188 if t <= -3452
vh inc -24 if m < 3187
ev dec -614 if rlq < 888
a inc -889 if qdq <= -2014
qn dec -268 if m < 3189
yo dec 881 if afu <= 1319
rlq inc -157 if qdq < -2006
pr dec -159 if afu >= 1311
ev dec 780 if fkp == 3990
yo dec -893 if bfx <= 2974
w inc 62 if m <= 3189
w inc 876 if qdq == -2016
w inc -860 if g >= -1426
t dec -819 if lpi < -2167
g inc -258 if ghj != -2184
bfx dec -116 if ghj > -2184
yo inc -995 if m >= 3182
vh dec -479 if vh == -2459
g inc 896 if yo == -4369
ghj inc -594 if w < 1029
jh dec -204 if g > -786
jh inc -320 if rlq >= 729
wfk inc 699 if u < 840
nkr dec -785 if sh < 1248
ev inc -21 if k <= 3061
k dec -540 if jq >= 2860
a dec 282 if a != 76
ev dec 320 if fkp == 3990
ghj dec -655 if k != 3588
nkr inc 31 if sh < 1263
qrc dec 182 if qn != 4807
wfk dec 453 if k > 3590
fkp inc -535 if yo >= -4376
qn inc -304 if rlq == 729
jh inc 46 if t != -3453
rlq dec -90 if bfx == 3085
u inc -448 if m == 3186
bfx inc -855 if jq == 2860
lpi inc 574 if bfx < 2231
qdq dec -247 if vh < -1974
pr dec 795 if qrc <= -1911
rlq dec -363 if u == 382
wfk dec 924 if g >= -780
u inc 883 if lpi >= -1593
w inc 819 if ghj == -1521
sh dec 299 if lpi > -1593
bfx dec 677 if a != 76
lpi dec -513 if fkp > 3447
ghj dec 149 if w > 1841
rlq dec 760 if fkp == 3456
jh inc -371 if vh == -1980
fkp inc -613 if w < 1851
ev inc -657 if qrc != -1912
qdq inc -594 if k < 3597
fkp inc -974 if qdq < -2354
fkp dec -797 if jq >= 2870
jh dec 131 if sh <= 957
lpi dec 350 if fkp >= 1861
ghj dec -888 if afu != 1312
rlq inc 43 if jq >= 2859
u inc 604 if a > 69
jq inc -490 if qrc != -1909
w inc -816 if a >= 74
afu inc 3 if rlq > 467
yo dec 688 if jq <= 2866
jh dec 134 if qn < 4506
afu dec -838 if ghj > -788
g inc -201 if qn < 4507
qn inc 216 if m <= 3188
qdq inc -311 if qn < 4729
qrc inc -418 if fkp > 1860
yo dec 109 if qrc <= -2326
qrc dec 29 if jq == 2854
yo inc -110 if m <= 3187
k inc 80 if wfk == -355
ghj inc -195 if ghj > -788
lpi dec 758 if w != 1044
jh dec -573 if fkp >= 1866
rlq inc 35 if qrc == -2327
pr dec -990 if lpi <= -2175
wfk inc -456 if vh > -1985
rlq inc 631 if a > 72
yo inc 116 if k <= 3678
g inc 85 if qdq <= -2667
ev dec -75 if g >= -903
ev dec -646 if lpi > -2184
nkr dec 870 if afu > 2154
jq inc -53 if m < 3189
afu dec 611 if nkr < -8646
m dec -287 if g < -897
nkr inc 36 if a < 85
nkr inc 54 if vh > -1982
wfk inc 109 if g < -894
afu dec 439 if afu <= 1553
bfx inc 471 if ghj == -977
nkr inc 76 if w >= 1027
m inc 420 if yo <= -5160
u dec 379 if a <= 79
g dec -318 if lpi == -2182
rlq dec -827 if g == -581
vh inc 985 if fkp >= 1869
afu dec 451 if ghj >= -979
m dec 366 if qdq < -2678
yo dec -144 if yo == -5160
t inc -342 if m > 3889
k inc 351 if m <= 3900
nkr inc 232 if rlq >= 1955
afu inc -56 if qn != 4715
qdq inc 964 if sh <= 959
qn inc -818 if pr != -4520
qrc inc -291 if afu > 592
t inc 121 if g < -577
rlq inc -364 if u >= 1485
u dec -730 if vh < -1002
qrc dec 612 if rlq <= 1598
g inc -540 if t == -3678
rlq dec 717 if wfk == -702
wfk dec 501 if jh <= -2952
qn dec 502 if qdq >= -1712
qdq dec -30 if m >= 3891
qn inc 962 if nkr < -8246
m inc 270 if jh > -2970
wfk dec 872 if yo == -5024
yo dec 872 if lpi <= -2181
bfx inc 552 if jq >= 2812
fkp inc -443 if vh > -998
nkr inc 571 if vh >= -992
vh dec -465 if qdq >= -1682
u inc 613 if nkr < -8246
nkr inc 63 if rlq < 880
qn inc -430 if sh == 957
qrc inc -495 if pr > -4530
vh inc 229 if w == 1034
bfx inc 184 if jq >= 2801
jq inc -41 if lpi <= -2192
afu dec 990 if wfk < -1202"""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

import unittest
from textwrap import dedent

from hamcrest import assert_that, is_

U = 'U'
R = 'R'
D = 'D'
L = 'L'

X = 1
Y = 0

VOID = '-'
def compute(input):
    matrix = [
        ["-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "1", "-", "-", "-"],
        ["-", "-", "2", "3", "4", "-", "-"],
        ["-", "5", "6", "7", "8", "9", "-"],
        ["-", "-", "A", "B", "C", "-", "-"],
        ["-", "-", "-", "D", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-"]
    ]

    commands = input.split()

    result = ""
    pos = [3, 1]
    for command in commands:
        for move in command:
            if move == U and matrix[pos[Y] - 1][pos[X]] != VOID:
                pos[Y] -= 1
            if move == D and matrix[pos[Y] + 1][pos[X]] != VOID:
                pos[Y] += 1
            if move == L and matrix[pos[Y]][pos[X] - 1] != VOID:
                pos[X] -= 1
            if move == R and matrix[pos[Y]][pos[X] + 1] != VOID:
                pos[X] += 1

        result += matrix[pos[Y]][pos[X]]

    return result


class ComputeTest(unittest.TestCase):
    def test_going_up(self):
        assert_that(compute("U"), is_("5"))
        assert_that(compute("UU"), is_("5"))
        assert_that(compute("LUU"), is_("5"))
        assert_that(compute("RUU"), is_("2"))
        assert_that(compute("DLUUU"), is_("5"))
        assert_that(compute("DUUU"), is_("5"))
        assert_that(compute("DRUUU"), is_("2"))

    def test_going_right(self):
        assert_that(compute("R"), is_("6"))
        assert_that(compute("RR"), is_("7"))
        assert_that(compute("URR"), is_("7"))
        assert_that(compute("DRR"), is_("7"))
        assert_that(compute("LURRR"), is_("8"))
        assert_that(compute("LRRR"), is_("8"))
        assert_that(compute("LDRRR"), is_("8"))

    def test_going_down(self):
        assert_that(compute("D"), is_("5"))
        assert_that(compute("DD"), is_("5"))
        assert_that(compute("LDD"), is_("5"))
        assert_that(compute("RDD"), is_("A"))
        assert_that(compute("ULDDD"), is_("5"))
        assert_that(compute("UDDD"), is_("5"))
        assert_that(compute("URDDD"), is_("A"))

    def test_going_left(self):
        assert_that(compute("L"), is_("5"))
        assert_that(compute("LL"), is_("5"))
        assert_that(compute("ULL"), is_("5"))
        assert_that(compute("DLL"), is_("5"))
        assert_that(compute("RULLL"), is_("2"))
        assert_that(compute("RLLL"), is_("5"))
        assert_that(compute("RDLLL"), is_("A"))

    def test_1(self):
        result = compute(dedent("""
            ULL
            RRDDD
            LURDL
            UUUUD
        """))
        assert_that(result, is_("5DB3"))


if __name__ == '__main__':
    print("Result is {}".format(compute(dedent("""
            LDUDDRUDRRURRRRDRUUDULDLULRRLLLUDDULRDLDDLRULLDDLRUURRLDUDDDDLUULUUDDDDLLLLLULLRURDRLRLRLLURDLLDDUULUUUUDLULLRLUUDDLRDRRURRLURRLLLRRDLRUDURRLRRRLULRDLUDRDRLUDDUUULDDDDDURLDULLRDDRRUDDDDRRURRULUDDLLRRDRURDLLLLLUUUDLULURLULLDRLRRDDLUDURUDRLRURURLRRDDLDUULURULRRLLLDRURDULRDUURRRLDLDUDDRLURRDRDRRLDLRRRLRURDRLDRUDLURRUURDLDRULULURRLDLLLUURRULUDDDRLDDUDDDRRLRDUDRUUDDULRDDULDDURULUDLUDRUDDDLRRRRRDLULDRLRRRRUULDUUDRRLURDLLUUDUDDDLUUURDRUULRURULRLLDDLLUDLURRLDRLDDDLULULLURLULRDLDRDDDLRDUDUURUUULDLLRDRUDRDURUUDDLRRRRLLLUULURRURLLDDLDDD
            DRURURLLUURRRULURRLRULLLURDULRLRRRLRUURRLRRURRRRUURRRLUDRDUDLUUDULURRLDLULURRLDURLUUDLDUDRUURDDRDLLLDDRDDLUUDRDUDDRRDLDUDRLDDDRLLDDLUDRULRLLURLDLURRDRUDUDLDLULLLRDLLRRDULLDRURRDLDRURDURDULUUURURDLUDRRURLRRLDULRRDURRDRDDULLDRRRLDRRURRRRUURDRLLLRRULLUDUDRRDDRURLULLUUDDRLDRRDUDLULUUDRDDDDLRLRULRLRLLDLLRRDDLDRDURRULLRLRRLULRULDDDRDRULDRUUDURDLLRDRURDRLRDDUDLLRUDLURURRULLUDRDRDURLLLDDDRDRURRDDRLRRRDLLDDLDURUULURULRLULRLLURLUDULDRRDDLRDLRRLRLLULLDDDRDRU
            URUUDUDRDDRDRRRDLLUDRUDRUUUURDRRDUDUULDUDLLUDRRUDLLRDLLULULDRRDDULDRLDLDDULLDDRDDDLRLLDLLRDUUDUURLUDURDRRRRLRRLDRRUULLDLDLRDURULRURULRRDRRDDUUURDURLLDDUUDLRLDURULURRRDRRUUUDRDDLRLRRLLULUDDRRLRRRRLRDRUDDUULULRRURUURURRLRUDLRRUUURUULLULULRRDDULDRRLLLDLUDRRRLLRDLLRLDUDDRRULULUDLURLDRDRRLULLRRDRDLUURLDDURRLDRLURULDLDRDLURRDRLUUDRUULLDRDURLLDLRUDDULLLLDLDDDLURDDUDUDDRLRDDUDDURURLULLRLUDRDDUDDLDRUURLDLUUURDUULRULLDDDURULDDLLD
            LRRLLRURUURRDLURRULDDDLURDUURLLDLRRRRULUUDDLULLDLLRDLUDUULLUDRLLDRULDDURURDUUULRUDRLLRDDDURLRDRRURDDRUDDRRULULLLDLRLULLDLLDRLLLUDLRURLDULRDDRDLDRRDLUUDDLURDLURLUDLRDLDUURLRRUULDLURULUURULLURLDDURRURDRLUULLRRLLLDDDURLURUURLLLLDLLLUDLDLRDULUULRRLUUUUDLURRURRULULULRURDDRRRRDRUDRURDUDDDDUDLURURRDRRDRUDRLDLDDDLURRRURRUDLDURDRLDLDLDDUDURLUDUUDRULLRLLUUDDUURRRUDURDRRUURLUDRRUDLUDDRUUDLULDLLDLRUUDUULLDULRRLDRUDRRDRLUUDDRUDDLLULRLULLDLDUULLDRUUDDUDLLLLDLDDLDLURLDLRUUDDUULLUDUUDRUDLRDDRDLDRUUDUDLLDUURRRLLLLRLLRLLRLUUDULLRLURDLLRUUDRULLULRDRDRRULRDLUDDURRRRURLLRDRLLDRUUULDUDDLRDRD
            DDLRRULRDURDURULLLLRLDDRDDRLLURLRDLULUDURRLUDLDUDRDULDDULURDRURLLDRRLDURRLUULLRUUDUUDLDDLRUUDRRDDRLURDRUDRRRDRUUDDRLLUURLURUDLLRRDRDLUUDLUDURUUDDUULUURLUDLLDDULLUURDDRDLLDRLLDDDRRDLDULLURRLDLRRRLRRURUUDRLURURUULDURUDRRLUDUDLRUDDUDDRLLLULUDULRURDRLUURRRRDLLRDRURRRUURULRUDULDULULUULULLURDUDUDRLDULDRDDULRULDLURLRLDDDDDDULDRURRRRDLLRUDDRDDLUUDUDDRLLRLDLUDRUDULDDDRLLLLURURLDLUUULRRRUDLLULUUULLDLRLDLLRLRDLDULLRLUDDDRDRDDLULUUR
            """))))

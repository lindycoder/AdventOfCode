import sys
import unittest
from textwrap import dedent
from typing import DefaultDict

from hamcrest import assert_that, is_


def compute(data):
    counts = {
        2: 0,
        3: 0
    }

    for line in data.split("\n"):
        index = index_letters(line)
        for sames in counts.keys():
            if has_same(sames, index):
                counts[sames] += 1

    return counts[2] * counts[3]


def compute2(data):
    boxes = [line for line in data.split("\n")]

    for i in range(0, len(boxes)):
        for j in range(0, len(boxes)):
            if i != j:
                different_letter = single_different_letter(boxes[i], boxes[j])
                if different_letter > -1:
                    return boxes[i][:different_letter] + boxes[i][different_letter + 1:]

    return None


def index_letters(string):
    index = DefaultDict(lambda: 0)
    for char in string:
        index[char] += 1

    return index


def has_same(number, index):
    return any(total == number for total in index.values())


class DayTest(unittest.TestCase):
    def test_has_same_2(self):
        assert_that(has_same(2, index_letters("abcdef")), is_(False))
        assert_that(has_same(2, index_letters("bababc")), is_(True))
        assert_that(has_same(2, index_letters("abbcde")), is_(True))
        assert_that(has_same(2, index_letters("abcccd")), is_(False))
        assert_that(has_same(2, index_letters("aabcdd")), is_(True))
        assert_that(has_same(2, index_letters("abcdee")), is_(True))
        assert_that(has_same(2, index_letters("ababab")), is_(False))

    def test_has_same_3(self):
        assert_that(has_same(3, index_letters("abcdef")), is_(False))
        assert_that(has_same(3, index_letters("bababc")), is_(True))
        assert_that(has_same(3, index_letters("abbcde")), is_(False))
        assert_that(has_same(3, index_letters("abcccd")), is_(True))
        assert_that(has_same(3, index_letters("aabcdd")), is_(False))
        assert_that(has_same(3, index_letters("abcdee")), is_(False))
        assert_that(has_same(3, index_letters("ababab")), is_(True))

    def test_checksum(self):
        input = dedent(""" \
            abcdef
            bababc
            abbcde
            abcccd
            aabcdd
            abcdee
            ababab""")
        assert_that(compute(input), is_(12))


def single_different_letter(str1, str2):
    difference_index = -1
    for i in range(0, len(str1)):
        if str1[i] != str2[i]:
            if difference_index != -1:
                return -1
            difference_index = i

    return difference_index


class Day2Test(unittest.TestCase):
    def test_single_different_letter(self):
        assert_that(single_different_letter("abcde", "axcye"), is_(-1))
        assert_that(single_different_letter("fghij", "fguij"), is_(2))

    def test_checksum(self):
        input = dedent(""" \
            abcde
            fghij
            klmno
            pqrst
            fguij
            axcye
            wvxyz""")
        assert_that(compute2(input), is_("fgij"))


puzzle_input = """ \
kqzxdenujwcsthbzgvyioflcsp
vqwxdenujwcsthbmggyioflarp
kqzxienujwcsthbmglyioclarp
kuzxdetujwcsthbmgvyioflcrp
kqnxdenujwcsthbmgvlooflarp
kqzxdknpjwcsthwmgvyioflarp
kgzxdenujwcsthbfgvyicflarp
kqzxdenujrnsthbmgjyioflarp
lqzxdeeujwcsthbmrvyioflarp
iqfxdenujwcsthbmgvyiofyarp
kvzxbenujwcstabmgvyioflarp
kmzxdenujwcsthbmglyioolarp
kqzxdenujhcsthbmgbyioflanp
nqzxdenujwcsehbmgvsioflarp
kqzlgenujwcsthbmgvyiofjarp
kqzxdyfujwcsihbmgvyioflarp
kqzxdsnujwcqthbmgvyiorlarp
kqzxdenuywcsthbmgvyinflmrp
knzxderujwcsthbmgvyioflaop
kqxxdenujwczthbmgvyioflajp
kqzxdevujwcsthbmgvyqoxlarp
kqzxdenujwclmhbmgvyioslarp
kqzldenujwcsthbmgvnisflarp
kjtxdenujwcsthbmgvyfoflarp
kqzxwenujwcstxbmgvyihflarp
kqzxdenuhecsthbmgvyeoflarp
kqzxdenhjwesthbmgvyioklarp
kqkxdenujwcsthbcgvyiofgarp
kqyxmenujwcsthbmgvyioflara
kqzxdqnrjwcwthbmgvyioflarp
kqzxdenufwcgyhbmgvyioflarp
lqzxdenujwcsthbmtvyiofearp
kqzxdenujwcsthbvgvthoflarp
kqzxeenujwcsahbmgvyioflamp
pqzxdenujwcsshbmjvyioflarp
kqzxdesujwcstdbmgvyioflatp
kqzxpenujwcsthimgvyioflhrp
kqzxdmkujwcsthbmgvpioflarp
kszxdenujwcsthbybvyioflarp
kqzxdvnujwcsthbmgvyqoslarp
kkzxdetujwcsthbmgvyiofltrp
kqzxdenujwcsthomgvyiozlaro
cqzfdenubwcsthbmgvyioflarp
kqzxdenyjwcsthbmhvyiofldrp
kqzxdenujwcsthbmghfiofxarp
kmqxdebujwcsthbmgvyioflarp
kqzxdenufwcsthbmvvypoflarp
kqnxdenujwcsthbmgvtzoflarp
bqzxdenujwcithbmgvyiohlarp
kqzxdenurwrsthbmgvyioelarp
kqzxdenujwcsthbmgpyiodlarl
kqzxdengjwcxthbmgvjioflarp
kizxdenujwcsnhqmgvyioflarp
jqzxdenajwcsthbmnvyioflarp
kqzcdenujwcsphbigvyioflarp
kezxdenujwcsthbfgvyioflaqp
kqzxdenujwcstybmgvyivfyarp
kqzxdenujwcsthbmgvbiofsnrp
kqzxdenujwcsthbmgvyhxfnarp
kvzxdenqjfcsthbmgvyioflarp
kqzxywnljwcsthbmgvyioflarp
kqzxdenujwcsbhbzgvyioxlarp
kqkxdenufwcsthbmgvyiofxarp
dqzxddnujwcsthsmgvyioflarp
yqrxdenujwcsthbagvyioflarp
kqzxdenujwcsajbmgvyiovlarp
kqztdunujwcsthbmgvyioilarp
kqzxdequjwcsthbmgvyyoflarm
kqzxdlnujwksthbmgvkioflarp
tqvxdenujwcsthbmgveioflarp
kqzndezupwcsthbmgvyioflarp
kqzctsnujwcsthbmgvyioflarp
kqzxdenujwmstkbmgvyioflgrp
kqzxdenujwzsthdmgvyiofdarp
kqzxdynujwcsthcmgvyioflasp
kqzxdesujwcstybmgcyioflarp
kqzxdenujwcsthbvgvyiyglarp
kqzxpenujwcsthbogvyioflard
khzxdenujwcsthbmgvyikflaep
kqzxdedujwchthbmgvyeoflarp
kxzxsepujwcsthbmgvyioflarp
xqzxdenujwcsthbpgvyioelarp
jfzxdenujwcsthbmgvyiollarp
kqzxcenujwcethbmgvwioflarp
kqzxdenujwcithbmgvysoflarg
kqlxdenujwnsthbmgvyiotlarp
wqzydenujwcsthbmgvyioftarp
kqzxienuwwcsthbmgayioflarp
kqzxdetujwcsthbmgvyhoflawp
kqzxdqnujwrsthbmgvyxoflarp
kqzxdenujwcvthbmgjiioflarp
kqzxdenujwcjthbxgvaioflarp
kqzxpenujwcsthymgvyioklarp
kqzxdenujwcsthbmswygoflarp
kqzxdenujwcsthbmgvyiaxiarp
kqzxdenudkcsthbmgvyzoflarp
kqzxdvndjwcsthbmgvyioflaxp
kqzxdenujwcsthbmdvymoflvrp
kqzxvenujwcsihbmgvyiofllrp
kqzxdqnujwcsthbmgtyioflprp
kqzxdenuuwcathbmgvsioflarp
kqzrdenujwesthbjgvyioflarp
kqzxdexujwcstzbmgvyyoflarp
kqzxpenujwjstabmgvyioflarp
kozxdenejwcsthbmgvpioflarp
kbzxdenvjwcsthbmgvyiofsarp
kolxdenujwcjthbmgvyioflarp
kqzxdenujwcsthbmgvyiffsakp
kqzxdelujwcsthbmlvyioflxrp
kqzxdenugwcsthrmgvyioflprp
kqzxdelujwcsthqmgvyiozlarp
kqzxienujwosthbmgvykoflarp
kqzxdeuujwicthbmgvyioflarp
kqzxdenbjwcsthbmcvyaoflarp
krzxdqnujwcsthbmgvyioflerp
wqzxzenujwcsthbmgvyioclarp
kqzxyenujwcsthbmgejioflarp
kqzxdenujwcstsbmgvtidflarp
kqnxdenejwcsthbmgvyioflara
kqzsdmnujwcsthbmgvyioflaep
kqzxdedujwnsthymgvyioflarp
kqzxdenujwusthbmgnyioflarx
kqzxlenujwcsthbmgayvoflarp
kqzxdenujwcsthbmgvyiofngrh
zqzxdenujwcsthbmgvyiofvxrp
kqzydenujwmsthbmgvyiuflarp
kqzxdenujkrsthbmdvyioflarp
kqzxdlnujocsthbmgvyiofaarp
kqzxdenujwcstybmgvyiofrwrd
kqzxdenupwksthbmgvyiofbarp
khzxdentjwcsthbmbvyioflarp
kqzxdenujwcuphbmgvyihflarp
kqzxdenhjwcgthbmgvyioflrrp
kqzxdenujwcsthbmgvyiofakhp
kqzxdenujwcstfkmgvyioflamp
kqzxdenujqcsthbmgvkiorlarp
kqzxdenujwcstvbmgvyioilasp
kqzxdxnujwcsthbpgayioflarp
kqzxdenupwysthbmgvyiofljrp
kqzxdenujwcdthbmgvymoflarv
kqnxdenujwcstvbmgvyixflarp
kqjxdenujwcsthbmgvyikflurp
kqsxdenulwcsthxmgvyioflarp
bqzxbenujwcsahbmgvyioflarp
vqzxdenujwcsthbmgvjzoflarp
kqzhfenujwcsthimgvyioflarp
eqzxdenujwcshhbmgnyioflarp
kqzxdenujucstubmgvyicflarp
kuzxdenuewcsthbmgvyiofuarp
kqzxdenulwcsthbmgpyigflarp
kqzxdebujwcsthbmgoyioflaro
kqzxdenujwcuthbmgucioflarp
kqzxdenujwcschpmgvyioflhrp
kqzxfenujwcsthbmjvrioflarp
kqzxdenujqcsthbmgvyndflarp
kqzxdgnbjwcsthbmgvywoflarp
kqzxdenujwcsthrmgtbioflarp
yqzxdenyjwcsthbmgvyioflarg
kqzxdenuxwxsthbmsvyioflarp
kqzxdenujwcsthbugqyvoflarp
qqzxdenujwcsahbmgoyioflarp
kqsxdenudwcsthbmguyioflarp
kqzxdenujwcstublgvyioflamp
kqzxdemujwtstqbmgvyioflarp
kqzxqvnajwcsthbmgvyioflarp
kqzxoennjwcstbbmgvyioflarp
kqzxfenujwcsthbmlvyioflwrp
kqzjdunujwcsthhmgvyioflarp
kqzxdenujwcqthbmgvyirfxarp
kqzxdengjwcsthbmgvyiowlgrp
kqgxdenujwcswhbmglyioflarp
mqzxdekuuwcsthbmgvyioflarp
kqzxdenujwdsthbmgbyiovlarp
krzxdenlhwcsthbmgvyioflarp
kqzxdenmjwcstqbmgvyioflanp
kqzxdenujwcmthbmgvtioflyrp
kqzxdenujwcsthbmgvaijflprp
kqzxdenuywysqhbmgvyioflarp
kqzxdenujwfsthbmgvyhoflark
nqzcdefujwcsthbmgvyioflarp
kqzxdenujrcsthgmgyyioflarp
kqzxdqnujwzsthbmgvyioftarp
kqzxdenujwcsthimgvyioolapp
kqzxdenupwcsthbmggyioflyrp
kqzxdjnujwcsthbvgvyioflarf
kqzxdtnujwasthbmgvyiofuarp
kqzxbensjzcsthbmgvyioflarp
kqzxdenujwcsphbmwiyioflarp
kqzgdenuowcsthbmgvyioflarh
kmzxdenujwasthbmgvtioflarp
kqzxdenujwcstybmgvyiofrard
vqzxdenejwcsthbmglyioflarp
kqhxdenujwcsmhbmgvyioflprp
kqzxdnnujwcsthzsgvyioflarp
kczxdenujwcsthbmgvyeoflaop
kqzxdenujwcsxhbmgvaioflaap
kqzxdenujwcsthbmgayiofnprp
kqzxdvnujwcsthbmgvyipjlarp
kqzxdenubwcskhbmgvyiofkarp
kqzxdenujwcsthbgggyigflarp
kqzxdenujncstabvgvyioflarp
kqzxdenujwcstqimqvyioflarp
kqzxeenujwcsdhbmgvyqoflarp
kcpxdenujwcsthbmgvyioilarp
kqwxuenujwcsthbmgvyiyflarp
kqzxdwnujwcstgbmgvyioplarp
kqzxdenuswcstvbmglyioflarp
kqzxdenujwcsthabgvyiwflarp
kqzxdpnujwcsthbmwvyiomlarp
kqzxdenujwcdthbmgvcioffarp
kqzxdenajwcsthbmtvyiofldrp
kqzbnenujwcshhbmgvyioflarp
kqzbdequiwcsthbmgvyioflarp
kqzxdenuswcsohbmgzyioflarp
kvzxdenujwcstdbmjvyioflarp
kqzxoenujwcqthbmpvyioflarp
kqzxhenujwcsthbmgoyiofoarp
klzxdenujwczthbmgvyioflanp
kqpxdenujwcsthbmgvyioflafz
kqkxdenujwcstxbngvyioflarp
kqzepenuxwcsthbmgvyioflarp
bqzxdenujmcithbmgvyioflarp
kdzxdjnujwcstnbmgvyioflarp
kszxdenujwcsthbmgeyiofrarp
kqzxdenijwcsthbmgvhiaflarp
kqzadenujwcbtxbmgvyioflarp
kqkxwenujwcsthbmgvyiowlarp
pqzddenujwcsthbmgvyboflarp
kqzxxenujwcsthbwgvyioflmrp
kqzxdjnujwcsthbmgvyipilarp
pqzxdenujwcsthbmgvyieflark
sqzxdenujtcsthbmgiyioflarp
kqzxdznujwcsthbmgvzioflajp
kqzxdrnujqcsthbmgvyiofvarp
gqzxdenujwcsthemgvlioflarp
kqzxdenujjcsthbmgvuiofljrp
kqzsdenujmcsthbmggyioflarp
kqzxienujwcsthbmgvaioflaip
kqzxdwnujwcstfkmgvyioflarp
kqzqdenujwcithbmzvyioflarp
kqzxdedpjwcsthbmgvyiofbarp
kqzxdeaujwcbtdbmgvyioflarp
kqzewenyjwcsthbmgvyioflarp
kqzxddnujwcsthbmgyyiofrarp
kqzxdtnujwcsthbmgvyiodlard
kqzxdefujwcsthbmgvyiffwarp
xczxdenujwcsthbmgvyooflarp
kuzxdenujucsthbmgvykoflarp
kqzxtenujwcwthbmgvyioplarp
kqzxdencllcsthbmgvyioflarp"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

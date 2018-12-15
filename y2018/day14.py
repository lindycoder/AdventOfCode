import sys
import unittest
from typing import List

from hamcrest import assert_that, is_


def compute(data):
    after = int(data)
    recipes = "37"

    elf1 = 0
    elf2 = 1

    while len(recipes) <= 10 + after:
        recipes, elf1, elf2 = compute_recipes(elf1, elf2, recipes)

    return recipes[after:after + 10]


def compute2(data):
    recipes = list("37")

    elf1 = 0
    elf2 = 1

    while True:
        recipes, elf1, elf2 = compute_recipes_arr(elf1, elf2, recipes)

        if len(recipes) % 10000 == 0:
            if data in "".join(recipes):
                break
            print(elf1, elf2, len(recipes))

    recipes_str = "".join(recipes)
    return len(recipes_str[:recipes_str.index(data)])


def compute_recipes(elf1, elf2, recipes):
    recipes += str(int(recipes[elf1]) + int(recipes[elf2]))
    elf1 = (1 + elf1 + int(recipes[elf1])) % len(recipes)
    elf2 = (1 + elf2 + int(recipes[elf2])) % len(recipes)
    return recipes, elf1, elf2


def compute_recipes_arr(elf1, elf2, recipes: List):
    recipes.extend(str(int(recipes[elf1]) + int(recipes[elf2])))
    elf1 = (1 + elf1 + int(recipes[elf1])) % len(recipes)
    elf2 = (1 + elf2 + int(recipes[elf2])) % len(recipes)
    return recipes, elf1, elf2


class ProvidedTest(unittest.TestCase):
    def test_part_1_1(self):
        assert_that(compute("9"), is_("5158916779"))

    def test_part_1_2(self):
        assert_that(compute("5"), is_("0124515891"))

    def test_part_1_3(self):
        assert_that(compute("18"), is_("9251071085"))

    def test_part_1_4(self):
        assert_that(compute("2018"), is_("5941429882"))

    def test_part_2_1(self):
        assert_that(compute2("51589"), is_(9))

    def test_part_2_2(self):
        assert_that(compute2("01245"), is_(5))

    def test_part_2_3(self):
        assert_that(compute2("92510"), is_(18))

    def test_part_2_4(self):
        assert_that(compute2("59414"), is_(2018))


puzzle_input = "846601"

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

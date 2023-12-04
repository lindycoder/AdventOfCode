import re
import sys
from pathlib import Path
from textwrap import dedent
from types import MappingProxyType

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int:
    lines = data.strip().splitlines()
    return sum(int(a + b) for a, b in map(extract_values, lines))


def compute2(data):
    lines = data.strip().splitlines()
    return sum(int(a + b) for a, b in map(extract_full_values, lines))


DIGITS = frozenset(str(i) for i in range(10))


def extract_values(line: str) -> tuple[str, str]:
    only_digits = list(filter(lambda e: e in DIGITS, line))
    return only_digits[0], only_digits[-1]


LITERAL_DIGITS = MappingProxyType(
    {
        **{d: d for d in DIGITS},
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
)

ANY_DIGIT = "|".join(LITERAL_DIGITS.keys())
FIRST_DIGIT_RE = re.compile(rf".*?({ANY_DIGIT}).*")
LAST_DIGIT_RE = re.compile(rf".*({ANY_DIGIT}).*?")


def extract_full_values(line: str) -> tuple[str, str]:
    first = FIRST_DIGIT_RE.match(line).group(1)
    last = LAST_DIGIT_RE.match(line).group(1)

    return LITERAL_DIGITS[first], LITERAL_DIGITS[last]


@pytest.mark.parametrize(
    "val,expect",
    [
        ("1abc2", ("1", "2")),
        ("pqr3stu8vwx", ("3", "8")),
        ("a1b2c3d4e5f", ("1", "5")),
        ("treb7uchet", ("7", "7")),
    ],
)
def test_extract_values(val, expect):
    assert_that(extract_values(val), is_(expect))


@pytest.mark.parametrize(
    "val,expect",
    [
        ("1abc2", ("1", "2")),
        ("pqr3stu8vwx", ("3", "8")),
        ("a1b2c3d4e5f", ("1", "5")),
        ("treb7uchet", ("7", "7")),
        ("two1nine", ("2", "9")),
        ("eightwothree", ("8", "3")),
        ("eighthree", ("8", "3")),
        ("abcone2threexyz", ("1", "3")),
        ("xtwone3four", ("2", "4")),
        ("4nineeightseven2", ("4", "2")),
        ("zoneight234", ("1", "4")),
        ("z234oneight", ("2", "8")),
        ("znineight234", ("9", "4")),
        ("7pqrstsixteen", ("7", "6")),
    ],
)
def test_extract_full_values(val, expect):
    assert_that(extract_full_values(val), is_(expect))


@pytest.mark.parametrize(
    "val,expect",
    [
        (
            dedent(
                """\
                1abc2
                pqr3stu8vwx
                a1b2c3d4e5f
                treb7uchet    
                """
            ),
            142,
        ),
        (puzzle_input, 54450),
    ],
)
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize(
    "val,expect",
    [
        (
            dedent(
                """\
                two1nine
                eightwothree
                abcone2threexyz
                xtwone3four
                4nineeightseven2
                zoneight234
                7pqrstsixteen                
                """
            ),
            281,
        )
    ],
)
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


if __name__ == "__main__":
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

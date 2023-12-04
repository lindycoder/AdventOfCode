import sys
from pathlib import Path
from textwrap import dedent

import pytest
from hamcrest import assert_that, is_

puzzle_input = Path(__file__.replace(".py", ".txt")).read_text()


def compute(data: str) -> int | str:
    lines = data.strip().splitlines()
    return 0


def compute2(data: str) -> int | str:
    lines = data.strip().splitlines()
    return 0


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            dedent(
                """\
                """
            ),
            0,
        ),
    ],
)
def test_compute(val: str, expect: int | str):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize(
    ("val", "expect"),
    [
        (
            dedent(
                """\
                """
            ),
            0,
        )
    ],
)
def test_compute2(val: str, expect: int | str):
    assert_that(compute2(val), is_(expect))


if __name__ == "__main__":
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

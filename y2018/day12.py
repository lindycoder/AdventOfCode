import re
import sys
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_


def compute(data):
    return compute_generations(data, 20)



def compute2(data):
    return compute_generations(data, 180)


def compute_generations(data, generations):
    check_up = int(generations / 10000000) or 1
    state, mutations = parse(data)
    origin_index = 0
    for gen in range(0, generations):

        while not state.startswith("...."):
            state = "." + state
            origin_index += 1

        while not state.endswith("...."):
            state += "."

        new_state = []
        for i in range(2, len(state) - 2):
            context = state[i - 2:i + 3]
            try:
                new_state.append(mutations[context])
            except KeyError:
                new_state.append(".")

        print(gen,state, origin_index)

        state = f"..{''.join(new_state)}.."


    return sum(i - origin_index for i, plant in enumerate(state) if plant == "#")

def parse(data):
    lines = data.split("\n")
    state_line = lines.pop(0)
    state = re.match("initial state: (.*)", state_line).group(1)

    lines.pop(0)

    mutations = {}
    for line in lines:
        context, new_state = line.split(" => ")
        # if context[2] != new_state:
        mutations[context] = new_state

    return state, mutations


class ParseTest(unittest.TestCase):
    def test_parse(self):
        input = dedent("""\
            initial state: #..#.#..##......###...###
            
            ...## => #
            ..#.. => #
            .#... => #
            .#.#. => #
            .#.## => #
            .##.. => #
            .#### => #
            #.#.# => #
            #.### => #
            ##.#. => #
            ##.## => #
            ###.. => #
            ###.# => #
            ####. => #""")

        state, mutations = parse(input)
        assert_that(state, is_("#..#.#..##......###...###"))
        assert_that(mutations, is_({
            "...##": "#",
            "..#..": "#",
            ".#...": "#",
            ".#.#.": "#",
            ".#.##": "#",
            ".##..": "#",
            ".####": "#",
            "#.#.#": "#",
            "#.###": "#",
            "##.#.": "#",
            "##.##": "#",
            "###..": "#",
            "###.#": "#",
            "####.": "#",
        }))


class ProvidedTest(unittest.TestCase):
    input = dedent("""\
        initial state: #..#.#..##......###...###
        
        ...## => #
        ..#.. => #
        .#... => #
        .#.#. => #
        .#.## => #
        .##.. => #
        .#### => #
        #.#.# => #
        #.### => #
        ##.#. => #
        ##.## => #
        ###.. => #
        ###.# => #
        ####. => #""")

    def test_part_1(self):
        assert_that(compute(self.input), is_(325))


puzzle_input = """\
initial state: #......##...#.#.###.#.##..##.#.....##....#.#.##.##.#..#.##........####.###.###.##..#....#...###.##

.#.## => .
.#### => .
#..#. => .
##.## => #
..##. => #
##... => #
..#.. => #
#.##. => .
##.#. => .
.###. => #
.#.#. => #
#..## => #
.##.# => #
#.### => #
.##.. => #
###.# => .
#.#.# => #
#.... => .
#...# => .
.#... => #
##..# => .
....# => .
..... => .
.#..# => #
##### => .
#.#.. => .
..#.# => #
...## => .
...#. => #
..### => .
####. => #
###.. => #"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

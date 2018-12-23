import re
import sys
import unittest
from dataclasses import dataclass
from textwrap import dedent
from typing import List, DefaultDict

from hamcrest import assert_that, is_

operations = {
    "addr": lambda registry, a, b, c: registry.set(c, registry[a] + registry[b]),
    "addi": lambda registry, a, b, c: registry.set(c, registry[a] + b),
    "mulr": lambda registry, a, b, c: registry.set(c, registry[a] * registry[b]),
    "muli": lambda registry, a, b, c: registry.set(c, registry[a] * b),
    "banr": lambda registry, a, b, c: registry.set(c, registry[a] & registry[b]),
    "bani": lambda registry, a, b, c: registry.set(c, registry[a] & b),
    "borr": lambda registry, a, b, c: registry.set(c, registry[a] | registry[b]),
    "bori": lambda registry, a, b, c: registry.set(c, registry[a] | b),
    "setr": lambda registry, a, b, c: registry.set(c, registry[a]),
    "seti": lambda registry, a, b, c: registry.set(c, a),
    "gtir": lambda registry, a, b, c: registry.set(c, 1 if a > registry[b] else 0),
    "gtri": lambda registry, a, b, c: registry.set(c, 1 if registry[a] > b else 0),
    "gtrr": lambda registry, a, b, c: registry.set(c, 1 if registry[a] > registry[b] else 0),
    "eqir": lambda registry, a, b, c: registry.set(c, 1 if a == registry[b] else 0),
    "eqri": lambda registry, a, b, c: registry.set(c, 1 if registry[a] == b else 0),
    "eqrr": lambda registry, a, b, c: registry.set(c, 1 if registry[a] == registry[b] else 0)
}


def compute(data):
    samples = parse(data)

    tested = [(sample, possible_opcodes(sample)) for sample in samples]

    return len(list(filter(lambda tests: len(tests[1]) >= 3, tested)))


def compute2(data):
    samples = parse(data)

    mapping = DefaultDict(lambda: set())
    for sample in samples:
        opcode = sample.command[0]
        mapping[opcode] = mapping[opcode].union(possible_opcodes(sample))

    fixed = {}
    while len(mapping) > 0:
        for opcode, possibilities in sorted(mapping.items()):
            if len(possibilities) == 1:
                operation = possibilities.pop()
                print("FIXED:", opcode, "is", operation)
                fixed[opcode] = operation

                mapping.pop(opcode)
                for o, p in mapping.items():
                    try:
                        p.remove(operation)
                    except KeyError:
                        pass
                break
        else:
            print(mapping)
            raise Exception("i'm stuck")

    program = [list(map(int, line.split(" "))) for line in input2.split("\n")]

    registry = Registry([0, 0, 0, 0])

    for line in program:
        opcode = line[0]
        args = line[1:]
        operations[fixed[opcode]](registry, *args)

    print(registry)
    return registry[0]


def parse(input):
    samples = []
    state_regex = re.compile(".*\[(.*)\]")
    for sample in input.split("\n\n"):
        before, command, after = sample.split("\n")
        samples.append(Sample(command=list(map(int, command.split(" "))),
                              before=list(map(int, state_regex.match(before).group(1).split(", "))),
                              after=list(map(int, state_regex.match(after).group(1).split(", ")))))

    return samples


@dataclass
class Sample:
    command: List[int]
    before: List[int]
    after: List[int]


class Registry(dict):
    def __init__(self, values) -> None:
        super().__init__({i: value for i, value in enumerate(values)})

    def set(self, registry, value):
        self[registry] = value

    def to_list(self):
        return [self[i] for i in range(0, len(self))]


class ParseTest(unittest.TestCase):
    def test_parse_samples(self):
        input = dedent("""\
            Before: [2, 1, 1, 0]
            10 1 3 1
            After:  [2, 1, 1, 0]
            
            Before: [1, 1, 3, 3]
            6 1 0 0
            After:  [1, 1, 3, 3]""")

        sample1, sample2 = parse(input)

        assert_that(sample1, is_(Sample(command=[10, 1, 3, 1],
                                        before=[2, 1, 1, 0],
                                        after=[2, 1, 1, 0])))

        assert_that(sample2, is_(Sample(command=[6, 1, 0, 0],
                                        before=[1, 1, 3, 3],
                                        after=[1, 1, 3, 3])))


def possible_opcodes(sample):
    possibilities = set()
    for name, operation in operations.items():
        registry = Registry(sample.before)
        operation(registry, *sample.command[1:])
        if registry.to_list() == sample.after:
            possibilities.add(name)

    return possibilities


class ProvidedTest(unittest.TestCase):
    def test_possible_opcodes(self):
        sample = Sample(command=[9, 2, 1, 2],
                        before=[3, 2, 1, 1],
                        after=[3, 2, 2, 1])

        assert_that(possible_opcodes(sample), is_({"mulr", "addi", "seti"}))

    def test_compute(self):
        input = dedent("""\
            Before: [3, 2, 1, 1]
            9 2 1 2
            After:  [3, 2, 2, 1]""")

        assert_that(compute(input), is_(1))


puzzle_input = """\
Before: [2, 1, 1, 0]
10 1 3 1
After:  [2, 1, 1, 0]

Before: [1, 1, 3, 3]
6 1 0 0
After:  [1, 1, 3, 3]

Before: [2, 1, 2, 2]
14 1 3 0
After:  [0, 1, 2, 2]

Before: [1, 2, 2, 3]
1 0 2 2
After:  [1, 2, 0, 3]

Before: [2, 2, 3, 2]
12 0 2 3
After:  [2, 2, 3, 2]

Before: [1, 1, 0, 1]
13 3 3 2
After:  [1, 1, 0, 1]

Before: [1, 1, 2, 1]
15 3 2 3
After:  [1, 1, 2, 1]

Before: [2, 1, 1, 0]
8 2 1 2
After:  [2, 1, 0, 0]

Before: [1, 1, 1, 2]
8 2 1 3
After:  [1, 1, 1, 0]

Before: [0, 3, 1, 1]
0 0 0 2
After:  [0, 3, 0, 1]

Before: [1, 1, 1, 1]
6 1 0 2
After:  [1, 1, 1, 1]

Before: [3, 1, 2, 0]
10 1 3 1
After:  [3, 1, 2, 0]

Before: [1, 2, 2, 1]
1 0 2 2
After:  [1, 2, 0, 1]

Before: [2, 1, 3, 3]
12 0 2 3
After:  [2, 1, 3, 2]

Before: [0, 1, 1, 3]
7 2 3 1
After:  [0, 0, 1, 3]

Before: [1, 1, 2, 3]
2 1 2 2
After:  [1, 1, 0, 3]

Before: [3, 1, 3, 2]
14 1 3 2
After:  [3, 1, 0, 2]

Before: [1, 1, 1, 0]
6 1 0 2
After:  [1, 1, 1, 0]

Before: [1, 3, 0, 3]
9 0 2 0
After:  [0, 3, 0, 3]

Before: [0, 3, 2, 0]
3 2 1 1
After:  [0, 1, 2, 0]

Before: [3, 1, 2, 0]
2 1 2 3
After:  [3, 1, 2, 0]

Before: [0, 3, 0, 0]
0 0 0 3
After:  [0, 3, 0, 0]

Before: [2, 1, 2, 3]
2 1 2 3
After:  [2, 1, 2, 0]

Before: [1, 1, 3, 1]
6 1 0 2
After:  [1, 1, 1, 1]

Before: [0, 1, 2, 1]
15 3 2 3
After:  [0, 1, 2, 1]

Before: [1, 1, 2, 2]
2 1 2 2
After:  [1, 1, 0, 2]

Before: [1, 2, 2, 0]
1 0 2 1
After:  [1, 0, 2, 0]

Before: [1, 1, 0, 2]
6 1 0 2
After:  [1, 1, 1, 2]

Before: [2, 2, 3, 2]
12 3 2 0
After:  [2, 2, 3, 2]

Before: [1, 0, 2, 2]
11 2 2 2
After:  [1, 0, 2, 2]

Before: [2, 2, 0, 3]
7 1 3 3
After:  [2, 2, 0, 0]

Before: [1, 1, 3, 1]
6 1 0 0
After:  [1, 1, 3, 1]

Before: [2, 1, 2, 1]
9 1 3 1
After:  [2, 1, 2, 1]

Before: [2, 1, 1, 0]
4 0 1 3
After:  [2, 1, 1, 1]

Before: [2, 0, 0, 3]
8 0 1 1
After:  [2, 1, 0, 3]

Before: [0, 1, 2, 2]
14 1 3 2
After:  [0, 1, 0, 2]

Before: [2, 1, 3, 2]
12 3 2 1
After:  [2, 2, 3, 2]

Before: [1, 1, 0, 1]
6 1 0 3
After:  [1, 1, 0, 1]

Before: [0, 0, 2, 0]
0 0 0 0
After:  [0, 0, 2, 0]

Before: [1, 1, 2, 1]
1 0 2 2
After:  [1, 1, 0, 1]

Before: [0, 2, 2, 1]
0 0 0 1
After:  [0, 0, 2, 1]

Before: [3, 2, 0, 3]
8 0 2 3
After:  [3, 2, 0, 1]

Before: [3, 1, 2, 1]
2 1 2 1
After:  [3, 0, 2, 1]

Before: [3, 1, 0, 2]
14 1 3 0
After:  [0, 1, 0, 2]

Before: [3, 2, 2, 0]
11 2 2 3
After:  [3, 2, 2, 2]

Before: [0, 2, 2, 2]
0 0 0 2
After:  [0, 2, 0, 2]

Before: [1, 3, 2, 3]
11 2 2 3
After:  [1, 3, 2, 2]

Before: [2, 0, 2, 1]
15 3 2 3
After:  [2, 0, 2, 1]

Before: [0, 3, 0, 3]
0 0 0 2
After:  [0, 3, 0, 3]

Before: [1, 1, 2, 2]
1 0 2 0
After:  [0, 1, 2, 2]

Before: [1, 2, 3, 2]
12 1 2 3
After:  [1, 2, 3, 2]

Before: [3, 1, 1, 3]
5 3 0 2
After:  [3, 1, 1, 3]

Before: [0, 1, 1, 2]
0 0 0 2
After:  [0, 1, 0, 2]

Before: [0, 1, 2, 1]
9 1 3 3
After:  [0, 1, 2, 1]

Before: [0, 1, 2, 3]
2 1 2 3
After:  [0, 1, 2, 0]

Before: [3, 1, 2, 2]
14 1 3 2
After:  [3, 1, 0, 2]

Before: [2, 3, 3, 0]
3 0 1 3
After:  [2, 3, 3, 1]

Before: [3, 3, 2, 3]
5 3 0 1
After:  [3, 1, 2, 3]

Before: [2, 1, 2, 1]
13 3 3 3
After:  [2, 1, 2, 0]

Before: [1, 1, 2, 1]
8 3 1 3
After:  [1, 1, 2, 0]

Before: [1, 2, 0, 0]
9 0 2 0
After:  [0, 2, 0, 0]

Before: [2, 1, 1, 0]
10 1 3 3
After:  [2, 1, 1, 1]

Before: [3, 1, 1, 2]
14 1 3 3
After:  [3, 1, 1, 0]

Before: [1, 2, 3, 2]
12 3 2 3
After:  [1, 2, 3, 2]

Before: [3, 1, 1, 3]
7 2 3 2
After:  [3, 1, 0, 3]

Before: [1, 2, 0, 0]
9 0 2 1
After:  [1, 0, 0, 0]

Before: [1, 2, 3, 3]
12 1 2 2
After:  [1, 2, 2, 3]

Before: [1, 1, 2, 2]
11 2 2 0
After:  [2, 1, 2, 2]

Before: [1, 1, 0, 1]
6 1 0 2
After:  [1, 1, 1, 1]

Before: [1, 1, 1, 1]
6 1 0 0
After:  [1, 1, 1, 1]

Before: [3, 1, 1, 3]
5 3 0 0
After:  [1, 1, 1, 3]

Before: [2, 1, 1, 3]
4 0 1 0
After:  [1, 1, 1, 3]

Before: [2, 1, 2, 2]
14 1 3 2
After:  [2, 1, 0, 2]

Before: [0, 1, 3, 1]
9 1 3 3
After:  [0, 1, 3, 1]

Before: [2, 1, 1, 1]
9 1 3 2
After:  [2, 1, 1, 1]

Before: [1, 1, 3, 3]
6 1 0 2
After:  [1, 1, 1, 3]

Before: [1, 3, 2, 1]
15 3 2 2
After:  [1, 3, 1, 1]

Before: [2, 3, 2, 1]
15 3 2 1
After:  [2, 1, 2, 1]

Before: [3, 2, 3, 3]
12 1 2 3
After:  [3, 2, 3, 2]

Before: [0, 1, 3, 0]
10 1 3 2
After:  [0, 1, 1, 0]

Before: [0, 0, 3, 2]
0 0 0 3
After:  [0, 0, 3, 0]

Before: [0, 1, 0, 1]
13 3 3 1
After:  [0, 0, 0, 1]

Before: [0, 0, 2, 3]
7 2 3 0
After:  [0, 0, 2, 3]

Before: [2, 2, 3, 0]
12 0 2 3
After:  [2, 2, 3, 2]

Before: [0, 1, 2, 1]
9 1 3 0
After:  [1, 1, 2, 1]

Before: [3, 0, 2, 0]
4 0 2 1
After:  [3, 1, 2, 0]

Before: [3, 3, 2, 1]
4 0 2 0
After:  [1, 3, 2, 1]

Before: [2, 1, 1, 2]
4 0 1 2
After:  [2, 1, 1, 2]

Before: [2, 1, 3, 2]
14 1 3 3
After:  [2, 1, 3, 0]

Before: [0, 2, 2, 1]
15 3 2 2
After:  [0, 2, 1, 1]

Before: [2, 1, 3, 1]
5 2 3 3
After:  [2, 1, 3, 0]

Before: [3, 1, 0, 1]
9 1 3 1
After:  [3, 1, 0, 1]

Before: [2, 1, 2, 2]
14 1 3 1
After:  [2, 0, 2, 2]

Before: [0, 1, 0, 0]
10 1 3 2
After:  [0, 1, 1, 0]

Before: [1, 1, 2, 1]
6 1 0 0
After:  [1, 1, 2, 1]

Before: [1, 0, 0, 1]
9 0 2 0
After:  [0, 0, 0, 1]

Before: [1, 1, 2, 1]
13 3 3 0
After:  [0, 1, 2, 1]

Before: [3, 1, 1, 1]
9 1 3 2
After:  [3, 1, 1, 1]

Before: [0, 1, 1, 1]
9 1 3 2
After:  [0, 1, 1, 1]

Before: [2, 0, 0, 2]
8 0 1 3
After:  [2, 0, 0, 1]

Before: [1, 0, 2, 2]
1 0 2 1
After:  [1, 0, 2, 2]

Before: [1, 1, 2, 2]
2 1 2 1
After:  [1, 0, 2, 2]

Before: [3, 3, 2, 3]
5 3 0 3
After:  [3, 3, 2, 1]

Before: [3, 1, 0, 2]
14 1 3 1
After:  [3, 0, 0, 2]

Before: [2, 1, 3, 3]
8 2 0 2
After:  [2, 1, 1, 3]

Before: [0, 1, 2, 0]
10 1 3 2
After:  [0, 1, 1, 0]

Before: [3, 2, 2, 1]
15 3 2 3
After:  [3, 2, 2, 1]

Before: [2, 0, 1, 2]
8 0 1 0
After:  [1, 0, 1, 2]

Before: [2, 3, 0, 1]
13 3 3 1
After:  [2, 0, 0, 1]

Before: [2, 1, 3, 1]
5 2 3 2
After:  [2, 1, 0, 1]

Before: [0, 1, 2, 1]
2 1 2 2
After:  [0, 1, 0, 1]

Before: [2, 1, 2, 2]
2 1 2 0
After:  [0, 1, 2, 2]

Before: [3, 1, 1, 0]
10 1 3 0
After:  [1, 1, 1, 0]

Before: [2, 1, 1, 2]
4 0 1 3
After:  [2, 1, 1, 1]

Before: [2, 1, 0, 2]
14 1 3 3
After:  [2, 1, 0, 0]

Before: [2, 1, 0, 3]
7 1 3 2
After:  [2, 1, 0, 3]

Before: [1, 3, 1, 1]
13 2 3 1
After:  [1, 0, 1, 1]

Before: [0, 2, 2, 1]
15 3 2 1
After:  [0, 1, 2, 1]

Before: [0, 3, 1, 1]
13 2 3 3
After:  [0, 3, 1, 0]

Before: [0, 2, 3, 2]
12 3 2 3
After:  [0, 2, 3, 2]

Before: [1, 3, 2, 0]
1 0 2 2
After:  [1, 3, 0, 0]

Before: [2, 0, 2, 2]
11 2 2 3
After:  [2, 0, 2, 2]

Before: [1, 0, 0, 2]
9 0 2 2
After:  [1, 0, 0, 2]

Before: [1, 1, 2, 1]
2 1 2 1
After:  [1, 0, 2, 1]

Before: [3, 2, 2, 2]
3 2 0 0
After:  [1, 2, 2, 2]

Before: [1, 1, 3, 2]
6 1 0 1
After:  [1, 1, 3, 2]

Before: [1, 1, 2, 0]
6 1 0 0
After:  [1, 1, 2, 0]

Before: [1, 1, 0, 2]
13 3 3 3
After:  [1, 1, 0, 0]

Before: [0, 3, 1, 1]
13 2 3 0
After:  [0, 3, 1, 1]

Before: [0, 2, 3, 1]
0 0 0 1
After:  [0, 0, 3, 1]

Before: [0, 1, 2, 0]
10 1 3 3
After:  [0, 1, 2, 1]

Before: [1, 2, 2, 2]
5 2 1 0
After:  [1, 2, 2, 2]

Before: [1, 1, 0, 2]
6 1 0 1
After:  [1, 1, 0, 2]

Before: [1, 0, 1, 3]
7 2 3 1
After:  [1, 0, 1, 3]

Before: [0, 2, 2, 2]
5 2 1 0
After:  [1, 2, 2, 2]

Before: [2, 0, 3, 2]
12 3 2 1
After:  [2, 2, 3, 2]

Before: [1, 1, 0, 2]
14 1 3 1
After:  [1, 0, 0, 2]

Before: [2, 3, 3, 1]
3 0 1 3
After:  [2, 3, 3, 1]

Before: [3, 0, 2, 1]
15 3 2 2
After:  [3, 0, 1, 1]

Before: [3, 1, 2, 2]
14 1 3 3
After:  [3, 1, 2, 0]

Before: [1, 0, 2, 3]
1 0 2 3
After:  [1, 0, 2, 0]

Before: [0, 2, 0, 1]
0 0 0 1
After:  [0, 0, 0, 1]

Before: [3, 1, 0, 1]
9 1 3 3
After:  [3, 1, 0, 1]

Before: [1, 1, 3, 2]
14 1 3 1
After:  [1, 0, 3, 2]

Before: [2, 1, 1, 0]
4 0 1 1
After:  [2, 1, 1, 0]

Before: [2, 1, 1, 1]
8 3 1 3
After:  [2, 1, 1, 0]

Before: [0, 1, 1, 0]
10 1 3 2
After:  [0, 1, 1, 0]

Before: [1, 0, 2, 1]
1 0 2 2
After:  [1, 0, 0, 1]

Before: [1, 2, 2, 3]
11 2 2 1
After:  [1, 2, 2, 3]

Before: [3, 1, 2, 0]
4 0 2 1
After:  [3, 1, 2, 0]

Before: [0, 0, 1, 0]
0 0 0 0
After:  [0, 0, 1, 0]

Before: [0, 2, 3, 3]
7 1 3 3
After:  [0, 2, 3, 0]

Before: [3, 1, 2, 1]
15 3 2 3
After:  [3, 1, 2, 1]

Before: [3, 1, 3, 3]
7 1 3 2
After:  [3, 1, 0, 3]

Before: [1, 1, 2, 0]
10 1 3 3
After:  [1, 1, 2, 1]

Before: [2, 1, 2, 1]
2 1 2 1
After:  [2, 0, 2, 1]

Before: [1, 1, 1, 1]
13 3 3 3
After:  [1, 1, 1, 0]

Before: [2, 1, 3, 1]
4 0 1 0
After:  [1, 1, 3, 1]

Before: [1, 1, 1, 1]
8 2 1 3
After:  [1, 1, 1, 0]

Before: [1, 1, 1, 3]
7 2 3 2
After:  [1, 1, 0, 3]

Before: [3, 2, 2, 2]
13 3 3 0
After:  [0, 2, 2, 2]

Before: [1, 3, 3, 2]
13 3 3 0
After:  [0, 3, 3, 2]

Before: [0, 3, 2, 1]
15 3 2 2
After:  [0, 3, 1, 1]

Before: [1, 2, 2, 2]
1 0 2 3
After:  [1, 2, 2, 0]

Before: [3, 1, 2, 1]
4 0 2 3
After:  [3, 1, 2, 1]

Before: [1, 1, 2, 1]
2 1 2 3
After:  [1, 1, 2, 0]

Before: [0, 1, 2, 0]
2 1 2 0
After:  [0, 1, 2, 0]

Before: [1, 1, 2, 3]
2 1 2 3
After:  [1, 1, 2, 0]

Before: [1, 1, 1, 2]
6 1 0 1
After:  [1, 1, 1, 2]

Before: [2, 3, 3, 3]
3 0 1 0
After:  [1, 3, 3, 3]

Before: [3, 2, 2, 0]
4 0 2 1
After:  [3, 1, 2, 0]

Before: [3, 1, 3, 3]
7 1 3 0
After:  [0, 1, 3, 3]

Before: [2, 3, 3, 1]
3 0 1 0
After:  [1, 3, 3, 1]

Before: [0, 1, 3, 0]
10 1 3 3
After:  [0, 1, 3, 1]

Before: [3, 1, 1, 0]
10 1 3 2
After:  [3, 1, 1, 0]

Before: [2, 2, 2, 0]
5 2 1 2
After:  [2, 2, 1, 0]

Before: [1, 1, 0, 0]
9 0 2 2
After:  [1, 1, 0, 0]

Before: [2, 3, 3, 0]
3 0 1 1
After:  [2, 1, 3, 0]

Before: [2, 1, 3, 2]
14 1 3 0
After:  [0, 1, 3, 2]

Before: [0, 1, 2, 2]
0 0 0 0
After:  [0, 1, 2, 2]

Before: [2, 0, 3, 0]
12 0 2 0
After:  [2, 0, 3, 0]

Before: [1, 1, 0, 0]
10 1 3 2
After:  [1, 1, 1, 0]

Before: [1, 1, 1, 2]
14 1 3 1
After:  [1, 0, 1, 2]

Before: [2, 1, 2, 3]
2 1 2 1
After:  [2, 0, 2, 3]

Before: [2, 3, 1, 0]
3 0 1 0
After:  [1, 3, 1, 0]

Before: [0, 3, 1, 3]
7 2 3 2
After:  [0, 3, 0, 3]

Before: [0, 1, 2, 1]
15 3 2 0
After:  [1, 1, 2, 1]

Before: [3, 3, 2, 2]
11 2 2 2
After:  [3, 3, 2, 2]

Before: [0, 1, 3, 1]
0 0 0 2
After:  [0, 1, 0, 1]

Before: [3, 2, 0, 3]
5 3 0 1
After:  [3, 1, 0, 3]

Before: [0, 3, 2, 2]
3 2 1 0
After:  [1, 3, 2, 2]

Before: [1, 1, 3, 1]
6 1 0 1
After:  [1, 1, 3, 1]

Before: [2, 2, 2, 1]
15 3 2 1
After:  [2, 1, 2, 1]

Before: [1, 1, 2, 0]
10 1 3 0
After:  [1, 1, 2, 0]

Before: [1, 1, 1, 3]
6 1 0 2
After:  [1, 1, 1, 3]

Before: [2, 0, 3, 3]
8 0 1 3
After:  [2, 0, 3, 1]

Before: [3, 1, 3, 2]
13 3 3 3
After:  [3, 1, 3, 0]

Before: [3, 2, 2, 2]
4 0 2 2
After:  [3, 2, 1, 2]

Before: [1, 1, 1, 0]
8 2 1 2
After:  [1, 1, 0, 0]

Before: [1, 0, 2, 1]
1 0 2 0
After:  [0, 0, 2, 1]

Before: [2, 3, 2, 1]
13 3 3 0
After:  [0, 3, 2, 1]

Before: [3, 0, 2, 3]
4 0 2 2
After:  [3, 0, 1, 3]

Before: [2, 1, 0, 1]
9 1 3 0
After:  [1, 1, 0, 1]

Before: [3, 2, 2, 1]
15 3 2 2
After:  [3, 2, 1, 1]

Before: [3, 1, 2, 1]
2 1 2 3
After:  [3, 1, 2, 0]

Before: [1, 1, 0, 0]
6 1 0 0
After:  [1, 1, 0, 0]

Before: [1, 0, 3, 2]
13 3 3 0
After:  [0, 0, 3, 2]

Before: [0, 2, 2, 2]
5 2 1 3
After:  [0, 2, 2, 1]

Before: [2, 3, 3, 2]
12 0 2 3
After:  [2, 3, 3, 2]

Before: [0, 2, 1, 1]
0 0 0 0
After:  [0, 2, 1, 1]

Before: [3, 0, 2, 1]
11 2 2 3
After:  [3, 0, 2, 2]

Before: [3, 2, 2, 1]
4 0 2 3
After:  [3, 2, 2, 1]

Before: [3, 1, 0, 3]
7 1 3 2
After:  [3, 1, 0, 3]

Before: [1, 1, 2, 1]
9 1 3 0
After:  [1, 1, 2, 1]

Before: [0, 0, 1, 3]
7 2 3 0
After:  [0, 0, 1, 3]

Before: [0, 1, 3, 1]
8 3 1 3
After:  [0, 1, 3, 0]

Before: [2, 1, 1, 1]
4 0 1 2
After:  [2, 1, 1, 1]

Before: [1, 1, 0, 0]
10 1 3 0
After:  [1, 1, 0, 0]

Before: [0, 1, 3, 2]
13 3 3 3
After:  [0, 1, 3, 0]

Before: [1, 1, 2, 0]
1 0 2 0
After:  [0, 1, 2, 0]

Before: [3, 1, 2, 0]
2 1 2 1
After:  [3, 0, 2, 0]

Before: [0, 1, 1, 3]
7 2 3 3
After:  [0, 1, 1, 0]

Before: [0, 2, 3, 3]
12 1 2 0
After:  [2, 2, 3, 3]

Before: [2, 1, 1, 1]
8 3 1 0
After:  [0, 1, 1, 1]

Before: [0, 1, 1, 2]
14 1 3 2
After:  [0, 1, 0, 2]

Before: [3, 1, 2, 1]
9 1 3 1
After:  [3, 1, 2, 1]

Before: [1, 2, 3, 2]
12 1 2 2
After:  [1, 2, 2, 2]

Before: [2, 3, 2, 2]
3 0 1 0
After:  [1, 3, 2, 2]

Before: [1, 1, 1, 0]
10 1 3 0
After:  [1, 1, 1, 0]

Before: [3, 2, 2, 2]
4 0 2 0
After:  [1, 2, 2, 2]

Before: [3, 1, 0, 2]
14 1 3 3
After:  [3, 1, 0, 0]

Before: [0, 3, 3, 2]
12 3 2 3
After:  [0, 3, 3, 2]

Before: [3, 3, 0, 0]
8 0 2 1
After:  [3, 1, 0, 0]

Before: [3, 0, 2, 0]
4 0 2 3
After:  [3, 0, 2, 1]

Before: [0, 3, 2, 1]
3 2 1 1
After:  [0, 1, 2, 1]

Before: [3, 0, 2, 3]
4 0 2 0
After:  [1, 0, 2, 3]

Before: [0, 1, 0, 0]
10 1 3 1
After:  [0, 1, 0, 0]

Before: [3, 3, 3, 3]
5 3 2 1
After:  [3, 1, 3, 3]

Before: [1, 2, 2, 0]
1 0 2 2
After:  [1, 2, 0, 0]

Before: [0, 3, 1, 2]
0 0 0 1
After:  [0, 0, 1, 2]

Before: [0, 3, 2, 3]
3 2 1 1
After:  [0, 1, 2, 3]

Before: [3, 1, 3, 2]
14 1 3 0
After:  [0, 1, 3, 2]

Before: [3, 1, 1, 3]
7 1 3 3
After:  [3, 1, 1, 0]

Before: [2, 2, 2, 2]
13 3 3 0
After:  [0, 2, 2, 2]

Before: [1, 1, 3, 3]
6 1 0 1
After:  [1, 1, 3, 3]

Before: [1, 1, 2, 0]
6 1 0 3
After:  [1, 1, 2, 1]

Before: [3, 3, 2, 1]
3 2 0 1
After:  [3, 1, 2, 1]

Before: [1, 1, 2, 3]
2 1 2 0
After:  [0, 1, 2, 3]

Before: [0, 3, 3, 1]
13 3 3 1
After:  [0, 0, 3, 1]

Before: [1, 2, 2, 0]
1 0 2 3
After:  [1, 2, 2, 0]

Before: [3, 2, 2, 0]
4 0 2 0
After:  [1, 2, 2, 0]

Before: [3, 1, 1, 3]
7 1 3 1
After:  [3, 0, 1, 3]

Before: [2, 2, 2, 3]
7 2 3 2
After:  [2, 2, 0, 3]

Before: [2, 1, 2, 2]
2 1 2 2
After:  [2, 1, 0, 2]

Before: [2, 0, 0, 3]
11 3 3 2
After:  [2, 0, 3, 3]

Before: [1, 1, 2, 1]
1 0 2 1
After:  [1, 0, 2, 1]

Before: [0, 1, 2, 1]
15 3 2 1
After:  [0, 1, 2, 1]

Before: [0, 3, 3, 3]
0 0 0 3
After:  [0, 3, 3, 0]

Before: [0, 1, 2, 3]
2 1 2 0
After:  [0, 1, 2, 3]

Before: [3, 3, 2, 3]
4 0 2 2
After:  [3, 3, 1, 3]

Before: [3, 2, 3, 3]
12 1 2 0
After:  [2, 2, 3, 3]

Before: [1, 1, 3, 0]
6 1 0 2
After:  [1, 1, 1, 0]

Before: [2, 3, 3, 3]
5 3 2 1
After:  [2, 1, 3, 3]

Before: [0, 1, 1, 2]
0 0 0 0
After:  [0, 1, 1, 2]

Before: [3, 1, 3, 2]
12 3 2 0
After:  [2, 1, 3, 2]

Before: [1, 3, 2, 1]
1 0 2 3
After:  [1, 3, 2, 0]

Before: [0, 1, 3, 2]
14 1 3 1
After:  [0, 0, 3, 2]

Before: [1, 1, 2, 3]
7 1 3 1
After:  [1, 0, 2, 3]

Before: [2, 2, 3, 0]
12 0 2 1
After:  [2, 2, 3, 0]

Before: [0, 1, 2, 2]
14 1 3 1
After:  [0, 0, 2, 2]

Before: [1, 1, 1, 2]
13 3 3 2
After:  [1, 1, 0, 2]

Before: [3, 3, 2, 0]
4 0 2 0
After:  [1, 3, 2, 0]

Before: [2, 1, 2, 2]
11 2 2 0
After:  [2, 1, 2, 2]

Before: [0, 0, 1, 3]
0 0 0 2
After:  [0, 0, 0, 3]

Before: [1, 0, 2, 1]
15 3 2 1
After:  [1, 1, 2, 1]

Before: [3, 2, 2, 2]
4 0 2 1
After:  [3, 1, 2, 2]

Before: [0, 2, 3, 3]
12 1 2 3
After:  [0, 2, 3, 2]

Before: [3, 3, 0, 3]
8 0 2 2
After:  [3, 3, 1, 3]

Before: [1, 1, 0, 2]
14 1 3 0
After:  [0, 1, 0, 2]

Before: [2, 3, 0, 3]
3 0 1 2
After:  [2, 3, 1, 3]

Before: [1, 1, 1, 1]
8 2 1 1
After:  [1, 0, 1, 1]

Before: [1, 1, 2, 0]
1 0 2 3
After:  [1, 1, 2, 0]

Before: [1, 2, 2, 1]
5 2 1 0
After:  [1, 2, 2, 1]

Before: [1, 1, 2, 3]
1 0 2 3
After:  [1, 1, 2, 0]

Before: [0, 1, 3, 0]
10 1 3 0
After:  [1, 1, 3, 0]

Before: [0, 1, 1, 1]
9 1 3 1
After:  [0, 1, 1, 1]

Before: [1, 1, 0, 3]
6 1 0 0
After:  [1, 1, 0, 3]

Before: [1, 2, 2, 3]
1 0 2 0
After:  [0, 2, 2, 3]

Before: [3, 3, 1, 2]
13 3 3 2
After:  [3, 3, 0, 2]

Before: [2, 2, 2, 1]
15 3 2 3
After:  [2, 2, 2, 1]

Before: [1, 2, 1, 3]
7 1 3 1
After:  [1, 0, 1, 3]

Before: [1, 1, 0, 2]
9 0 2 3
After:  [1, 1, 0, 0]

Before: [3, 3, 0, 2]
8 0 2 1
After:  [3, 1, 0, 2]

Before: [1, 0, 0, 3]
11 3 3 3
After:  [1, 0, 0, 3]

Before: [0, 3, 2, 2]
0 0 0 2
After:  [0, 3, 0, 2]

Before: [2, 3, 3, 0]
3 0 1 0
After:  [1, 3, 3, 0]

Before: [3, 3, 2, 1]
3 2 0 2
After:  [3, 3, 1, 1]

Before: [1, 1, 2, 2]
14 1 3 3
After:  [1, 1, 2, 0]

Before: [3, 3, 1, 1]
13 2 3 3
After:  [3, 3, 1, 0]

Before: [3, 1, 2, 0]
4 0 2 3
After:  [3, 1, 2, 1]

Before: [0, 3, 2, 2]
3 2 1 3
After:  [0, 3, 2, 1]

Before: [3, 1, 2, 1]
15 3 2 2
After:  [3, 1, 1, 1]

Before: [3, 1, 2, 2]
2 1 2 2
After:  [3, 1, 0, 2]

Before: [0, 0, 2, 1]
15 3 2 1
After:  [0, 1, 2, 1]

Before: [1, 1, 2, 1]
15 3 2 1
After:  [1, 1, 2, 1]

Before: [1, 3, 2, 2]
8 3 2 0
After:  [0, 3, 2, 2]

Before: [1, 2, 2, 1]
15 3 2 3
After:  [1, 2, 2, 1]

Before: [2, 0, 2, 1]
15 3 2 2
After:  [2, 0, 1, 1]

Before: [2, 2, 2, 1]
15 3 2 0
After:  [1, 2, 2, 1]

Before: [1, 3, 3, 2]
13 3 3 3
After:  [1, 3, 3, 0]

Before: [2, 0, 0, 2]
13 3 3 2
After:  [2, 0, 0, 2]

Before: [1, 0, 0, 0]
9 0 2 1
After:  [1, 0, 0, 0]

Before: [2, 2, 2, 3]
11 3 3 0
After:  [3, 2, 2, 3]

Before: [1, 3, 2, 1]
1 0 2 2
After:  [1, 3, 0, 1]

Before: [3, 1, 3, 1]
9 1 3 1
After:  [3, 1, 3, 1]

Before: [0, 2, 3, 0]
12 1 2 2
After:  [0, 2, 2, 0]

Before: [1, 1, 3, 2]
6 1 0 0
After:  [1, 1, 3, 2]

Before: [3, 0, 2, 2]
8 3 2 1
After:  [3, 0, 2, 2]

Before: [1, 1, 0, 1]
9 0 2 0
After:  [0, 1, 0, 1]

Before: [1, 1, 2, 1]
9 1 3 1
After:  [1, 1, 2, 1]

Before: [2, 2, 2, 0]
5 2 0 0
After:  [1, 2, 2, 0]

Before: [3, 3, 2, 1]
15 3 2 2
After:  [3, 3, 1, 1]

Before: [0, 1, 1, 1]
9 1 3 3
After:  [0, 1, 1, 1]

Before: [1, 1, 3, 0]
6 1 0 1
After:  [1, 1, 3, 0]

Before: [0, 3, 1, 3]
0 0 0 2
After:  [0, 3, 0, 3]

Before: [2, 3, 3, 0]
8 2 0 1
After:  [2, 1, 3, 0]

Before: [3, 1, 3, 2]
14 1 3 1
After:  [3, 0, 3, 2]

Before: [0, 3, 1, 3]
7 2 3 0
After:  [0, 3, 1, 3]

Before: [2, 1, 3, 1]
4 0 1 2
After:  [2, 1, 1, 1]

Before: [0, 1, 3, 2]
0 0 0 2
After:  [0, 1, 0, 2]

Before: [2, 2, 3, 1]
12 0 2 2
After:  [2, 2, 2, 1]

Before: [3, 1, 3, 1]
13 3 3 3
After:  [3, 1, 3, 0]

Before: [3, 3, 2, 2]
3 2 1 0
After:  [1, 3, 2, 2]

Before: [0, 1, 2, 3]
2 1 2 2
After:  [0, 1, 0, 3]

Before: [3, 1, 2, 2]
3 2 0 0
After:  [1, 1, 2, 2]

Before: [0, 1, 1, 0]
8 2 1 3
After:  [0, 1, 1, 0]

Before: [1, 1, 2, 3]
1 0 2 0
After:  [0, 1, 2, 3]

Before: [1, 2, 0, 3]
7 1 3 3
After:  [1, 2, 0, 0]

Before: [2, 1, 3, 0]
10 1 3 1
After:  [2, 1, 3, 0]

Before: [3, 1, 2, 0]
3 2 0 0
After:  [1, 1, 2, 0]

Before: [1, 1, 2, 2]
6 1 0 2
After:  [1, 1, 1, 2]

Before: [0, 1, 2, 0]
10 1 3 1
After:  [0, 1, 2, 0]

Before: [2, 1, 2, 2]
5 2 0 1
After:  [2, 1, 2, 2]

Before: [2, 1, 0, 2]
14 1 3 0
After:  [0, 1, 0, 2]

Before: [1, 1, 2, 1]
15 3 2 2
After:  [1, 1, 1, 1]

Before: [3, 1, 2, 0]
2 1 2 2
After:  [3, 1, 0, 0]

Before: [1, 1, 2, 3]
2 1 2 1
After:  [1, 0, 2, 3]

Before: [3, 0, 2, 2]
3 2 0 2
After:  [3, 0, 1, 2]

Before: [0, 0, 3, 2]
13 3 3 2
After:  [0, 0, 0, 2]

Before: [1, 0, 2, 2]
1 0 2 2
After:  [1, 0, 0, 2]

Before: [0, 1, 2, 3]
11 3 3 3
After:  [0, 1, 2, 3]

Before: [2, 0, 3, 3]
5 3 2 1
After:  [2, 1, 3, 3]

Before: [0, 2, 0, 3]
0 0 0 3
After:  [0, 2, 0, 0]

Before: [2, 2, 0, 1]
13 3 3 3
After:  [2, 2, 0, 0]

Before: [0, 1, 2, 2]
14 1 3 3
After:  [0, 1, 2, 0]

Before: [2, 1, 2, 1]
4 0 1 1
After:  [2, 1, 2, 1]

Before: [1, 1, 3, 1]
9 1 3 0
After:  [1, 1, 3, 1]

Before: [1, 1, 1, 3]
6 1 0 1
After:  [1, 1, 1, 3]

Before: [3, 1, 1, 0]
8 2 1 1
After:  [3, 0, 1, 0]

Before: [3, 2, 2, 1]
15 3 2 1
After:  [3, 1, 2, 1]

Before: [2, 1, 2, 3]
11 3 3 0
After:  [3, 1, 2, 3]

Before: [0, 0, 2, 1]
15 3 2 2
After:  [0, 0, 1, 1]

Before: [1, 2, 2, 1]
15 3 2 0
After:  [1, 2, 2, 1]

Before: [0, 3, 2, 2]
0 0 0 3
After:  [0, 3, 2, 0]

Before: [2, 1, 2, 0]
2 1 2 3
After:  [2, 1, 2, 0]

Before: [0, 3, 2, 3]
3 2 1 0
After:  [1, 3, 2, 3]

Before: [1, 2, 2, 3]
1 0 2 3
After:  [1, 2, 2, 0]

Before: [2, 3, 0, 0]
3 0 1 3
After:  [2, 3, 0, 1]

Before: [2, 3, 1, 3]
3 0 1 1
After:  [2, 1, 1, 3]

Before: [3, 1, 2, 1]
2 1 2 0
After:  [0, 1, 2, 1]

Before: [3, 1, 3, 2]
12 3 2 1
After:  [3, 2, 3, 2]

Before: [3, 1, 2, 3]
2 1 2 3
After:  [3, 1, 2, 0]

Before: [2, 1, 2, 0]
2 1 2 2
After:  [2, 1, 0, 0]

Before: [0, 3, 2, 3]
0 0 0 3
After:  [0, 3, 2, 0]

Before: [1, 0, 0, 2]
13 3 3 3
After:  [1, 0, 0, 0]

Before: [2, 3, 3, 3]
3 0 1 1
After:  [2, 1, 3, 3]

Before: [0, 1, 0, 3]
7 1 3 3
After:  [0, 1, 0, 0]

Before: [0, 1, 2, 2]
2 1 2 2
After:  [0, 1, 0, 2]

Before: [2, 0, 3, 0]
8 2 0 3
After:  [2, 0, 3, 1]

Before: [2, 3, 2, 1]
15 3 2 3
After:  [2, 3, 2, 1]

Before: [0, 2, 3, 2]
13 3 3 3
After:  [0, 2, 3, 0]

Before: [0, 2, 2, 3]
7 1 3 2
After:  [0, 2, 0, 3]

Before: [3, 2, 1, 3]
7 1 3 3
After:  [3, 2, 1, 0]

Before: [2, 1, 1, 2]
14 1 3 0
After:  [0, 1, 1, 2]

Before: [3, 1, 2, 0]
4 0 2 2
After:  [3, 1, 1, 0]

Before: [1, 2, 3, 1]
12 1 2 0
After:  [2, 2, 3, 1]

Before: [0, 0, 3, 2]
12 3 2 3
After:  [0, 0, 3, 2]

Before: [2, 1, 2, 0]
10 1 3 3
After:  [2, 1, 2, 1]

Before: [2, 0, 3, 3]
12 0 2 3
After:  [2, 0, 3, 2]

Before: [1, 1, 1, 2]
14 1 3 2
After:  [1, 1, 0, 2]

Before: [0, 2, 0, 3]
11 3 3 2
After:  [0, 2, 3, 3]

Before: [3, 2, 1, 3]
7 2 3 3
After:  [3, 2, 1, 0]

Before: [3, 1, 2, 2]
8 3 2 3
After:  [3, 1, 2, 0]

Before: [2, 3, 2, 3]
3 0 1 0
After:  [1, 3, 2, 3]

Before: [2, 1, 2, 2]
4 0 1 3
After:  [2, 1, 2, 1]

Before: [3, 2, 2, 2]
3 2 0 2
After:  [3, 2, 1, 2]

Before: [3, 1, 2, 1]
4 0 2 2
After:  [3, 1, 1, 1]

Before: [2, 3, 2, 1]
15 3 2 0
After:  [1, 3, 2, 1]

Before: [2, 1, 3, 2]
4 0 1 3
After:  [2, 1, 3, 1]

Before: [0, 1, 3, 2]
14 1 3 0
After:  [0, 1, 3, 2]

Before: [1, 2, 2, 1]
15 3 2 1
After:  [1, 1, 2, 1]

Before: [1, 3, 0, 2]
9 0 2 0
After:  [0, 3, 0, 2]

Before: [1, 1, 3, 0]
6 1 0 3
After:  [1, 1, 3, 1]

Before: [1, 0, 2, 0]
1 0 2 2
After:  [1, 0, 0, 0]

Before: [0, 1, 0, 3]
0 0 0 1
After:  [0, 0, 0, 3]

Before: [1, 3, 2, 3]
1 0 2 1
After:  [1, 0, 2, 3]

Before: [3, 3, 2, 2]
3 2 1 2
After:  [3, 3, 1, 2]

Before: [2, 1, 0, 2]
4 0 1 3
After:  [2, 1, 0, 1]

Before: [2, 2, 1, 3]
7 2 3 0
After:  [0, 2, 1, 3]

Before: [2, 1, 2, 2]
4 0 1 2
After:  [2, 1, 1, 2]

Before: [2, 1, 3, 2]
12 3 2 3
After:  [2, 1, 3, 2]

Before: [2, 2, 3, 3]
5 3 2 1
After:  [2, 1, 3, 3]

Before: [0, 1, 1, 0]
10 1 3 0
After:  [1, 1, 1, 0]

Before: [0, 3, 2, 1]
13 3 3 3
After:  [0, 3, 2, 0]

Before: [0, 2, 3, 2]
12 3 2 1
After:  [0, 2, 3, 2]

Before: [0, 2, 3, 1]
0 0 0 0
After:  [0, 2, 3, 1]

Before: [1, 1, 0, 1]
9 0 2 1
After:  [1, 0, 0, 1]

Before: [3, 2, 3, 3]
7 1 3 1
After:  [3, 0, 3, 3]

Before: [0, 3, 0, 3]
11 3 3 3
After:  [0, 3, 0, 3]

Before: [3, 3, 2, 1]
15 3 2 1
After:  [3, 1, 2, 1]

Before: [1, 1, 2, 1]
6 1 0 1
After:  [1, 1, 2, 1]

Before: [3, 3, 2, 3]
4 0 2 0
After:  [1, 3, 2, 3]

Before: [2, 3, 3, 0]
12 0 2 3
After:  [2, 3, 3, 2]

Before: [1, 3, 2, 0]
3 2 1 1
After:  [1, 1, 2, 0]

Before: [3, 3, 2, 3]
3 2 0 1
After:  [3, 1, 2, 3]

Before: [0, 2, 3, 1]
12 1 2 0
After:  [2, 2, 3, 1]

Before: [3, 0, 2, 0]
3 2 0 1
After:  [3, 1, 2, 0]

Before: [1, 3, 2, 1]
1 0 2 1
After:  [1, 0, 2, 1]

Before: [1, 1, 2, 1]
6 1 0 3
After:  [1, 1, 2, 1]

Before: [1, 2, 3, 2]
12 1 2 1
After:  [1, 2, 3, 2]

Before: [1, 1, 2, 1]
1 0 2 3
After:  [1, 1, 2, 0]

Before: [2, 1, 0, 0]
10 1 3 0
After:  [1, 1, 0, 0]

Before: [1, 2, 2, 0]
5 2 1 1
After:  [1, 1, 2, 0]

Before: [3, 3, 2, 0]
4 0 2 1
After:  [3, 1, 2, 0]

Before: [0, 0, 0, 3]
0 0 0 0
After:  [0, 0, 0, 3]

Before: [1, 1, 1, 0]
6 1 0 0
After:  [1, 1, 1, 0]

Before: [1, 1, 2, 3]
1 0 2 2
After:  [1, 1, 0, 3]

Before: [3, 0, 2, 1]
4 0 2 0
After:  [1, 0, 2, 1]

Before: [1, 1, 0, 0]
6 1 0 2
After:  [1, 1, 1, 0]

Before: [1, 1, 1, 0]
8 2 1 0
After:  [0, 1, 1, 0]

Before: [3, 2, 2, 3]
5 2 1 2
After:  [3, 2, 1, 3]

Before: [3, 3, 2, 1]
4 0 2 2
After:  [3, 3, 1, 1]

Before: [2, 3, 0, 2]
3 0 1 2
After:  [2, 3, 1, 2]

Before: [1, 3, 0, 2]
9 0 2 2
After:  [1, 3, 0, 2]

Before: [1, 2, 0, 1]
9 0 2 1
After:  [1, 0, 0, 1]

Before: [2, 0, 2, 0]
5 2 0 3
After:  [2, 0, 2, 1]

Before: [1, 1, 3, 1]
8 3 1 2
After:  [1, 1, 0, 1]

Before: [1, 1, 3, 0]
10 1 3 0
After:  [1, 1, 3, 0]

Before: [2, 3, 3, 2]
8 2 0 2
After:  [2, 3, 1, 2]

Before: [3, 1, 0, 0]
10 1 3 1
After:  [3, 1, 0, 0]

Before: [1, 1, 0, 3]
9 0 2 1
After:  [1, 0, 0, 3]

Before: [3, 2, 3, 2]
12 3 2 2
After:  [3, 2, 2, 2]

Before: [1, 3, 2, 0]
1 0 2 1
After:  [1, 0, 2, 0]

Before: [1, 2, 0, 1]
13 3 3 0
After:  [0, 2, 0, 1]

Before: [0, 1, 3, 3]
5 3 2 3
After:  [0, 1, 3, 1]

Before: [1, 1, 1, 0]
10 1 3 1
After:  [1, 1, 1, 0]

Before: [2, 0, 2, 0]
5 2 0 1
After:  [2, 1, 2, 0]

Before: [0, 1, 2, 1]
2 1 2 3
After:  [0, 1, 2, 0]

Before: [3, 2, 3, 3]
7 1 3 0
After:  [0, 2, 3, 3]

Before: [0, 3, 0, 0]
0 0 0 0
After:  [0, 3, 0, 0]

Before: [3, 1, 3, 1]
8 3 1 1
After:  [3, 0, 3, 1]

Before: [0, 1, 3, 2]
14 1 3 2
After:  [0, 1, 0, 2]

Before: [2, 3, 1, 3]
3 0 1 0
After:  [1, 3, 1, 3]

Before: [1, 1, 0, 2]
6 1 0 3
After:  [1, 1, 0, 1]

Before: [1, 3, 2, 2]
3 2 1 1
After:  [1, 1, 2, 2]

Before: [0, 2, 2, 1]
15 3 2 0
After:  [1, 2, 2, 1]

Before: [2, 1, 2, 0]
10 1 3 1
After:  [2, 1, 2, 0]

Before: [2, 0, 2, 0]
11 2 2 0
After:  [2, 0, 2, 0]

Before: [0, 1, 0, 2]
13 3 3 0
After:  [0, 1, 0, 2]

Before: [1, 1, 0, 3]
6 1 0 3
After:  [1, 1, 0, 1]

Before: [1, 3, 2, 2]
1 0 2 3
After:  [1, 3, 2, 0]

Before: [3, 1, 2, 3]
2 1 2 2
After:  [3, 1, 0, 3]

Before: [3, 1, 2, 3]
4 0 2 0
After:  [1, 1, 2, 3]

Before: [2, 1, 3, 2]
12 0 2 3
After:  [2, 1, 3, 2]

Before: [3, 1, 2, 2]
2 1 2 0
After:  [0, 1, 2, 2]

Before: [1, 1, 2, 2]
14 1 3 0
After:  [0, 1, 2, 2]

Before: [3, 1, 0, 2]
8 0 2 0
After:  [1, 1, 0, 2]

Before: [2, 3, 2, 1]
15 3 2 2
After:  [2, 3, 1, 1]

Before: [3, 1, 0, 2]
13 3 3 3
After:  [3, 1, 0, 0]

Before: [3, 1, 2, 0]
10 1 3 3
After:  [3, 1, 2, 1]

Before: [0, 0, 1, 3]
0 0 0 1
After:  [0, 0, 1, 3]

Before: [3, 3, 3, 3]
11 3 3 2
After:  [3, 3, 3, 3]

Before: [0, 1, 1, 0]
10 1 3 3
After:  [0, 1, 1, 1]

Before: [3, 2, 2, 3]
5 2 1 3
After:  [3, 2, 2, 1]

Before: [1, 0, 0, 1]
9 0 2 2
After:  [1, 0, 0, 1]

Before: [2, 2, 2, 0]
5 2 1 0
After:  [1, 2, 2, 0]

Before: [1, 1, 2, 1]
15 3 2 0
After:  [1, 1, 2, 1]

Before: [2, 1, 1, 2]
14 1 3 2
After:  [2, 1, 0, 2]

Before: [3, 2, 2, 3]
11 3 3 1
After:  [3, 3, 2, 3]

Before: [1, 1, 2, 0]
6 1 0 2
After:  [1, 1, 1, 0]

Before: [3, 0, 0, 1]
8 0 2 3
After:  [3, 0, 0, 1]

Before: [3, 3, 3, 3]
5 3 2 3
After:  [3, 3, 3, 1]

Before: [0, 1, 2, 2]
14 1 3 0
After:  [0, 1, 2, 2]

Before: [3, 1, 0, 1]
9 1 3 2
After:  [3, 1, 1, 1]

Before: [3, 1, 3, 0]
10 1 3 0
After:  [1, 1, 3, 0]

Before: [3, 2, 1, 3]
7 2 3 2
After:  [3, 2, 0, 3]

Before: [2, 1, 3, 3]
8 2 0 3
After:  [2, 1, 3, 1]

Before: [0, 3, 2, 3]
11 2 2 3
After:  [0, 3, 2, 2]

Before: [0, 1, 2, 1]
2 1 2 1
After:  [0, 0, 2, 1]

Before: [2, 1, 2, 1]
4 0 1 0
After:  [1, 1, 2, 1]

Before: [1, 1, 3, 0]
6 1 0 0
After:  [1, 1, 3, 0]

Before: [2, 1, 2, 0]
4 0 1 1
After:  [2, 1, 2, 0]

Before: [0, 1, 0, 2]
14 1 3 2
After:  [0, 1, 0, 2]

Before: [1, 1, 1, 3]
7 1 3 3
After:  [1, 1, 1, 0]

Before: [0, 1, 1, 1]
0 0 0 0
After:  [0, 1, 1, 1]

Before: [1, 2, 3, 2]
12 3 2 2
After:  [1, 2, 2, 2]

Before: [1, 1, 0, 3]
7 1 3 3
After:  [1, 1, 0, 0]

Before: [1, 2, 1, 3]
7 2 3 1
After:  [1, 0, 1, 3]

Before: [3, 1, 0, 2]
14 1 3 2
After:  [3, 1, 0, 2]

Before: [2, 3, 3, 3]
12 0 2 3
After:  [2, 3, 3, 2]

Before: [3, 2, 3, 1]
12 1 2 0
After:  [2, 2, 3, 1]

Before: [1, 1, 1, 2]
6 1 0 2
After:  [1, 1, 1, 2]

Before: [0, 0, 2, 1]
11 2 2 3
After:  [0, 0, 2, 2]

Before: [0, 3, 1, 3]
0 0 0 1
After:  [0, 0, 1, 3]

Before: [2, 1, 3, 0]
8 2 0 2
After:  [2, 1, 1, 0]

Before: [2, 1, 3, 3]
12 0 2 1
After:  [2, 2, 3, 3]

Before: [1, 2, 3, 3]
12 1 2 1
After:  [1, 2, 3, 3]

Before: [1, 1, 0, 3]
6 1 0 2
After:  [1, 1, 1, 3]

Before: [3, 3, 2, 2]
4 0 2 3
After:  [3, 3, 2, 1]

Before: [3, 2, 0, 2]
13 3 3 3
After:  [3, 2, 0, 0]

Before: [1, 1, 0, 1]
6 1 0 1
After:  [1, 1, 0, 1]

Before: [3, 3, 2, 3]
7 2 3 0
After:  [0, 3, 2, 3]

Before: [3, 1, 2, 2]
2 1 2 1
After:  [3, 0, 2, 2]

Before: [3, 1, 3, 1]
9 1 3 2
After:  [3, 1, 1, 1]

Before: [3, 3, 2, 1]
15 3 2 3
After:  [3, 3, 2, 1]

Before: [0, 1, 3, 0]
10 1 3 1
After:  [0, 1, 3, 0]

Before: [1, 1, 2, 2]
6 1 0 0
After:  [1, 1, 2, 2]

Before: [2, 0, 1, 1]
8 0 1 2
After:  [2, 0, 1, 1]

Before: [1, 1, 2, 3]
11 2 2 2
After:  [1, 1, 2, 3]

Before: [0, 3, 3, 2]
12 3 2 1
After:  [0, 2, 3, 2]

Before: [0, 1, 2, 1]
9 1 3 1
After:  [0, 1, 2, 1]

Before: [3, 0, 3, 3]
5 3 0 1
After:  [3, 1, 3, 3]

Before: [1, 0, 0, 1]
9 0 2 3
After:  [1, 0, 0, 0]

Before: [0, 1, 1, 0]
10 1 3 1
After:  [0, 1, 1, 0]

Before: [1, 1, 3, 2]
6 1 0 2
After:  [1, 1, 1, 2]

Before: [3, 3, 3, 1]
5 2 3 0
After:  [0, 3, 3, 1]

Before: [3, 1, 2, 3]
7 1 3 2
After:  [3, 1, 0, 3]

Before: [3, 3, 2, 3]
11 3 3 0
After:  [3, 3, 2, 3]

Before: [1, 1, 0, 1]
8 3 1 2
After:  [1, 1, 0, 1]

Before: [0, 1, 3, 2]
14 1 3 3
After:  [0, 1, 3, 0]

Before: [2, 3, 0, 3]
3 0 1 3
After:  [2, 3, 0, 1]

Before: [2, 1, 3, 2]
12 0 2 2
After:  [2, 1, 2, 2]

Before: [2, 1, 0, 0]
10 1 3 3
After:  [2, 1, 0, 1]

Before: [3, 2, 2, 0]
3 2 0 0
After:  [1, 2, 2, 0]

Before: [2, 2, 2, 1]
13 3 3 2
After:  [2, 2, 0, 1]

Before: [3, 1, 3, 1]
5 2 3 1
After:  [3, 0, 3, 1]

Before: [2, 3, 3, 3]
12 0 2 1
After:  [2, 2, 3, 3]

Before: [1, 1, 1, 1]
6 1 0 3
After:  [1, 1, 1, 1]

Before: [0, 1, 0, 0]
10 1 3 0
After:  [1, 1, 0, 0]

Before: [3, 1, 2, 3]
7 1 3 0
After:  [0, 1, 2, 3]

Before: [2, 1, 2, 1]
15 3 2 2
After:  [2, 1, 1, 1]

Before: [3, 1, 3, 2]
13 3 3 2
After:  [3, 1, 0, 2]

Before: [0, 1, 3, 1]
8 3 1 2
After:  [0, 1, 0, 1]

Before: [0, 0, 3, 0]
0 0 0 0
After:  [0, 0, 3, 0]

Before: [2, 3, 3, 1]
12 0 2 1
After:  [2, 2, 3, 1]

Before: [0, 1, 3, 1]
9 1 3 0
After:  [1, 1, 3, 1]

Before: [3, 1, 1, 0]
10 1 3 3
After:  [3, 1, 1, 1]

Before: [1, 1, 0, 1]
6 1 0 0
After:  [1, 1, 0, 1]

Before: [0, 2, 0, 0]
0 0 0 0
After:  [0, 2, 0, 0]

Before: [3, 0, 2, 3]
3 2 0 0
After:  [1, 0, 2, 3]

Before: [0, 2, 2, 3]
0 0 0 2
After:  [0, 2, 0, 3]

Before: [0, 3, 3, 3]
11 3 3 2
After:  [0, 3, 3, 3]

Before: [3, 1, 1, 3]
5 3 0 3
After:  [3, 1, 1, 1]

Before: [1, 2, 0, 3]
11 3 3 2
After:  [1, 2, 3, 3]

Before: [0, 3, 1, 1]
0 0 0 1
After:  [0, 0, 1, 1]

Before: [2, 1, 0, 0]
10 1 3 1
After:  [2, 1, 0, 0]

Before: [2, 1, 0, 1]
9 1 3 1
After:  [2, 1, 0, 1]

Before: [2, 3, 2, 3]
3 2 1 1
After:  [2, 1, 2, 3]

Before: [0, 3, 0, 2]
0 0 0 3
After:  [0, 3, 0, 0]

Before: [0, 2, 2, 3]
11 2 2 2
After:  [0, 2, 2, 3]

Before: [3, 2, 2, 1]
15 3 2 0
After:  [1, 2, 2, 1]

Before: [2, 3, 2, 3]
11 2 2 2
After:  [2, 3, 2, 3]

Before: [1, 0, 2, 1]
15 3 2 3
After:  [1, 0, 2, 1]

Before: [2, 3, 3, 2]
3 0 1 0
After:  [1, 3, 3, 2]

Before: [3, 3, 2, 2]
4 0 2 0
After:  [1, 3, 2, 2]

Before: [3, 1, 3, 2]
14 1 3 3
After:  [3, 1, 3, 0]

Before: [2, 1, 2, 3]
2 1 2 0
After:  [0, 1, 2, 3]

Before: [3, 1, 3, 3]
5 3 0 0
After:  [1, 1, 3, 3]

Before: [0, 1, 2, 2]
2 1 2 0
After:  [0, 1, 2, 2]

Before: [1, 1, 2, 3]
6 1 0 0
After:  [1, 1, 2, 3]

Before: [1, 3, 2, 2]
1 0 2 2
After:  [1, 3, 0, 2]

Before: [1, 1, 2, 0]
2 1 2 0
After:  [0, 1, 2, 0]

Before: [1, 2, 0, 1]
9 0 2 0
After:  [0, 2, 0, 1]

Before: [3, 2, 2, 3]
4 0 2 0
After:  [1, 2, 2, 3]

Before: [2, 2, 3, 2]
12 0 2 2
After:  [2, 2, 2, 2]

Before: [2, 0, 2, 1]
15 3 2 0
After:  [1, 0, 2, 1]

Before: [2, 1, 2, 3]
5 2 0 0
After:  [1, 1, 2, 3]

Before: [2, 1, 2, 1]
9 1 3 0
After:  [1, 1, 2, 1]

Before: [3, 3, 2, 0]
3 2 1 0
After:  [1, 3, 2, 0]

Before: [1, 3, 2, 3]
1 0 2 3
After:  [1, 3, 2, 0]

Before: [0, 0, 2, 1]
15 3 2 3
After:  [0, 0, 2, 1]

Before: [1, 3, 2, 2]
1 0 2 1
After:  [1, 0, 2, 2]

Before: [3, 0, 3, 3]
5 3 0 0
After:  [1, 0, 3, 3]

Before: [2, 3, 1, 3]
7 2 3 2
After:  [2, 3, 0, 3]

Before: [0, 1, 0, 2]
14 1 3 1
After:  [0, 0, 0, 2]

Before: [2, 1, 2, 1]
2 1 2 3
After:  [2, 1, 2, 0]

Before: [2, 0, 1, 3]
7 2 3 1
After:  [2, 0, 1, 3]

Before: [1, 1, 1, 2]
14 1 3 0
After:  [0, 1, 1, 2]

Before: [2, 1, 0, 1]
4 0 1 0
After:  [1, 1, 0, 1]

Before: [2, 3, 0, 2]
3 0 1 0
After:  [1, 3, 0, 2]

Before: [2, 3, 2, 2]
5 2 0 3
After:  [2, 3, 2, 1]

Before: [0, 0, 2, 1]
15 3 2 0
After:  [1, 0, 2, 1]

Before: [1, 1, 3, 2]
14 1 3 2
After:  [1, 1, 0, 2]

Before: [1, 3, 0, 3]
9 0 2 3
After:  [1, 3, 0, 0]

Before: [1, 3, 3, 1]
13 3 3 0
After:  [0, 3, 3, 1]

Before: [3, 2, 2, 1]
4 0 2 1
After:  [3, 1, 2, 1]

Before: [2, 3, 1, 1]
3 0 1 3
After:  [2, 3, 1, 1]

Before: [1, 1, 0, 0]
9 0 2 3
After:  [1, 1, 0, 0]

Before: [2, 1, 3, 0]
8 2 0 0
After:  [1, 1, 3, 0]

Before: [2, 2, 2, 0]
5 2 1 1
After:  [2, 1, 2, 0]

Before: [1, 1, 2, 1]
6 1 0 2
After:  [1, 1, 1, 1]

Before: [0, 3, 1, 0]
0 0 0 2
After:  [0, 3, 0, 0]

Before: [1, 3, 2, 2]
8 3 2 1
After:  [1, 0, 2, 2]

Before: [1, 1, 1, 0]
10 1 3 2
After:  [1, 1, 1, 0]

Before: [1, 2, 2, 0]
11 2 2 1
After:  [1, 2, 2, 0]

Before: [2, 1, 2, 2]
11 2 2 2
After:  [2, 1, 2, 2]

Before: [1, 3, 2, 1]
15 3 2 1
After:  [1, 1, 2, 1]

Before: [0, 2, 3, 3]
0 0 0 0
After:  [0, 2, 3, 3]

Before: [0, 2, 2, 3]
11 2 2 0
After:  [2, 2, 2, 3]

Before: [3, 2, 3, 3]
5 3 2 2
After:  [3, 2, 1, 3]

Before: [2, 0, 3, 3]
12 0 2 2
After:  [2, 0, 2, 3]

Before: [2, 1, 1, 1]
9 1 3 0
After:  [1, 1, 1, 1]

Before: [1, 1, 2, 1]
9 1 3 2
After:  [1, 1, 1, 1]

Before: [1, 1, 2, 2]
11 2 2 3
After:  [1, 1, 2, 2]

Before: [2, 1, 3, 2]
12 3 2 0
After:  [2, 1, 3, 2]

Before: [1, 1, 0, 2]
9 0 2 0
After:  [0, 1, 0, 2]

Before: [1, 1, 3, 3]
6 1 0 3
After:  [1, 1, 3, 1]

Before: [1, 3, 0, 2]
13 3 3 2
After:  [1, 3, 0, 2]

Before: [1, 1, 0, 0]
6 1 0 3
After:  [1, 1, 0, 1]

Before: [3, 2, 3, 3]
5 3 0 3
After:  [3, 2, 3, 1]

Before: [1, 1, 1, 3]
8 2 1 3
After:  [1, 1, 1, 0]

Before: [3, 1, 2, 2]
14 1 3 0
After:  [0, 1, 2, 2]

Before: [1, 0, 2, 0]
1 0 2 1
After:  [1, 0, 2, 0]

Before: [2, 1, 3, 3]
7 1 3 2
After:  [2, 1, 0, 3]

Before: [1, 1, 2, 1]
2 1 2 0
After:  [0, 1, 2, 1]

Before: [2, 1, 0, 2]
14 1 3 1
After:  [2, 0, 0, 2]

Before: [0, 3, 2, 1]
15 3 2 3
After:  [0, 3, 2, 1]

Before: [2, 3, 3, 3]
3 0 1 3
After:  [2, 3, 3, 1]

Before: [3, 0, 2, 3]
4 0 2 1
After:  [3, 1, 2, 3]

Before: [0, 2, 1, 3]
7 2 3 1
After:  [0, 0, 1, 3]

Before: [1, 3, 2, 0]
3 2 1 3
After:  [1, 3, 2, 1]

Before: [3, 2, 3, 3]
5 3 0 0
After:  [1, 2, 3, 3]

Before: [2, 0, 0, 1]
8 0 1 0
After:  [1, 0, 0, 1]

Before: [2, 1, 3, 1]
9 1 3 2
After:  [2, 1, 1, 1]

Before: [0, 2, 2, 1]
11 2 2 1
After:  [0, 2, 2, 1]

Before: [0, 1, 0, 3]
0 0 0 3
After:  [0, 1, 0, 0]

Before: [2, 1, 1, 3]
4 0 1 1
After:  [2, 1, 1, 3]

Before: [3, 3, 2, 2]
3 2 0 0
After:  [1, 3, 2, 2]

Before: [2, 2, 3, 2]
12 1 2 0
After:  [2, 2, 3, 2]

Before: [3, 0, 2, 1]
11 2 2 2
After:  [3, 0, 2, 1]

Before: [2, 0, 3, 2]
8 2 0 0
After:  [1, 0, 3, 2]

Before: [0, 1, 2, 1]
0 0 0 0
After:  [0, 1, 2, 1]

Before: [1, 2, 2, 1]
1 0 2 0
After:  [0, 2, 2, 1]

Before: [2, 1, 1, 1]
8 2 1 0
After:  [0, 1, 1, 1]

Before: [1, 1, 2, 2]
14 1 3 1
After:  [1, 0, 2, 2]

Before: [0, 3, 3, 2]
12 3 2 0
After:  [2, 3, 3, 2]

Before: [0, 3, 2, 1]
15 3 2 1
After:  [0, 1, 2, 1]

Before: [2, 2, 3, 0]
8 2 0 0
After:  [1, 2, 3, 0]

Before: [3, 3, 2, 1]
4 0 2 1
After:  [3, 1, 2, 1]

Before: [1, 1, 2, 2]
14 1 3 2
After:  [1, 1, 0, 2]

Before: [3, 2, 3, 3]
12 1 2 1
After:  [3, 2, 3, 3]

Before: [1, 1, 2, 2]
6 1 0 1
After:  [1, 1, 2, 2]

Before: [2, 1, 3, 0]
10 1 3 0
After:  [1, 1, 3, 0]

Before: [2, 1, 2, 1]
15 3 2 0
After:  [1, 1, 2, 1]

Before: [1, 3, 3, 3]
11 3 3 2
After:  [1, 3, 3, 3]

Before: [3, 3, 2, 2]
8 3 2 3
After:  [3, 3, 2, 0]

Before: [2, 1, 0, 1]
4 0 1 2
After:  [2, 1, 1, 1]

Before: [1, 1, 0, 3]
7 1 3 2
After:  [1, 1, 0, 3]

Before: [2, 3, 3, 2]
12 3 2 3
After:  [2, 3, 3, 2]

Before: [1, 2, 0, 3]
9 0 2 0
After:  [0, 2, 0, 3]

Before: [1, 0, 0, 0]
9 0 2 0
After:  [0, 0, 0, 0]

Before: [2, 2, 3, 3]
12 0 2 0
After:  [2, 2, 3, 3]

Before: [2, 3, 3, 3]
11 3 3 1
After:  [2, 3, 3, 3]

Before: [0, 3, 2, 3]
11 2 2 1
After:  [0, 2, 2, 3]

Before: [2, 2, 3, 3]
12 1 2 0
After:  [2, 2, 3, 3]

Before: [3, 1, 1, 0]
10 1 3 1
After:  [3, 1, 1, 0]

Before: [3, 1, 2, 1]
9 1 3 3
After:  [3, 1, 2, 1]

Before: [1, 2, 1, 3]
7 1 3 3
After:  [1, 2, 1, 0]

Before: [2, 1, 2, 1]
2 1 2 2
After:  [2, 1, 0, 1]

Before: [2, 1, 3, 2]
14 1 3 1
After:  [2, 0, 3, 2]

Before: [1, 1, 1, 3]
6 1 0 3
After:  [1, 1, 1, 1]

Before: [0, 1, 1, 2]
14 1 3 3
After:  [0, 1, 1, 0]

Before: [3, 1, 0, 3]
8 0 2 0
After:  [1, 1, 0, 3]

Before: [1, 0, 2, 1]
15 3 2 0
After:  [1, 0, 2, 1]

Before: [0, 1, 2, 2]
13 3 3 1
After:  [0, 0, 2, 2]

Before: [3, 1, 2, 1]
15 3 2 0
After:  [1, 1, 2, 1]

Before: [1, 1, 1, 2]
6 1 0 0
After:  [1, 1, 1, 2]

Before: [1, 1, 2, 1]
13 3 3 2
After:  [1, 1, 0, 1]

Before: [0, 1, 1, 1]
0 0 0 3
After:  [0, 1, 1, 0]

Before: [0, 1, 0, 0]
10 1 3 3
After:  [0, 1, 0, 1]

Before: [1, 1, 0, 0]
6 1 0 1
After:  [1, 1, 0, 0]

Before: [0, 1, 2, 1]
13 3 3 0
After:  [0, 1, 2, 1]

Before: [1, 3, 2, 3]
3 2 1 0
After:  [1, 3, 2, 3]

Before: [1, 2, 0, 2]
9 0 2 2
After:  [1, 2, 0, 2]

Before: [1, 3, 2, 1]
15 3 2 3
After:  [1, 3, 2, 1]

Before: [2, 2, 0, 3]
7 1 3 2
After:  [2, 2, 0, 3]

Before: [1, 1, 2, 3]
7 1 3 0
After:  [0, 1, 2, 3]

Before: [1, 0, 2, 1]
1 0 2 3
After:  [1, 0, 2, 0]

Before: [1, 2, 2, 2]
1 0 2 0
After:  [0, 2, 2, 2]

Before: [1, 1, 0, 3]
6 1 0 1
After:  [1, 1, 0, 3]

Before: [1, 2, 2, 2]
1 0 2 1
After:  [1, 0, 2, 2]

Before: [1, 1, 2, 3]
7 2 3 2
After:  [1, 1, 0, 3]

Before: [1, 1, 0, 2]
14 1 3 3
After:  [1, 1, 0, 0]

Before: [0, 1, 1, 2]
0 0 0 3
After:  [0, 1, 1, 0]

Before: [1, 0, 1, 1]
13 2 3 3
After:  [1, 0, 1, 0]

Before: [3, 1, 2, 2]
14 1 3 1
After:  [3, 0, 2, 2]

Before: [2, 1, 1, 0]
4 0 1 2
After:  [2, 1, 1, 0]

Before: [0, 2, 1, 1]
13 3 3 0
After:  [0, 2, 1, 1]

Before: [0, 3, 1, 3]
11 3 3 1
After:  [0, 3, 1, 3]

Before: [1, 3, 0, 2]
9 0 2 3
After:  [1, 3, 0, 0]

Before: [3, 2, 2, 3]
7 2 3 0
After:  [0, 2, 2, 3]

Before: [2, 1, 2, 2]
2 1 2 1
After:  [2, 0, 2, 2]

Before: [2, 2, 2, 1]
15 3 2 2
After:  [2, 2, 1, 1]

Before: [3, 3, 1, 1]
13 3 3 3
After:  [3, 3, 1, 0]

Before: [2, 2, 2, 3]
5 2 0 3
After:  [2, 2, 2, 1]

Before: [0, 3, 2, 3]
11 3 3 3
After:  [0, 3, 2, 3]

Before: [2, 3, 2, 0]
3 2 1 2
After:  [2, 3, 1, 0]

Before: [2, 1, 2, 1]
2 1 2 0
After:  [0, 1, 2, 1]

Before: [3, 3, 1, 3]
7 2 3 2
After:  [3, 3, 0, 3]

Before: [3, 0, 2, 0]
11 2 2 0
After:  [2, 0, 2, 0]

Before: [0, 3, 1, 2]
0 0 0 2
After:  [0, 3, 0, 2]

Before: [1, 1, 2, 0]
2 1 2 1
After:  [1, 0, 2, 0]

Before: [3, 1, 3, 2]
12 3 2 3
After:  [3, 1, 3, 2]

Before: [0, 0, 1, 2]
0 0 0 0
After:  [0, 0, 1, 2]

Before: [3, 1, 1, 1]
8 3 1 1
After:  [3, 0, 1, 1]

Before: [0, 0, 2, 1]
0 0 0 0
After:  [0, 0, 2, 1]

Before: [1, 1, 2, 3]
1 0 2 1
After:  [1, 0, 2, 3]

Before: [2, 3, 2, 0]
3 2 1 1
After:  [2, 1, 2, 0]

Before: [1, 3, 3, 2]
12 3 2 1
After:  [1, 2, 3, 2]

Before: [0, 1, 3, 2]
0 0 0 1
After:  [0, 0, 3, 2]

Before: [2, 1, 2, 0]
10 1 3 2
After:  [2, 1, 1, 0]

Before: [2, 2, 3, 2]
12 0 2 0
After:  [2, 2, 3, 2]

Before: [2, 0, 2, 3]
7 2 3 0
After:  [0, 0, 2, 3]

Before: [3, 1, 3, 3]
11 3 3 2
After:  [3, 1, 3, 3]

Before: [3, 1, 3, 0]
10 1 3 3
After:  [3, 1, 3, 1]

Before: [0, 1, 1, 3]
7 2 3 0
After:  [0, 1, 1, 3]

Before: [1, 1, 2, 0]
1 0 2 2
After:  [1, 1, 0, 0]

Before: [1, 1, 1, 0]
10 1 3 3
After:  [1, 1, 1, 1]

Before: [1, 1, 3, 2]
13 3 3 3
After:  [1, 1, 3, 0]

Before: [2, 0, 3, 1]
8 0 1 0
After:  [1, 0, 3, 1]

Before: [3, 2, 2, 3]
3 2 0 0
After:  [1, 2, 2, 3]

Before: [0, 3, 2, 3]
0 0 0 2
After:  [0, 3, 0, 3]

Before: [2, 2, 1, 2]
13 3 3 3
After:  [2, 2, 1, 0]

Before: [0, 2, 3, 3]
5 3 2 0
After:  [1, 2, 3, 3]

Before: [2, 1, 2, 2]
2 1 2 3
After:  [2, 1, 2, 0]

Before: [2, 1, 0, 3]
4 0 1 1
After:  [2, 1, 0, 3]

Before: [2, 1, 1, 0]
10 1 3 0
After:  [1, 1, 1, 0]

Before: [2, 3, 3, 2]
12 3 2 1
After:  [2, 2, 3, 2]

Before: [3, 2, 3, 1]
5 2 3 2
After:  [3, 2, 0, 1]

Before: [3, 3, 3, 1]
5 2 3 1
After:  [3, 0, 3, 1]

Before: [1, 1, 3, 3]
7 1 3 1
After:  [1, 0, 3, 3]

Before: [2, 1, 2, 3]
2 1 2 2
After:  [2, 1, 0, 3]

Before: [3, 1, 2, 3]
2 1 2 0
After:  [0, 1, 2, 3]

Before: [3, 1, 3, 1]
5 2 3 0
After:  [0, 1, 3, 1]

Before: [0, 2, 3, 3]
12 1 2 2
After:  [0, 2, 2, 3]

Before: [1, 0, 2, 2]
1 0 2 0
After:  [0, 0, 2, 2]

Before: [1, 1, 1, 2]
6 1 0 3
After:  [1, 1, 1, 1]

Before: [0, 3, 3, 1]
13 3 3 0
After:  [0, 3, 3, 1]

Before: [2, 1, 2, 1]
4 0 1 3
After:  [2, 1, 2, 1]

Before: [1, 1, 1, 3]
7 2 3 1
After:  [1, 0, 1, 3]

Before: [0, 3, 1, 2]
0 0 0 0
After:  [0, 3, 1, 2]

Before: [3, 3, 2, 2]
4 0 2 1
After:  [3, 1, 2, 2]

Before: [0, 3, 2, 2]
3 2 1 2
After:  [0, 3, 1, 2]

Before: [3, 1, 1, 3]
7 2 3 3
After:  [3, 1, 1, 0]

Before: [2, 1, 2, 1]
15 3 2 1
After:  [2, 1, 2, 1]

Before: [1, 1, 1, 0]
6 1 0 3
After:  [1, 1, 1, 1]

Before: [1, 3, 3, 2]
12 3 2 2
After:  [1, 3, 2, 2]

Before: [3, 1, 1, 2]
14 1 3 1
After:  [3, 0, 1, 2]

Before: [0, 2, 2, 3]
0 0 0 0
After:  [0, 2, 2, 3]

Before: [1, 1, 2, 3]
6 1 0 3
After:  [1, 1, 2, 1]

Before: [1, 1, 1, 0]
6 1 0 1
After:  [1, 1, 1, 0]

Before: [2, 3, 1, 3]
7 2 3 3
After:  [2, 3, 1, 0]

Before: [0, 1, 3, 0]
0 0 0 0
After:  [0, 1, 3, 0]

Before: [3, 0, 0, 3]
11 3 3 0
After:  [3, 0, 0, 3]

Before: [3, 1, 2, 1]
9 1 3 0
After:  [1, 1, 2, 1]

Before: [3, 0, 2, 1]
15 3 2 0
After:  [1, 0, 2, 1]

Before: [1, 1, 1, 1]
6 1 0 1
After:  [1, 1, 1, 1]"""

input2 = """\
1 2 3 0
1 0 0 3
0 2 0 2
6 2 3 2
8 3 2 0
0 0 3 0
10 1 0 1
15 1 1 2
1 3 3 3
1 1 3 0
1 2 0 1
1 1 3 0
0 0 2 0
10 0 2 2
15 2 0 3
1 0 2 1
1 1 1 0
1 3 0 2
0 0 2 0
0 0 2 0
10 0 3 3
15 3 3 1
1 0 0 2
1 3 0 0
1 0 1 3
13 2 0 0
0 0 1 0
10 1 0 1
15 1 2 0
1 2 2 2
1 1 3 1
12 2 3 3
0 3 1 3
0 3 1 3
10 0 3 0
15 0 1 1
1 3 1 2
1 0 1 3
1 3 2 0
2 0 2 2
0 2 1 2
10 1 2 1
15 1 1 2
0 2 0 0
6 0 1 0
0 0 0 1
6 1 2 1
1 2 1 3
12 1 3 0
0 0 3 0
10 0 2 2
15 2 1 0
1 3 3 1
1 0 2 3
1 3 1 2
8 3 2 3
0 3 3 3
10 0 3 0
15 0 2 3
1 3 1 0
1 0 2 2
1 0 2 1
13 2 0 0
0 0 3 0
10 0 3 3
1 3 2 2
0 0 0 0
6 0 3 0
1 2 1 1
11 1 0 0
0 0 3 0
10 3 0 3
1 1 3 0
0 3 0 1
6 1 1 1
1 2 2 2
15 0 2 1
0 1 2 1
10 3 1 3
15 3 0 2
1 3 2 1
1 2 2 3
1 0 2 0
14 1 3 1
0 1 3 1
0 1 2 1
10 2 1 2
15 2 3 0
1 3 2 2
1 3 1 1
2 1 2 3
0 3 3 3
10 0 3 0
15 0 3 1
0 3 0 3
6 3 1 3
1 1 3 0
1 2 0 2
15 0 2 0
0 0 1 0
10 0 1 1
15 1 1 0
1 3 2 1
1 0 3 2
1 2 3 2
0 2 1 2
10 2 0 0
15 0 2 1
1 1 3 0
1 0 3 3
1 2 3 2
7 3 2 3
0 3 3 3
10 3 1 1
15 1 2 0
0 2 0 2
6 2 0 2
1 3 0 3
1 0 0 1
2 3 2 3
0 3 1 3
10 3 0 0
15 0 2 3
1 3 1 0
0 3 0 1
6 1 3 1
2 0 2 2
0 2 3 2
10 2 3 3
15 3 0 2
1 2 2 0
1 2 0 3
0 1 0 1
6 1 2 1
5 0 3 0
0 0 2 0
10 2 0 2
15 2 3 0
1 0 1 2
0 1 0 1
6 1 1 1
1 1 2 3
0 3 2 2
0 2 3 2
0 2 2 2
10 2 0 0
15 0 1 2
1 1 2 0
1 0 1 3
1 3 0 1
6 0 1 0
0 0 1 0
0 0 3 0
10 2 0 2
15 2 0 1
0 1 0 0
6 0 0 0
1 2 2 2
7 3 2 3
0 3 2 3
0 3 2 3
10 3 1 1
1 0 2 3
12 2 3 0
0 0 2 0
10 1 0 1
0 2 0 3
6 3 3 3
0 0 0 2
6 2 0 2
0 3 0 0
6 0 2 0
2 3 2 3
0 3 1 3
10 3 1 1
1 2 3 3
1 3 3 2
1 1 3 0
9 0 3 2
0 2 1 2
10 2 1 1
15 1 1 3
1 3 3 2
1 0 0 1
6 0 1 1
0 1 3 1
10 1 3 3
15 3 2 2
1 3 2 3
1 1 0 1
10 0 0 1
0 1 1 1
10 2 1 2
15 2 1 1
1 0 2 2
1 3 1 0
0 0 0 3
6 3 2 3
8 2 3 3
0 3 2 3
10 3 1 1
15 1 0 2
1 2 0 0
1 1 1 3
0 2 0 1
6 1 3 1
4 0 3 1
0 1 2 1
0 1 2 1
10 2 1 2
1 3 1 1
1 2 3 3
3 0 1 0
0 0 2 0
10 2 0 2
15 2 3 1
1 0 3 2
1 3 3 0
8 2 3 0
0 0 2 0
0 0 2 0
10 0 1 1
15 1 3 0
1 2 2 2
1 3 2 1
1 0 2 3
7 3 2 1
0 1 2 1
10 0 1 0
15 0 0 3
0 0 0 2
6 2 0 2
1 3 1 1
1 1 1 0
6 0 1 0
0 0 3 0
0 0 2 0
10 3 0 3
15 3 3 1
1 1 2 0
0 2 0 2
6 2 2 2
1 0 1 3
7 3 2 2
0 2 1 2
10 2 1 1
15 1 1 2
0 1 0 0
6 0 2 0
1 2 2 1
1 1 1 3
4 0 3 1
0 1 2 1
10 1 2 2
0 1 0 3
6 3 2 3
0 1 0 1
6 1 1 1
1 1 1 0
10 1 0 1
0 1 2 1
10 1 2 2
15 2 3 3
0 3 0 1
6 1 3 1
0 1 0 2
6 2 0 2
6 0 1 1
0 1 3 1
10 3 1 3
15 3 1 0
1 2 0 3
0 2 0 1
6 1 3 1
8 2 3 3
0 3 3 3
10 0 3 0
1 1 1 3
1 0 0 1
0 3 2 3
0 3 1 3
10 3 0 0
15 0 3 1
1 1 3 3
1 3 1 0
0 2 0 2
6 2 2 2
11 2 0 0
0 0 1 0
10 1 0 1
15 1 3 0
1 0 0 3
0 2 0 2
6 2 3 2
1 1 3 1
0 1 2 3
0 3 1 3
0 3 3 3
10 0 3 0
15 0 1 2
1 1 3 0
0 2 0 1
6 1 0 1
1 1 0 3
6 0 1 1
0 1 3 1
10 2 1 2
15 2 3 0
1 3 2 1
1 0 2 2
6 3 1 2
0 2 3 2
10 2 0 0
1 0 3 1
1 0 3 3
0 3 0 2
6 2 2 2
7 3 2 1
0 1 3 1
10 0 1 0
15 0 2 1
1 1 3 3
0 3 0 0
6 0 3 0
0 2 0 2
6 2 0 2
1 2 3 3
0 3 1 3
10 1 3 1
15 1 1 2
1 2 3 3
1 2 3 1
14 0 1 0
0 0 1 0
10 2 0 2
15 2 0 0
0 0 0 3
6 3 0 3
1 2 0 2
1 0 2 1
7 3 2 2
0 2 1 2
0 2 3 2
10 0 2 0
15 0 3 3
1 2 2 2
1 2 2 1
0 1 0 0
6 0 3 0
11 1 0 1
0 1 3 1
10 1 3 3
15 3 3 1
1 2 1 0
0 0 0 3
6 3 1 3
1 0 0 2
4 0 3 3
0 3 1 3
10 3 1 1
15 1 1 3
1 1 3 0
1 1 1 1
10 1 0 2
0 2 3 2
10 2 3 3
15 3 1 1
1 2 1 3
1 2 2 2
12 2 3 3
0 3 3 3
10 1 3 1
15 1 3 2
1 2 1 1
1 2 2 3
1 3 2 0
14 0 3 1
0 1 1 1
10 1 2 2
1 2 0 1
11 1 0 1
0 1 3 1
0 1 2 1
10 1 2 2
1 2 2 1
14 0 1 1
0 1 2 1
0 1 2 1
10 1 2 2
15 2 0 0
1 0 2 2
1 3 3 1
0 0 0 3
6 3 3 3
2 3 2 1
0 1 1 1
10 0 1 0
15 0 1 1
1 0 2 3
0 1 0 2
6 2 3 2
1 1 3 0
8 3 2 3
0 3 2 3
0 3 3 3
10 3 1 1
15 1 3 2
1 2 3 3
1 2 3 1
0 0 0 0
6 0 2 0
5 0 3 3
0 3 1 3
10 2 3 2
15 2 0 3
1 1 0 0
0 3 0 2
6 2 0 2
0 0 2 0
0 0 2 0
10 0 3 3
15 3 3 1
0 1 0 0
6 0 3 0
1 2 1 3
1 1 3 2
2 0 2 3
0 3 1 3
0 3 2 3
10 1 3 1
1 1 1 0
1 2 3 3
1 2 3 2
15 0 2 3
0 3 1 3
10 1 3 1
1 3 3 0
1 1 2 3
3 2 0 3
0 3 1 3
0 3 2 3
10 1 3 1
15 1 2 0
1 3 2 2
1 1 0 3
1 3 3 1
2 1 2 3
0 3 3 3
0 3 3 3
10 3 0 0
1 0 0 3
0 1 0 1
6 1 2 1
1 2 3 2
7 3 2 1
0 1 2 1
10 0 1 0
15 0 3 2
1 2 0 0
1 2 0 3
1 3 2 1
5 0 3 1
0 1 3 1
0 1 1 1
10 1 2 2
15 2 3 1
1 3 0 3
1 1 2 0
0 1 0 2
6 2 0 2
2 3 2 3
0 3 3 3
10 1 3 1
15 1 1 2
1 3 0 1
1 2 1 3
1 0 2 0
14 1 3 3
0 3 3 3
0 3 3 3
10 3 2 2
15 2 1 1
1 0 2 2
1 2 3 0
0 0 0 3
6 3 1 3
0 3 2 0
0 0 3 0
10 1 0 1
15 1 0 3
1 2 2 2
1 1 3 0
1 3 0 1
10 0 0 0
0 0 3 0
10 3 0 3
15 3 0 0
0 3 0 2
6 2 0 2
1 1 1 3
6 3 1 3
0 3 1 3
0 3 3 3
10 0 3 0
15 0 1 1
0 0 0 2
6 2 2 2
1 1 2 3
1 2 0 0
4 0 3 3
0 3 1 3
0 3 2 3
10 1 3 1
1 0 1 0
1 0 0 2
1 2 3 3
8 2 3 3
0 3 2 3
10 1 3 1
1 3 3 0
1 2 1 3
14 0 3 2
0 2 3 2
10 1 2 1
15 1 0 2
1 2 0 0
1 3 1 1
3 0 1 3
0 3 3 3
10 2 3 2
15 2 2 3
1 3 0 2
14 1 0 2
0 2 3 2
10 3 2 3
15 3 3 1
1 0 2 0
1 0 2 2
0 1 0 3
6 3 2 3
1 2 0 0
0 0 1 0
0 0 1 0
10 1 0 1
15 1 3 3
1 3 3 1
1 2 3 0
1 1 1 2
14 1 0 1
0 1 3 1
10 1 3 3
15 3 0 2
1 0 2 1
1 2 1 3
5 0 3 1
0 1 1 1
10 2 1 2
15 2 3 1
1 0 1 3
1 1 0 0
1 2 1 2
7 3 2 0
0 0 3 0
0 0 2 0
10 1 0 1
0 2 0 0
6 0 3 0
1 1 2 3
1 3 3 2
0 3 2 0
0 0 2 0
10 0 1 1
15 1 0 0
1 0 3 2
0 1 0 1
6 1 0 1
6 3 1 1
0 1 1 1
10 1 0 0
15 0 1 3
1 1 0 0
1 0 2 1
6 0 1 1
0 1 2 1
0 1 3 1
10 3 1 3
15 3 1 0
1 0 1 1
1 2 3 3
8 2 3 3
0 3 1 3
0 3 1 3
10 3 0 0
15 0 0 1
1 1 1 3
0 0 0 0
6 0 2 0
1 2 0 2
9 3 0 3
0 3 3 3
0 3 1 3
10 1 3 1
1 3 3 2
1 2 2 3
13 0 2 2
0 2 1 2
10 2 1 1
15 1 0 0
1 0 0 3
1 1 3 1
1 2 2 2
7 3 2 3
0 3 2 3
0 3 3 3
10 3 0 0
15 0 2 1
1 1 2 0
1 3 2 2
1 2 0 3
9 0 3 3
0 3 3 3
10 3 1 1
1 1 0 3
1 2 2 0
9 3 0 2
0 2 3 2
10 1 2 1
1 0 0 2
9 3 0 0
0 0 3 0
10 1 0 1
15 1 3 2
1 2 0 1
1 2 2 0
9 3 0 0
0 0 2 0
10 2 0 2
1 2 2 3
1 2 1 0
12 1 3 3
0 3 1 3
10 3 2 2
1 1 0 0
0 1 0 3
6 3 2 3
9 0 3 1
0 1 1 1
10 1 2 2
15 2 2 0
0 2 0 2
6 2 3 2
1 3 0 1
14 1 3 2
0 2 2 2
10 0 2 0
15 0 1 2
1 2 1 0
0 1 0 1
6 1 1 1
1 1 0 3
4 0 3 3
0 3 2 3
10 2 3 2
15 2 0 0
0 3 0 3
6 3 0 3
1 2 3 2
7 3 2 1
0 1 3 1
10 1 0 0
15 0 2 1
1 2 0 0
0 2 0 3
6 3 3 3
1 3 2 2
13 0 2 0
0 0 2 0
0 0 1 0
10 1 0 1
1 2 3 2
1 0 3 3
1 0 1 0
12 2 3 2
0 2 2 2
10 1 2 1
15 1 1 2
1 0 0 1
1 2 1 3
1 2 3 0
5 0 3 3
0 3 2 3
10 3 2 2
15 2 1 3
1 3 1 0
1 2 3 2
3 2 0 1
0 1 2 1
10 1 3 3
15 3 1 1
0 1 0 0
6 0 2 0
0 3 0 3
6 3 1 3
4 0 3 2
0 2 1 2
10 2 1 1
15 1 0 3
1 1 0 0
1 0 0 1
1 1 2 2
6 0 1 1
0 1 3 1
10 1 3 3
15 3 0 0
0 1 0 1
6 1 2 1
1 3 1 3
1 0 0 2
14 3 1 2
0 2 1 2
10 0 2 0
15 0 3 3
0 3 0 2
6 2 1 2
1 3 0 0
0 1 0 1
6 1 3 1
2 0 2 1
0 1 2 1
10 1 3 3
15 3 3 1
1 2 0 0
1 2 2 2
1 1 2 3
4 0 3 0
0 0 2 0
10 0 1 1
15 1 1 3
1 3 0 1
1 1 2 0
1 0 2 2
0 0 2 1
0 1 2 1
10 3 1 3
1 2 0 1
1 2 3 2
15 0 2 0
0 0 1 0
10 0 3 3
15 3 1 0
1 3 1 1
0 1 0 3
6 3 1 3
6 3 1 3
0 3 3 3
10 0 3 0
15 0 3 1
1 0 0 3
1 3 0 0
11 2 0 2
0 2 1 2
10 1 2 1
1 0 1 2
1 0 0 0
1 3 0 2
0 2 3 2
10 2 1 1
1 1 2 0
1 0 3 2
1 1 3 3
0 3 2 3
0 3 2 3
10 1 3 1
15 1 0 3
1 2 3 2
1 3 0 0
1 3 0 1
3 2 1 0
0 0 3 0
10 0 3 3
15 3 1 2
1 2 1 1
1 0 1 3
0 1 0 0
6 0 3 0
14 0 1 3
0 3 1 3
0 3 2 3
10 2 3 2
15 2 0 1
0 2 0 3
6 3 0 3
1 3 0 2
1 2 1 0
12 0 3 3
0 3 3 3
10 3 1 1
15 1 3 0
0 3 0 3
6 3 0 3
1 1 3 1
0 1 2 2
0 2 1 2
10 0 2 0
15 0 2 2
1 2 0 3
1 2 2 0
5 0 3 1
0 1 3 1
10 1 2 2
15 2 2 1
1 3 2 2
1 3 1 3
2 3 2 0
0 0 1 0
0 0 1 0
10 0 1 1
0 1 0 2
6 2 2 2
1 2 0 3
1 2 0 0
12 2 3 2
0 2 2 2
0 2 1 2
10 2 1 1
15 1 3 3
1 1 1 0
1 3 2 2
1 2 1 1
11 1 2 0
0 0 3 0
10 0 3 3
15 3 2 1
1 2 2 0
1 3 2 3
2 3 2 2
0 2 3 2
0 2 2 2
10 2 1 1
1 0 1 2
1 1 2 3
4 0 3 2
0 2 2 2
10 2 1 1
15 1 3 0
0 2 0 2
6 2 2 2
1 0 2 3
1 0 0 1
7 3 2 3
0 3 1 3
10 3 0 0
1 2 1 3
1 2 3 1
1 1 0 2
12 1 3 2
0 2 1 2
0 2 2 2
10 0 2 0
1 0 0 2
8 2 3 1
0 1 2 1
10 1 0 0
15 0 1 3
1 2 3 2
0 0 0 0
6 0 1 0
1 3 0 1
15 0 2 1
0 1 2 1
10 3 1 3
15 3 2 1
1 2 1 0
1 1 0 2
0 2 0 3
6 3 2 3
5 0 3 2
0 2 2 2
10 2 1 1
15 1 1 0
1 1 2 3
0 0 0 1
6 1 0 1
0 1 0 2
6 2 1 2
10 3 3 2
0 2 1 2
10 0 2 0
15 0 2 2
1 2 3 0
1 2 1 1
1 2 0 3
12 1 3 0
0 0 2 0
10 2 0 2
0 1 0 1
6 1 3 1
1 1 1 3
1 0 0 0
6 3 1 3
0 3 2 3
10 2 3 2
15 2 1 0
1 3 1 2
1 0 1 3
8 3 2 2
0 2 2 2
10 0 2 0
15 0 1 2
1 1 2 1
1 1 0 0
1 1 0 3
10 0 0 0
0 0 2 0
0 0 3 0
10 0 2 2
15 2 0 0
0 0 0 2
6 2 2 2
0 3 0 1
6 1 2 1
10 3 3 3
0 3 1 3
0 3 1 3
10 3 0 0
15 0 0 1
1 3 0 0
1 3 2 3
3 2 0 2
0 2 3 2
10 2 1 1
15 1 1 3
1 1 3 1
1 3 1 2
0 1 2 1
0 1 2 1
10 3 1 3
15 3 2 0"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")

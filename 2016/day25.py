import unittest
from textwrap import dedent

import sys
from hamcrest import assert_that, is_

DEFAULT_REGISTRY = lambda: {'a': 0, 'b': 0, 'c': 0, 'd': 0}


def compute(data):
    length_assertion = 50
    program = data.strip().split("\n")
    expected_output = [0, 1] * int(length_assertion / 2)
    tramission_is_wrong_or_very_good = lambda i: expected_output[:len(i.transmitted)] != i.transmitted

    index = -1
    output = []
    while output[:length_assertion] != expected_output:
        index += 1

        registry = DEFAULT_REGISTRY()
        registry['a'] = index
        interpreter = Interpreter(program, registry, should_stop=tramission_is_wrong_or_very_good)
        interpreter.run()
        output = interpreter.transmitted
        print("#{} Got output: {}".format(index, output))


    return index




class Interpreter(object):
    def __init__(self, program, registry=None, should_stop=None):
        self.registry = registry or DEFAULT_REGISTRY()
        self.program = split(program)
        self.line = 0
        self.transmitted = []
        self.should_stop = should_stop if should_stop is not None else lambda _: False

    def run(self):
        while self.line < len(self.program):
            cmd = self.program[self.line]

            getattr(self, "do_{}".format(cmd[0]))(*cmd[1:])

            if self.should_stop(self):
                return

            self.line += 1

    def do_cpy(self, source, target):
        if target in self.registry:
            self.registry[target] = self._read(source)

    def do_inc(self, target):
        self.registry[target] += 1

    def do_dec(self, target):
        self.registry[target] -= 1

    def do_jnz(self, source, target):
        if self._read(source) > 0:
            if not self.optimize_loop(source, target):
                self.line += self._read(target) - 1

    def do_tgl(self, source):
        target_line = self.line + self._read(source)
        if 0 <= target_line < len(self.program):
            cmd = self.program[target_line]
            if len(cmd) == 3:
                if cmd[0] == "jnz":
                    cmd[0] = "cpy"
                else:
                    cmd[0] = "jnz"
            else:
                if cmd[0] == "inc":
                    cmd[0] = "dec"
                else:
                    cmd[0] = "inc"
            self.program[target_line] = cmd

    def do_out(self, source):
        self.transmitted.append(self._read(source))

    def _read(self, source):
        if source in self.registry:
            return self.registry[source]

        return int(source)

    def optimize_loop(self, condition, lines):
        try:
            if condition not in self.registry or lines in self.registry:
                raise CantOptimize

            lines = int(lines)

            if lines == -5: #multiplication
                operand1 = self._get_op(self.program[self.line - 1])
                if operand1[0] != condition:
                    raise CantOptimize

                multiplier = self._get_jnz(self.program[self.line - 2])

                surrogate = None
                base = None
                for line in self.program[self.line - 4:self.line - 2]:
                    if line[0] in ("inc", "dec") and line[1] == multiplier[0]:
                        surrogate = self._get_op(line)
                    else:
                        base = self._get_op(line)

                if surrogate is None or base is None:
                    raise CantOptimize

                operand2, target_surrogate = self._get_cpy(self.program[self.line - 5])

                if surrogate[0] != target_surrogate:
                    raise CantOptimize

                self.registry[base[0]] += (self._read(operand1[0]) * self._read(operand2)) * base[1]
                self.registry[operand1[0]] = 0
                self.registry[target_surrogate] = 0
                return True
            elif lines == -2: #addition
                base = None
                modifier = None
                for line in self.program[self.line - 2:self.line]:
                    if line[0] in ("inc", "dec") and line[1] == condition:
                        modifier = self._get_op(line)
                    else:
                        base = self._get_op(line)

                if base is None or modifier is None:
                    raise CantOptimize

                self.registry[base[0]] += self.registry[condition] * - modifier[1]
                self.registry[condition] = 0
                return True

        except CantOptimize:
            pass
        return False

    def _get_op(self, line):
        if line[0] == "inc":
            return line[1], 1
        elif line[0] == "dec":
            return line[1], -1
        else:
            raise CantOptimize

    def _get_jnz(self, line):
        if line[0] != "jnz":
            raise CantOptimize
        if line[1] not in self.registry or line[2] in self.registry:
            raise CantOptimize
        return line[1], int(line[2])

    def _get_cpy(self, line):
        if line[0] != "cpy":
            raise CantOptimize
        if line[2] not in self.registry:
            raise CantOptimize
        return line[1], line[2]


class CantOptimize(Exception):
    pass


def is_int(val):
    try:
        int(val)
    except ValueError:
        return False
    return True


def split(l):
    return [e.split() for e in l]


class CPYTest(unittest.TestCase):
    def test_copy_int(self):
        interpreter = Interpreter([
            "cpy 1 a"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(1))

    def test_copy_registry(self):
        interpreter = Interpreter([
            "cpy 2 b",
            "cpy b c",
        ])

        interpreter.run()

        assert_that(interpreter.registry['b'], is_(2))
        assert_that(interpreter.registry['c'], is_(2))


class IncDecTest(unittest.TestCase):
    def test_inc(self):
        interpreter = Interpreter([
            "inc a",
            "inc a"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(2))

    def test_dev(self):
        interpreter = Interpreter([
            "dec a",
            "dec a"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(-2))


class JnzTest(unittest.TestCase):
    def test_jump_if_true(self):
        interpreter = Interpreter([
            "inc a",
            "jnz a 2",
            "inc a",
            "dec a"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(0))

    def test_dont_jump_if_0(self):
        interpreter = Interpreter([
            "jnz a 2",
            "inc a"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(1))

    def test_jump_backwards(self):
        interpreter = Interpreter([
            "cpy 2 a",
            "dec a",
            "jnz a -1",
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(0))

    def test_jump_past_final_line_ends(self):
        interpreter = Interpreter([
            "inc a",
            "jnz a 2"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(1))

    def test_can_read_int(self):
        interpreter = Interpreter([
            "jnz 1 2",
            "inc a"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(0))

    def test_can_jump_of_var(self):
        interpreter = Interpreter([
            "inc a",
            "inc a",
            "jnz 1 a",
            "inc a"
        ])

        interpreter.run()

        assert_that(interpreter.registry['a'], is_(2))


class TglTest(unittest.TestCase):
    def test_tgl_one_args(self):
        interpreter = Interpreter([
            "tgl a",
            "tgl 2",
            "tgl 2",
            "dec a",
            "inc a",
        ])

        interpreter.run()

        assert_that(interpreter.program, is_([l.split() for l in [
            "inc a",
            "tgl 2",
            "tgl 2",
            "inc a",
            "dec a",
        ]]))

    def test_tgl_two_args(self):
        interpreter = Interpreter([
            "cpy a b",
            "tgl -1",
            "tgl 1",
            "jnz 0 1",
        ])

        interpreter.run()

        assert_that(interpreter.program, is_([l.split() for l in [
            "jnz a b",
            "tgl -1",
            "tgl 1",
            "cpy 0 1",
        ]]))

    def test_out_of_bound(self):
        interpreter = Interpreter([
            "tgl -1",
            "tgl 1",
        ])

        interpreter.run()


class OutTest(unittest.TestCase):
    def test_transmits(self):
        interpreter = Interpreter([
            "out 1",
            "out a",
            "inc a",
            "out a",
        ])

        interpreter.run()

        assert_that(interpreter.transmitted, is_([1, 0, 1]))


class ShouldStopTest(unittest.TestCase):
    def test_transmits(self):
        interpreter = Interpreter([
            "inc a",
            "inc a",
            "inc a",
        ])
        interpreter.should_stop = lambda intrprtr: intrprtr.line == 1
        interpreter.run()

        assert_that(interpreter.registry['a'], is_(2))


class OptimizationTest(unittest.TestCase):
    def test_addition(self):
        interpreter1 = Interpreter([
            "inc c",
            "inc a",
            "dec b",
            "jnz b -2",
            "inc c",
        ], {'a': 1000000, 'b': 1000000, 'c': 0})

        interpreter1.run()

        assert_that(interpreter1.registry, is_({'a': 2000000, 'b': 0, 'c': 2}))

    def test_multiplication10(self):
        interpreter1 = Interpreter([
            "inc e",
            "cpy a d",
            "dec b",
            "cpy b c",
            "inc a",
            "dec c",
            "jnz c -2",
            "dec d",
            "jnz d -5",
            "inc e",
        ], {'a': 10, 'b': 10, 'c': 0, 'd': 0, 'e': 0})

        interpreter1.run()

        assert_that(interpreter1.registry, is_({'a': 100, 'b': 9, 'c': 0, 'd': 0, 'e': 2}))

    def test_multiplication100(self):
        interpreter1 = Interpreter([
            "inc e",
            "cpy a d",
            "dec b",
            "cpy b c",
            "inc a",
            "dec c",
            "jnz c -2",
            "dec d",
            "jnz d -5",
            "inc e",
        ], {'a': 100, 'b': 100, 'c': 0, 'd': 0, 'e': 0})

        interpreter1.run()

        assert_that(interpreter1.registry, is_({'a': 10000, 'b': 99, 'c': 0, 'd': 0, 'e': 2}))

    def test_multiplication10000000(self):
        interpreter1 = Interpreter([
            "inc e",
            "cpy a d",
            "dec b",
            "cpy b c",
            "inc a",
            "dec c",
            "jnz c -2",
            "dec d",
            "jnz d -5",
            "inc e",
        ], {'a': 10000000, 'b': 10000000, 'c': 0, 'd': 0, 'e': 0})

        interpreter1.run()

        assert_that(interpreter1.registry, is_({'a': 100000000000000, 'b': 9999999, 'c': 0, 'd': 0, 'e': 2}))

    def test_multiplication_inverted_sub(self):
        interpreter1 = Interpreter([
            "inc e",
            "cpy a d",
            "dec b",
            "cpy b c",
            "dec c",
            "inc a",
            "jnz c -2",
            "dec d",
            "jnz d -5",
            "inc e",
        ], {'a': 10000000, 'b': 10000000, 'c': 0, 'd': 0, 'e': 0})

        interpreter1.run()

        assert_that(interpreter1.registry, is_({'a': 100000000000000, 'b': 9999999, 'c': 0, 'd': 0, 'e': 2}))


puzzle_input = dedent("""
    cpy a d
    cpy 14 c
    cpy 182 b
    inc d
    dec b
    jnz b -2
    dec c
    jnz c -5
    cpy d a
    jnz 0 0
    cpy a b
    cpy 0 a
    cpy 2 c
    jnz b 2
    jnz 1 6
    dec b
    dec c
    jnz c -4
    inc a
    jnz 1 -7
    cpy 2 b
    jnz c 2
    jnz 1 4
    dec b
    dec c
    jnz 1 -4
    jnz 0 0
    out b
    jnz a -19
    jnz 1 -21""")

if __name__ == '__main__':

    if sys.argv[1] == "1":
        result = compute(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

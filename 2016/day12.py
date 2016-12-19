import unittest
from textwrap import dedent

import sys
from hamcrest import assert_that, is_

DEFAULT_REGISTRY = lambda: {'a': 0, 'b': 0, 'c': 0, 'd': 0}


def compute(data):
    interpreter = Interpreter()

    interpreter.run(data.split("\n"))

    return interpreter.registry['a']


class Interpreter(object):
    def __init__(self, registry=None):
        self.registry = registry or DEFAULT_REGISTRY()
        self.line = 0

    def run(self, program):
        while self.line < len(program):
            if program[self.line]:
                cmd = program[self.line].split()

                getattr(self, "do_{}".format(cmd[0]))(*cmd[1:])

            self.line += 1

    def do_cpy(self, source, target):
        self.registry[target] = self._read(source)

    def do_inc(self, target):
        self.registry[target] += 1

    def do_dec(self, target):
        self.registry[target] -= 1

    def do_jnz(self, source, target):
        if self._read(source) > 0:
            self.line += int(target) - 1

    def _read(self, source):
        if source in self.registry:
            return self.registry[source]

        return int(source)


class CPYTest(unittest.TestCase):
    def test_copy_int(self):
        interpreter = Interpreter()

        interpreter.run([
            "cpy 1 a"
        ])

        assert_that(interpreter.registry['a'], is_(1))

    def test_copy_registry(self):
        interpreter = Interpreter()

        interpreter.run([
            "cpy 2 b",
            "cpy b c",
        ])

        assert_that(interpreter.registry['b'], is_(2))
        assert_that(interpreter.registry['c'], is_(2))


class IncDecTest(unittest.TestCase):
    def test_inc(self):
        interpreter = Interpreter()

        interpreter.run([
            "inc a",
            "inc a"
        ])

        assert_that(interpreter.registry['a'], is_(2))

    def test_dev(self):
        interpreter = Interpreter()

        interpreter.run([
            "dec a",
            "dec a"
        ])

        assert_that(interpreter.registry['a'], is_(-2))


class JnzTest(unittest.TestCase):
    def test_jump_if_true(self):
        interpreter = Interpreter()

        interpreter.run([
            "inc a",
            "jnz a 2",
            "inc a",
            "dec a"
        ])

        assert_that(interpreter.registry['a'], is_(0))

    def test_dont_jump_if_0(self):
        interpreter = Interpreter()

        interpreter.run([
            "jnz a 2",
            "inc a"
        ])

        assert_that(interpreter.registry['a'], is_(1))

    def test_jump_backwards(self):
        interpreter = Interpreter()

        interpreter.run([
            "cpy 2 a",
            "dec a",
            "jnz a -1",
        ])

        assert_that(interpreter.registry['a'], is_(0))

    def test_jump_past_final_line_ends(self):
        interpreter = Interpreter()

        interpreter.run([
            "inc a",
            "jnz a 2"
        ])

        assert_that(interpreter.registry['a'], is_(1))

    def test_can_read_int(self):
        interpreter = Interpreter()

        interpreter.run([
            "jnz 1 2",
            "inc a"
        ])

        assert_that(interpreter.registry['a'], is_(0))


class ComputeTest(unittest.TestCase):
    def test_official(self):
        r = compute(dedent("""
            cpy 41 a
            inc a
            inc a
            dec a
            jnz a 2
            dec a"""))
        assert_that(r, is_(42))


if __name__ == '__main__':
    puzzle_input = dedent("""
        cpy 1 a
        cpy 1 b
        cpy 26 d
        jnz c 2
        jnz 1 5
        cpy 7 c
        inc d
        dec c
        jnz c -2
        cpy a c
        inc a
        dec b
        jnz b -2
        cpy c b
        dec d
        jnz d -6
        cpy 13 c
        cpy 14 d
        inc a
        dec d
        jnz d -2
        dec c
        jnz c -5
        """)

    if sys.argv[1] == "1":
        result = compute(puzzle_input)
    else:
        DEFAULT_REGISTRY = lambda: {'a': 0, 'b': 0, 'c': 1, 'd': 0}
        result = compute(puzzle_input)

    print("Result is {}".format(result))

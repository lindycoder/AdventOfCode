import sys
import unittest
from collections import defaultdict, deque
from textwrap import dedent

from hamcrest import assert_that, is_

from y2017.duet import SetValue, AddValue, MultiplyValue, ModValue, JumpOnPositive, Send, Receive, run_program, DONE, WAITING, \
    STILL_WAITING


class CountingDeque(deque):
    def __init__(self, iterable=(), maxlen=None):
        self.added = 0
        super().__init__(iterable, maxlen)

    def append(self, *args, **kwargs):
        self.added += 1
        return super().append(*args, **kwargs)


def compute(data):
    sound_queue = deque()
    fake_queue = deque()

    program = run_program(defaultdict(lambda: 0), data, {
        "snd": Send(sound_queue),
        "set": SetValue(),
        "add": AddValue(),
        "mul": MultiplyValue(),
        "mod": ModValue(),
        "rcv": Receive(fake_queue),
        "jgz": JumpOnPositive(),
    })

    while True:
        state = next(program)

        if state == WAITING:
            return sound_queue.pop()


def compute2(data):
    program_0_queue = CountingDeque()
    program_1_queue = CountingDeque()

    programs = [
        run_program(defaultdict(lambda: 0, {'p': 0}), data, {
            "snd": Send(program_1_queue),
            "set": SetValue(),
            "add": AddValue(),
            "mul": MultiplyValue(),
            "mod": ModValue(),
            "rcv": Receive(program_0_queue),
            "jgz": JumpOnPositive(),
        }),
        run_program(defaultdict(lambda: 0, {'p': 1}), data, {
            "snd": Send(program_0_queue),
            "set": SetValue(),
            "add": AddValue(),
            "mul": MultiplyValue(),
            "mod": ModValue(),
            "rcv": Receive(program_1_queue),
            "jgz": JumpOnPositive(),
        })
    ]

    while True:
        if any(next(p) in [DONE, STILL_WAITING] for p in programs):
            return program_0_queue.added


class DayTest(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            set a 1
            add a 2
            mul a a
            mod a 5
            snd a
            set a 0
            rcv a
            jgz a -1
            set a 1
            jgz a -2""")

        assert_that(compute(input), is_(4))

    def test_puzzle(self):
        assert_that(compute(puzzle_input), is_(1187))


class Day2Test(unittest.TestCase):
    def test_example(self):
        input = dedent("""\
            snd 1
            snd 2
            snd p
            rcv a
            rcv b
            rcv c
            rcv d""")

        assert_that(compute2(input), is_(3))

    def test_simple(self):
        input = dedent("""\
            snd p
            rcv a
            jgz a 2
            snd 2""")

        assert_that(compute2(input), is_(2))

    def test_deadlock_program0_done(self):
        input = dedent("""\
            add p -1
            mul p -1
            jgz p 2
            rcv a""")

        assert_that(compute2(input), is_(0))

    def test_deadlock_program1_done(self):
        input = dedent("""\
            add p -1
            mul p -1
            jgz p 2
            rcv a""")

        assert_that(compute2(input), is_(0))

    def test_deadlock_program1_done_program0_not_done(self):
        input = dedent("""\
            jgz p 2
            rcv a
            snd 5""")

        assert_that(compute2(input), is_(1))

    def test_reach_deadlock(self):
        input = dedent("""\
            jgz p 4
            snd 1
            snd 2
            snd 3
            snd 4
            snd 5
            snd 6
            rcv a
            rcv b
            rcv c
            rcv d""")

        assert_that(compute2(input), is_(3))

    def test_puzzle_second(self):
        assert_that(compute2(puzzle_input), is_(5969))


puzzle_input = """\
set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 464
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19"""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

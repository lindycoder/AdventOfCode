import unittest
from collections import defaultdict, deque

from hamcrest import assert_that, is_


class Waiting(Exception):
    pass


class Instruction:
    pass


class BaseInstructionTest(unittest.TestCase):
    def setUp(self):
        self.registry = defaultdict(lambda: 0)


class SetValue(Instruction):
    def __call__(self, registry, target, value):
        target(value())


class SetValueTest(BaseInstructionTest):
    def test(self):
        SetValue()(self.registry, Var(self.registry, "a"), Scalar(1))
        assert_that(self.registry["a"], is_(1))


class AddValue(Instruction):
    def __call__(self, registry, target, source):
        target(target() + source())


class AddValueTest(BaseInstructionTest):
    def test(self):
        AddValue()(self.registry, Var(self.registry, "a"), Scalar(1))
        AddValue()(self.registry, Var(self.registry, "a"), Scalar(1))
        assert_that(self.registry["a"], is_(2))


class MultiplyValue(Instruction):
    def __call__(self, registry, target, source):
        target(target() * source())


class MultiplyValueTest(BaseInstructionTest):
    def test(self):
        self.registry["a"] = 5
        MultiplyValue()(self.registry, Var(self.registry, "a"), Scalar(5))
        assert_that(self.registry["a"], is_(25))


class ModValue(Instruction):
    def __call__(self, registry, target, source):
        target(target() % source())


class ModValueTest(BaseInstructionTest):
    def test(self):
        self.registry["a"] = 5
        ModValue()(self.registry, Var(self.registry, "a"), Scalar(3))
        assert_that(self.registry["a"], is_(2))


class Jump(Instruction):
    def __call__(self, registry, source, length):
        if source() > 0:
            return length()


class JumpTest(BaseInstructionTest):
    def test_do(self):
        self.registry["a"] = 5
        move = Jump()(self.registry, Var(self.registry, "a"), Scalar(3))

        assert_that(move, is_(3))

    def test_dont(self):
        self.registry["a"] = 0
        move = Jump()(self.registry, Var(self.registry, "a"), Scalar(3))

        assert_that(move, is_(None))


class Send(Instruction):
    def __init__(self, queue):
        self.queue = queue

    def __call__(self, registry, source):
        self.queue.append(source())


class SendTest(BaseInstructionTest):
    def test(self):
        queue = deque()
        Send(queue)(self.registry, Scalar(1))
        assert_that(queue.popleft(), is_(1))


class Receive(Instruction):
    def __init__(self, queue):
        self.queue = queue

    def __call__(self, registry, target):
        try:
            target(self.queue.popleft())
        except IndexError as e:
            raise Waiting from e


class ReceiveTest(BaseInstructionTest):
    def test(self):
        queue = deque((13,))
        Receive(queue)(self.registry, Var(self.registry, "a"))
        assert_that(self.registry["a"], is_(13))

    def test_waiting(self):
        queue = deque()
        with self.assertRaises(Waiting):
            Receive(queue)(self.registry, Var(self.registry, "a"))


class Scalar:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


class Var:
    def __init__(self, registry, name):
        self.registry = registry
        self.name = name

    def __call__(self, value=None):
        if value is None:
            return self.registry[self.name]
        else:
            self.registry[self.name] = value


def parse(registry, val):
    try:
        value = int(val)
    except ValueError:
        return Var(registry, val)

    return Scalar(value)


def compile(registry, instructions, data):
    def to_line(raw):
        parts = raw.split(" ")
        return instructions[parts[0]], [parse(registry, a) for a in parts[1:]]

    lines = [to_line(line) for line in data.split("\n")]
    return lines


def run_program(registry, data, instructions):
    lines = compile(registry, instructions, data)
    cursor = 0

    just_waited = False
    while 0 <= cursor < len(lines):
        instruction, args = lines[cursor]
        try:
            move = instruction(registry, *args)
            just_waited = False
            cursor += move if move is not None else 1
        except Waiting:
            if just_waited:
                yield STILL_WAITING

            yield WAITING
            just_waited = True

    while True:
        yield DONE


DONE = "DONE"
WAITING = "WAITING"
STILL_WAITING = "STILL_WAITING"

import logging
from abc import abstractmethod
from dataclasses import dataclass, field
from inspect import signature
from typing import List, Mapping, Tuple, Callable, Type, Dict

import pytest
from hamcrest import assert_that, is_, greater_than


@dataclass
class Parameter:
    @classmethod
    @abstractmethod
    def from_mode(cls, mode, state, val, relative_base):
        pass


@dataclass
class Reader(Parameter):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @classmethod
    def from_mode(cls, mode, state, val, relative_base):
        return {
            0: PositionalReader(state, val),
            1: ImmediateReader(val),
            2: PositionalReader(state, relative_base + val),
        }[mode]



@dataclass
class Writer(Parameter):
    inv: Callable

    def __call__(self, *args, **kwargs):
        return self.inv(*args, **kwargs)

    @classmethod
    def from_mode(cls, mode, state, val, relative_base):
        return cls({
            0: WritePositional(state, val),
            2: WritePositional(state, relative_base + val),
        }[mode])

    def __str__(self):
        return f"Writer using {self.inv}"

@dataclass
class Intcode:
    state: List[int]
    stdin: List[int] = field(default_factory=list)
    stdout: List[int] = field(default_factory=list)
    _index: int = 0
    _relative_base: int = 0
    _operations: Dict[int, Tuple[Callable, List[Type['Parameter']]]] = None
    _is_halted: bool = False

    class AwaitingInput(Exception):
        pass

    @classmethod
    def from_input(cls, raw, **kwargs):
        return cls(list(map(int, raw.strip().split(','))), **kwargs)

    def __post_init__(self):
        self._operations = {}

        for member in dir(self):
            if member.startswith('op_'):
                code = int(member.split('_')[1])
                fn = getattr(self, member)
                sig = signature(fn)
                self._operations[code] = (
                    fn, [p.annotation for p in sig.parameters.values()]
                )

    def __getitem__(self, item):
        self._adapt_size(item)
        return self.state[item]

    def __setitem__(self, key, value):
        self._adapt_size(key)
        self.state[key] = value

    def _adapt_size(self, index):
        if index >= len(self.state):
            self.state += [0 for _ in range(len(self.state), index + 1)]

    def run(self):
        try:
            while not self.is_halted:
                logging.debug(f'i={self._index}; state={self.state}')
                instruction = self[self._index]

                operation, op_params = self._operations[instruction % 100]

                args = []
                for i, p in enumerate(op_params):
                    val = self[self._index + i + 1]
                    mode = instruction // (10 ** (2 + i)) % 10

                    args.append(p.from_mode(mode,
                                            state=self,
                                            val=val,
                                            relative_base=self._relative_base))

                logging.debug(f'  {instruction}: {operation.__name__} :: {",".join(map(str, args))}')
                jump = operation(*args)
                if jump is not None:
                    self._index = jump
                else:
                    self._index += len(op_params) + 1
        except Intcode.AwaitingInput:
            pass

    @property
    def is_halted(self):
        return self._is_halted

    def op_1_add(self, a: Reader, b: Reader, target: Writer):
        target(a() + b())

    def op_2_multiply(self, a: Reader, b: Reader, target: Writer):
        target(a() * b())

    def op_3_read_input(self, target: Writer):
        try:
            target(self.stdin.pop(0))
        except IndexError as e:
            raise Intcode.AwaitingInput from e

    def op_4_output(self, a: Reader):
        self.stdout.append(a())

    def op_5_jump_if_true(self, v: Reader, jump: Reader):
        if v() != 0:
            return jump()

    def op_6_jump_if_false(self, v: Reader, jump: Reader):
        if v() == 0:
            return jump()

    def op_7_less_than(self, a: Reader, b: Reader, target: Writer):
        target(1 if a() < b() else 0)

    def op_8_equals(self, a: Reader, b: Reader, target: Writer):
        target(1 if a() == b() else 0)

    def op_9_update_relative_base(self, a: Reader):
        self._relative_base += a()

    def op_99_end(self):
        self._is_halted = True
        self._index = len(self.state)



@dataclass
class PositionalReader(Reader):
    state: List[int]
    index: int

    def __call__(self, *args, **kwargs):
        return self.state[self.index]

    def __str__(self):
        return f"Reader @ position {self.index} ({self.state[self.index]})"

@dataclass
class ImmediateReader(Reader):
    value: int

    def __call__(self, *args, **kwargs):
        return self.value

    def __str__(self):
        return f"Reader of {self.value}"


@dataclass
class WritePositional(Callable):
    state: List[int]
    index: int

    def __call__(self, value):
        self.state[self.index] = value

    def __str__(self):
        return f"Writer @ position {self.index} ({self.state[self.index]})"


@pytest.mark.parametrize('val,expect', [
    ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
     [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
])
def test_from_day2(val, expect):
    ex = Intcode(val)
    ex.run()
    assert_that(ex.state, is_(expect))


def test_3():
    code = Intcode.from_input('3,3,99,0')
    code.stdin.append(55)
    code.run()
    assert_that(code[3], is_(55))


def test_4():
    code = Intcode.from_input('4,0,4,4,99')
    code.run()
    assert_that(code.stdout, [4, 99])


def test_immediate_mode():
    code = Intcode.from_input('1002,4,3,4,33')
    code.run()
    assert_that(code[4], 4)


def test_delayed_input():
    code = Intcode.from_input('3,5,3,6,99,-1,-1')
    code.run()
    assert_that(code.is_halted, is_(False))
    code.stdin.append([10])
    code.run()
    assert_that(code.is_halted, is_(False))
    code.stdin.append([20])
    code.run()
    assert_that(code.is_halted, is_(True))
    assert_that(code[5], 10)
    assert_that(code[6], 20)


EQUAL_TO_8_POS = '3,9,8,9,10,9,4,9,99,-1,8'
LESS_THAN_8_POS = '3,9,7,9,10,9,4,9,99,-1,8'
EQUAL_TO_8_IMM = '3,3,1108,-1,8,3,4,3,99'
LESS_THAN_8_IMM = '3,3,1107,-1,8,3,4,3,99'


@pytest.mark.parametrize('program, input, output', [
    (EQUAL_TO_8_POS, 8, [1]),
    (EQUAL_TO_8_POS, 7, [0]),
    (EQUAL_TO_8_IMM, 8, [1]),
    (EQUAL_TO_8_IMM, 7, [0]),
    (LESS_THAN_8_POS, 8, [0]),
    (LESS_THAN_8_POS, 7, [1]),
    (LESS_THAN_8_IMM, 8, [0]),
    (LESS_THAN_8_IMM, 7, [1]),
])
def test_compare_tests(program, input, output):
    code = Intcode.from_input(program)
    code.stdin.append(input)
    code.run()
    assert_that(code.stdout, is_(output))


EQUAL_TO_0_JUMP_POS = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
EQUAL_TO_0_JUMP_IMM = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'

@pytest.mark.parametrize('program, input, output', [
    (EQUAL_TO_0_JUMP_POS, 0, [0]),
    (EQUAL_TO_0_JUMP_POS, 10, [1]),
    (EQUAL_TO_0_JUMP_IMM, 0, [0]),
    (EQUAL_TO_0_JUMP_IMM, 10, [1]),
])
def test_jump(program, input, output):
    code = Intcode.from_input(program)
    code.stdin.append(input)
    code.run()
    assert_that(code.stdout, is_(output))


def test_copy_extra_mem_copy_itself():
    program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    code = Intcode(program[:])
    code.run()
    assert_that(code.stdout, is_(program))


def test_compute_big_digits():
    program = [1102,34915192,34915192,7,4,7,99,0]
    code = Intcode(program[:])
    code.run()
    assert_that(code.stdout[0], greater_than(10 ** 15))


def test_output_big_digits():
    program = [104,1125899906842624,99]
    code = Intcode(program[:])
    code.run()
    assert_that(code.stdout[0], is_(1125899906842624))


import unittest

import sys
from hamcrest import assert_that, is_
from y2017.duet import *

class CountingMultiplyValue(MultiplyValue):
    def __init__(self):
        self.call_count = 0

    def __call__(self, registry, target, source):
        self.call_count += 1
        super().__call__(registry, target, source)


def compute(data):
    registry = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
    mul = CountingMultiplyValue()
    program = run_program(registry, data, {
        "set": SetValue(),
        "sub": SubValue(),
        "mul": mul,
        "jnz": JumpOnNonZero(),
    })

    while next(program) != DONE:
        pass

    return mul.call_count

def compute2_prog(data):
    registry = {'a': 1, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
    program = run_program(registry, data, {
        "set": SetValue(),
        "sub": SubValue(),
        "mul": MultiplyValue(),
        "jnz": JumpOnNonZero(),
    })

    while next(program) != DONE:
        print(str(registry))

    return registry['h']

def compute2(data):
    not_primes = 0

    base = (81 * 100 + 100000)
    for i in range(0, 1001):
        if not is_prime(base + (i * 17)):
            not_primes += 1

    return not_primes


class DayTest(unittest.TestCase):
    def test(self):
        assert_that(compute(puzzle_input), is_(6241))


class Day2Test(unittest.TestCase):
    def test(self):
        assert_that(compute2(puzzle_input), is_(909))


def is_prime(n):
    for i in range(2, int(n ** (1/2)) + 1):
        if n % i == 0:
            return False
    return True

class IsPrimeTest(unittest.TestCase):
    def test(self):
        assert_that(is_prime(2), is_(True))
        assert_that(is_prime(3), is_(True))
        assert_that(is_prime(4), is_(False))
        assert_that(is_prime(5), is_(True))
        assert_that(is_prime(6), is_(False))
        assert_that(is_prime(7), is_(True))
        assert_that(is_prime(8), is_(False))
        assert_that(is_prime(9), is_(False))
        assert_that(is_prime(10), is_(False))
        assert_that(is_prime(11), is_(True))



"""
0 set b 81
1 set c b
2 jnz a 2 -> 4
3 jnz 1 5 -> 8
4 mul b 100
5 sub b -100000
6 set c b
7 sub c -17000
8 set f 1         is_prime = True   for _ in range(0 step 17
9 set d 2
10 set e 2          for d in range(2, b)
11 set g d            for e in range(2, b) {      108100
12 mul g e
13 sub g b              if d * e - b == 0 :
14 jnz g 2  -> 16
15 set f 0                is_prime = False
16 sub e -1             e += 1
17 set g e
18 sub g b
19 jnz g -8 -> 11     }
20 sub d -1
21 set g d
22 sub g b          
23 jnz g -13 -> 10  }
24 jnz f 2 -> 26    if not is_prime
25 sub h -1             h += 1
26 set g b
27 sub g c
28 jnz g 2 -> 30
29 jnz 1 3 -> EXIT
30 sub b -17
31 jnz 1 -23 -> 8     * 1000 
"""

# all not prime from (81 * 100 + 100000) to (81 * 100 + 100000 + 17000)
puzzle_input = """\
set b 81
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23"""


puzzle_input_shorter = """\
set b 81
set c b
jnz a 2
jnz 1 5
mul b 1
sub b -100
set c b
sub c -170
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23"""

if __name__ == '__main__':

    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print("Result is {}".format(result))

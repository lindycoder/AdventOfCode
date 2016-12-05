import hashlib
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_

PREFIX = '00000'


def compute(door_id):
    password = {'0': '', '1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': ''}
    index = 0
    found = 0
    while found < 8:
        hash = hashlib.md5(bytes(door_id + str(index), "UTF-8")).hexdigest()
        if hash[:5] == PREFIX and hash[5] in password and password[hash[5]] == '':
            password[hash[5]] = hash[6]
            found += 1
        index += 1
    return "".join([v for k, v in sorted(password.items(), key=lambda e: e[0])])


class ComputeTest(unittest.TestCase):
    def test_1(self):
        assert_that(compute("abc"), is_("05ace8e3"))

if __name__ == '__main__':
    print("Result is {}".format(compute("abbhdwsy")))

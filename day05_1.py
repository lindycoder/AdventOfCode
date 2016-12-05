import hashlib
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_

PREFIX = '00000'


def compute(door_id):
    password = ""
    index = 0
    while len(password) < 8:
        hash = hashlib.md5(bytes(door_id + str(index), "UTF-8")).hexdigest()
        if hash[:5] == PREFIX:
            password += hash[5]
        index += 1
    return password


class ComputeTest(unittest.TestCase):
    def test_1(self):
        assert_that(compute("abc"), is_("18f47a30"))

if __name__ == '__main__':
    print("Result is {}".format(compute("abbhdwsy")))
